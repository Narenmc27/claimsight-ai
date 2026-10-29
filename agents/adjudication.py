def adjudicate(policy: dict, fraud: dict) -> dict:
    reasons = list(policy["reasons"])

    if policy["decision"] == "reject":
        decision = "reject"
    elif policy["decision"] == "human_review":
        decision = "human_review"
    elif fraud["risk"] == "high":
        decision = "human_review"
        reasons += fraud["signals"]
    else:
        decision = "approve"

    payout = policy["payout"] if decision == "approve" else 0
    return {
        "decision": decision,
        "payout": payout,
        "reasons": reasons,
        "fraud_risk": fraud["risk"],
    }