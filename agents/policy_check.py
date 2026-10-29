MAX_PAYOUT = 500_000
DEDUCTIBLE = 5_000
REPORT_DEADLINE_DAYS = 30
POLICE_REPORT_ABOVE = 50_000


def check_policy(claim: dict, extracted: dict) -> dict:
    reject, review = [], []

    # Exclusions
    if extracted["driver_drunk"]:
        reject.append("Exclusion: driver drunk or under drugs")
    if extracted["no_valid_licence"]:
        reject.append("Exclusion: no valid licence")
    if extracted["racing_or_stunt"]:
        reject.append("Exclusion: racing or stunt driving")
    if extracted["intentional_damage"]:
        reject.append("Exclusion: damage done on purpose")
    if extracted["incident_type"] == "wear_and_tear":
        reject.append("Exclusion: normal wear and tear")

    # Deadline
    if claim["days_to_report"] > REPORT_DEADLINE_DAYS:
        reject.append(f"Reported after {claim['days_to_report']} days (limit {REPORT_DEADLINE_DAYS})")

    # Missing documents or unclear case: a human must look
    if extracted["incident_type"] == "theft" and not claim["police_report"]:
        review.append("Theft claim without police report")
    if claim["amount"] > POLICE_REPORT_ABOVE and not claim["police_report"]:
        review.append("Amount above Rs 50,000 needs a police report")
    if extracted["incident_type"] == "accident" and not claim["photos"]:
        review.append("Accident claim without photos")
    if extracted["incident_type"] == "other":
        review.append("Incident type unclear")

    if reject:
        decision = "reject"
    elif review:
        decision = "human_review"
    else:
        decision = "pass"

    payout = 0
    if decision == "pass":
        payout = max(0, min(claim["amount"] - DEDUCTIBLE, MAX_PAYOUT))

    return {"decision": decision, "reasons": reject + review, "payout": payout}