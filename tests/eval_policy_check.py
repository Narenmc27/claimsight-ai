import sys
sys.path.append(".")

from tests.load_data import load_claims
from agents.extraction import extract
from agents.policy_check import check_policy

# C6 looks fine on policy rules. The Fraud Agent (Step 6) will catch it.
EXPECTED = {
    "C1": "pass", "C2": "reject", "C3": "reject",
    "C4": "human_review", "C5": "reject", "C6": "pass",
}

passed = 0
for claim in load_claims():
    extracted = extract(claim["description"]).model_dump()
    result = check_policy(claim, extracted)
    ok = result["decision"] == EXPECTED[claim["id"]]
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {claim['id']}  {result['decision']}  {result['reasons']}  payout={result['payout']}")

print(f"\nScore: {passed}/{len(EXPECTED)}")