import sys
sys.path.append(".")

from tests.load_data import load_claims
from agents.extraction import extract
from agents.policy_check import check_policy
from agents.fraud_check import check_fraud
from agents.adjudication import adjudicate

passed = 0
claims = load_claims()
for claim in claims:
    extracted = extract(claim["description"]).model_dump()
    policy = check_policy(claim, extracted)
    fraud = check_fraud(claim, extracted)
    final = adjudicate(policy, fraud)

    ok = final["decision"] == claim["expected_decision"]
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {claim['id']}  got={final['decision']}  want={claim['expected_decision']}  payout={final['payout']}")
    print(f"       reasons: {final['reasons']}")

print(f"\nEnd-to-end: {passed}/{len(claims)}")