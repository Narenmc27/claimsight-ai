import sys
sys.path.append(".")

from tests.load_data import load_claims
from agents.extraction import extract

# Only the fields we are sure about
EXPECTED = {
    "C1": {"incident_type": "accident", "driver_drunk": False},
    "C2": {"incident_type": "accident", "driver_drunk": True},
    "C4": {"incident_type": "theft"},
    "C5": {"incident_type": "wear_and_tear"},
    "C6": {"incident_type": "accident", "driver_drunk": False},
}

passed, total = 0, 0
for claim in load_claims():
    cid = claim["id"]
    if cid not in EXPECTED:
        continue
    result = extract(claim["description"]).model_dump()
    for field, expected_value in EXPECTED[cid].items():
        total += 1
        ok = result[field] == expected_value
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}  {cid}  {field} = {result[field]}")

print(f"\nScore: {passed}/{total}")