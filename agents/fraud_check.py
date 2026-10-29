NEW_POLICY_DAYS = 30
HIGH_AMOUNT = 300_000


def check_fraud(claim: dict, extracted: dict) -> dict:
    score, signals = 0, []

    if claim["policy_age_days"] < NEW_POLICY_DAYS:
        score += 2
        signals.append(f"Policy only {claim['policy_age_days']} days old")
    if claim["amount"] > HIGH_AMOUNT:
        score += 1
        signals.append(f"High amount: Rs {claim['amount']:,}")
    if extracted["incident_type"] == "theft" and not claim["police_report"]:
        score += 1
        signals.append("Theft without police report")

    risk = "high" if score >= 3 else "medium" if score == 2 else "low"
    return {"risk": risk, "score": score, "signals": signals}