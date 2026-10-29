import sys
sys.path.append(".")

from tests.load_data import load_claims
from agents.graph import graph

c1 = next(c for c in load_claims() if c["id"] == "C1")
claim = {**c1, "image_path": "data/images/this_file_does_not_exist.jpg"}

final = graph.invoke({"claim": claim})["final"]
ok = final["decision"] == "human_review"
print(f"{'PASS' if ok else 'FAIL'}  photo check fails -> got={final['decision']}  {final['reasons']}")