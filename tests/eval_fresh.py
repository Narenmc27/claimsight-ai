import sys
import json
from pathlib import Path
sys.path.append(".")

from agents.graph import graph

claims = json.loads(Path("data/fresh_claims.json").read_text(encoding="utf-8"))

if any(c["expected_decision"] == "FILL_ME" for c in claims):
    print("Stop: fill in expected_decision for every claim first.")
    sys.exit()

RISK = {"reject": 0, "human_review": 1, "approve": 2}   # higher = more generous

decision_ok = payout_ok = unsafe = 0
for c in claims:
    final = graph.invoke({"claim": c})["final"]
    d_ok = final["decision"] == c["expected_decision"]
    p_ok = final["payout"] == c["expected_payout"]
    decision_ok += d_ok
    payout_ok += p_ok
    too_generous = RISK[final["decision"]] > RISK[c["expected_decision"]]
    unsafe += too_generous

    print(f"{'PASS' if d_ok and p_ok else 'FAIL'}  {c['id']}  got={final['decision']} ({final['payout']})  want={c['expected_decision']} ({c['expected_payout']})")
    if not (d_ok and p_ok):
        print(f"        reasons: {final['reasons']}")
        if too_generous:
            print("        !! UNSAFE: more generous than expected")

print(f"\nDecisions correct: {decision_ok}/{len(claims)}")
print(f"Payouts correct:   {payout_ok}/{len(claims)}")
print(f"Too generous:      {unsafe}")