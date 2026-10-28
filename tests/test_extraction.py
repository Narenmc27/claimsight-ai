import sys
sys.path.append(".")

from tests.load_data import load_claims
from agents.extraction import extract

for claim in load_claims():
    result = extract(claim["description"])
    print(claim["id"], "->", result.model_dump())