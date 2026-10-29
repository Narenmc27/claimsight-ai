def adjudicate(policy: dict, fraud: dict, vision: dict | None = None) -> dict:
    reasons = list(policy["reasons"])

    if policy["decision"] == "reject":
        decision = "reject"
    elif policy["decision"] == "human_review":
        decision = "human_review"
    else:
        decision = "approve"
        if fraud["risk"] == "high":
            decision = "human_review"
            reasons += fraud["signals"]
        if vision:
            if vision.get("error"):
                decision = "human_review"
                reasons.append(f"Photo could not be checked ({vision['error']})")
            elif not vision["is_car"]:
                decision = "human_review"
                reasons.append("Photo does not show a vehicle")
            elif vision["incident_type"] == "accident" and not vision["damage_visible"]:
                decision = "human_review"
                reasons.append("Accident claim, but photo shows no damage")

    payout = policy["payout"] if decision == "approve" else 0
    return {
        "decision": decision,
        "payout": payout,
        "reasons": reasons,
        "fraud_risk": fraud["risk"],
    }