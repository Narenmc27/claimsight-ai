import sys
import json
from pathlib import Path
sys.path.append(".")

from agents.extraction import extract
from agents.policy_check import check_policy
from agents.fraud_check import check_fraud

claims = {c["id"]: c for c in json.loads(Path("data/fresh_claims.json").read_text(encoding="utf-8"))}

for cid in sys.argv[1:]:
    c = claims[cid]
    e = extract(c["description"]).model_dump()
    print(cid, "-", c["description"])
    print("  extracted:", e)
    print("  policy:   ", check_policy(c, e))
    print("  fraud:    ", check_fraud(c, e))
    print()