import sys
import json
from pathlib import Path
sys.path.append(".")

from agents.graph import graph

claims = json.loads(Path("data/heldout_claims.json").read_text(encoding="utf-8"))

SAFE_DECISIONS = {"reject": 0, "human_review": 1, "approve": 2}   # higher = riskier for the company

decision_ok = payout_ok = unsafe = 0
for c in claims:
    final = graph.invoke({"claim": c})["final"]
    d_ok = final["decision"] == c["expected_decision"]
    p_ok = final["payout"] == c["expected_payout"]
    decision_ok += d_ok
    payout_ok += p_ok
    too_risky = SAFE_DECISIONS[final["decision"]] > SAFE_DECISIONS[c["expected_decision"]]
    unsafe += too_risky

    tag = "PASS" if d_ok and p_ok else "FAIL"
    print(f"{tag}  {c['id']}  got={final['decision']} ({final['payout']})  want={c['expected_decision']} ({c['expected_payout']})")
    if tag == "FAIL":
        print(f"        reasons: {final['reasons']}")
        if too_risky:
            print("        !! UNSAFE: system was more generous than expected")

print(f"\nDecisions correct: {decision_ok}/{len(claims)}")
print(f"Payouts correct:   {payout_ok}/{len(claims)}")
print(f"Unsafe errors:     {unsafe}")