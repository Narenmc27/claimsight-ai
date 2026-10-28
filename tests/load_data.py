import json
from pathlib import Path

def load_claims():
    path = Path("data/golden_claims.json")
    return json.loads(path.read_text(encoding="utf-8"))

def load_policy():
    path = Path("data/policy.md")
    return path.read_text(encoding="utf-8")

if __name__ == "__main__":
    claims = load_claims()
    print(f"Loaded {len(claims)} claims")
    for c in claims:
        print(c["id"], "->", c["expected_decision"])