import sys
sys.path.append(".")

from agents.vision import analyze_damage

CASES = [
    ("data/images/damaged_car.jpg", {"is_car": True, "damage_visible": True}),
    ("data/images/clean_car.jpg",   {"is_car": True, "damage_visible": False}),
    ("data/images/dog.jpg",         {"is_car": False, "damage_visible": False}),
]

passed, total = 0, 0
for path, expected in CASES:
    result = analyze_damage(path).model_dump()
    print(f"\n{path}\n  {result['summary']} (severity: {result['severity']})")
    for field, want in expected.items():
        total += 1
        ok = result[field] == want
        passed += ok
        print(f"  {'PASS' if ok else 'FAIL'}  {field} = {result[field]}")

print(f"\nScore: {passed}/{total}")