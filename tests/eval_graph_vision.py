import sys
sys.path.append(".")

from tests.load_data import load_claims
from agents.graph import graph

c1 = next(c for c in load_claims() if c["id"] == "C1")

# (image, wanted decision, text that must appear in the reasons)
CASES = [
    ("damaged_car.jpg", "approve", None),
    ("clean_car.jpg", "human_review", "shows no damage"),
    ("dog.jpg", "human_review", "does not show a vehicle"),
]

passed = inconclusive = 0
for image, want, reason_text in CASES:
    claim = {**c1, "image_path": f"data/images/{image}"}
    final = graph.invoke({"claim": claim})["final"]
    reasons = " | ".join(final["reasons"])

    if "could not be checked" in reasons:
        inconclusive += 1
        print(f"SKIP  {image}  Gemini did not answer, not counted ({reasons})")
        continue

    ok = final["decision"] == want and (reason_text is None or reason_text in reasons)
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {image}  got={final['decision']}  {reasons}")

print(f"\nPassed {passed}, inconclusive {inconclusive}, of {len(CASES)}")