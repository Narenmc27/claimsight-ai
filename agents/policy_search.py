import re
from pathlib import Path
from rank_bm25 import BM25Okapi
import numpy as np

def load_rules(path="data/policy.md"):
    """Cut the policy into one rule per item."""
    rules, section = [], ""
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("## "):
            section = line[3:]
        elif line.startswith("- "):
            rules.append({"id": len(rules), "section": section, "text": line[2:]})
    return rules


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


class KeywordSearch:
    def __init__(self, rules):
        self.rules = rules
        self.bm25 = BM25Okapi([tokenize(r["section"] + " " + r["text"]) for r in rules])

    def search(self, query, k=3):
        scores = self.bm25.get_scores(tokenize(query))
        best = sorted(range(len(self.rules)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.rules[i] for i in best]

class SemanticSearch:
    def __init__(self, rules):
        from fastembed import TextEmbedding
        self.rules = rules
        self.model = TextEmbedding("BAAI/bge-small-en-v1.5")
        texts = [r["section"] + ": " + r["text"] for r in rules]
        vectors = np.array(list(self.model.embed(texts)))
        self.vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

    def search(self, query, k=3):
        q = np.array(list(self.model.embed([query])))[0]
        q = q / np.linalg.norm(q)
        scores = self.vectors @ q          # similarity of the claim to each rule
        best = np.argsort(scores)[::-1][:k]
        return [self.rules[int(i)] for i in best]