# ClaimSight AI

Multi-agent insurance claims triage. It reads a car insurance claim, checks it
against the policy, scores fraud risk, checks the damage photo, and decides:
**approve**, **reject**, or **human review**, with reasons.

## How it works

```
claim -> extract -+-> policy check -+
                  |                 |
                  +-> fraud check --+-> adjudicate -> decision + reasons
                  |                 |
                  +-> photo check --+
```

| Part | Technology | Job |
|---|---|---|
| Extraction | LLM with strict JSON schema | Turns the claim text into clean fields |
| Policy check | Plain Python | Exclusions, deadline, documents, payout limits |
| Fraud check | Plain Python | Explainable warning signs, no guessing |
| Photo check | Gemini vision | Is it a car? Is damage visible? |
| Adjudication | Plain Python | Combines everything. If unsure, a person checks |
| Policy search | BM25 vs embeddings | Finds the matching policy rule (compared on labelled cases) |
| Orchestration | LangGraph | Runs policy, fraud and photo checks side by side |

**Design rule:** the LLM reads text and images. Code makes the decisions that
must be correct and repeatable.

## Results (honest)

| Test | Claims | Score | Note |
|---|---|---|---|
| Golden claims | 6 | 6/6 | Used while building |
| Held-out, first run | 16 | **14/16** | Not seen before. 2 real failures |
| Held-out, after fixes | 16 | 16/16 | Tuned on these, so not a clean score |
| Fresh set (development) | 8 | 8/8 | Answers and code adjusted while looking at them |
| Blind set | 6 | 6/6 | Written by someone else, run once, no changes after |
| Vision | 3 photos | 3/3 | Tiny test |
| Policy search, top 3 | 8 | keyword 5/8, embeddings 8/8 | Small test |
| Policy search, top 1 | 8 | keyword 3/8, embeddings 7/8 | Small test |

## What went wrong, and what I learned

- The model confused **whose action** a field describes (another driver was
  drunk, a thief damaged the car, a brother was driving). I rewrote the field
  descriptions and added an `other_driver` field.
- A yes/no field cannot hold "not sure". I added `alcohol_uncertain`, which
  sends the claim to a human.
- A test that only checks the decision can hide a pass for the wrong reason.
  My tests now print the reasons too.
- When Gemini timed out, the whole claim crashed. Now a failed photo check sends
  the claim to human review, and the vision test reports it as SKIP instead of
  a fake pass.
- Several of my first test answers disagreed with my own policy text. I fixed
  the policy text, not the score.
- `pip install agents` installed an unrelated library that shadowed my own
  `agents` folder. Adding `__init__.py` files fixed it.

## Limits

- Small test sets (6 to 16 claims)
- Fraud thresholds are hand-picked, not learned from data
- The policy is a short, made-up car insurance policy
- A claim below the deductible is approved with a payout of 0

## Project structure

```
agents/      extraction, policy_check, fraud_check, vision, adjudication, graph
data/        policy.md, golden / held-out / fresh / blind claims, test images
tests/       eval scripts for every agent and for the full graph
```

## Run

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python tests/eval_graph.py
```

Needs `GROQ_API_KEY`, `GOOGLE_API_KEY` and `VISION_MODEL` in a `.env` file.
