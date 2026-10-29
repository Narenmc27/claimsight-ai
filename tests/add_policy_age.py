import json
from pathlib import Path

AGES = {"C1": 400, "C2": 800, "C3": 200, "C4": 365, "C5": 600, "C6": 10}

path = Path("data/golden_claims.json")
claims = json.loads(path.read_text(encoding="utf-8"))
for c in claims:
    c["policy_age_days"] = AGES[c["id"]]
path.write_text(json.dumps(claims, indent=2), encoding="utf-8")
print("Added policy_age_days to", len(claims), "claims")