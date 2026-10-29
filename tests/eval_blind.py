import sys
import json
from pathlib import Path
sys.path.append(".")

from agents.graph import graph

claims = json.loads(Path("data/blind_claims.json").read_text(encoding="utf-8"))

ok_count = 0
for c in claims:
    final = graph.invoke({"claim": c})["final"]
    ok = final["decision"] == c["expected_decision"] and final["payout"] == c["expected_payout"]
    ok_count += ok
    print(f"{'PASS' if ok else 'FAIL'}  {c['id']}  got={final['decision']} ({final['payout']})  want={c['expected_decision']} ({c['expected_payout']})")
    print(f"        reasons: {final['reasons']}")

print(f"\nBlind test: {ok_count}/{len(claims)}")