import sys
sys.path.append(".")

from agents.policy_search import load_rules, KeywordSearch, SemanticSearch

# (claim text, part of the rule that MUST be found)
CASES = [
    ("My car was hit from behind at a traffic signal.", "Accident damage"),
    ("I hit a divider at night. The police test showed I had been drinking.", "drunk or under drugs"),
    ("A truck scratched my car door. I reported it after 45 days.", "within 30 days"),
    ("My car was stolen from outside my house last night.", "Theft of the insured car"),
    ("My front tyres are very old and worn. Please pay for new tyres.", "wear and tear"),
    # harder: different words than the rule
    ("I had a few beers before the crash.", "drunk or under drugs"),
    ("My driving permit had expired last month.", "no valid licence"),
    ("We were doing a street race with friends when I crashed.", "Racing or stunt"),
]

rules = load_rules()
searchers = {"Keyword": KeywordSearch(rules), "Meaning": SemanticSearch(rules)}

for name, search in searchers.items():
    hits = 0
    print(f"\n--- {name} search ---")
    for query, must_find in CASES:
        top = [r["text"] for r in search.search(query, k=1)]
        ok = any(must_find.lower() in t.lower() for t in top)
        hits += ok
        print(f"{'HIT ' if ok else 'MISS'}  {must_find}   <- {query[:45]}")
    print(f"{name} search: {hits}/{len(CASES)}")
    