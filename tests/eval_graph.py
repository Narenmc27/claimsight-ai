import sys
sys.path.append(".")

from tests.load_data import load_claims
from agents.graph import graph

passed = 0
claims = load_claims()
for claim in claims:
    final = graph.invoke({"claim": claim})["final"]
    ok = final["decision"] == claim["expected_decision"]
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {claim['id']}  got={final['decision']}  want={claim['expected_decision']}")

print(f"\nGraph end-to-end: {passed}/{len(claims)}")
print("\n" + graph.get_graph().draw_mermaid())