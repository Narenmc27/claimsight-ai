import json
from pathlib import Path

FINAL = {
    "F1": ("approve", 40000),
    "F2": ("human_review", 0),
    "F3": ("reject", 0),
    "F4": ("approve", 45000),
    "F5": ("human_review", 0),
    "F6": ("approve", 30000),
    "F7": ("approve", 60000),
    "F8": ("human_review", 0),
}

path = Path("data/fresh_claims.json")
claims = json.loads(path.read_text(encoding="utf-8"))
for c in claims:
    c["expected_decision"], c["expected_payout"] = FINAL[c["id"]]
path.write_text(json.dumps(claims, indent=2), encoding="utf-8")
print("updated", len(claims), "claims")