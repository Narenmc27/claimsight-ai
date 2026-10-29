import sys
sys.path.append(".")

from tests.load_data import load_claims
from agents.extraction import extract
from agents.fraud_check import check_fraud

EXPECTED = {"C1": "low", "C2": "low", "C3": "low", "C4": "medium", "C5": "low", "C6": "high"}

passed = 0
for claim in load_claims():
    extracted = extract(claim["description"]).model_dump()
    result = check_fraud(claim, extracted)
    ok = result["risk"] == EXPECTED[claim["id"]]
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {claim['id']}  {result['risk']}  {result['signals']}")

print(f"\nScore: {passed}/{len(EXPECTED)}")