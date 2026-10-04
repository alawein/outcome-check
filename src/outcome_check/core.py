from outcome_check.contract import age_seconds, validate


def same_json(left: object, right: object) -> bool:
    if type(left) in (int, float) and type(right) in (int, float):
        return left == right
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(same_json(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(
            same_json(a, b) for a, b in zip(left, right, strict=True)
        )
    return left == right


def check_packet(packet: dict) -> dict:
    validate(packet)
    actions = {row["id"]: row for row in packet["actions"]}
    observations = {row["id"]: row for row in packet["observations"]}
    results = []
    for requirement in sorted(packet["requirements"], key=lambda row: row["id"]):
        action_id = requirement["action_id"]
        action = (
            "not_required"
            if action_id is None
            else {"succeeded": "confirmed", "failed": "contradicted", "unknown": "unobserved"}[
                actions.get(action_id, {"status": "unknown"})["status"]
            ]
        )
        observation = observations.get(requirement["observation_id"])
        outcome, reason = "unobserved", "missing observation"
        if observation is not None:
            age = age_seconds(packet["as_of"], observation["observed_at"])
            if observation["subject"] != requirement["subject"]:
                reason = "subject mismatch"
            elif age < 0:
                reason = "future observation"
            elif age > requirement["max_age_seconds"]:
                reason = "stale observation"
            else:
                value = observation["state"]
                for key in requirement["path"]:
                    if type(value) is not dict or key not in value:
                        reason = "missing object path"
                        break
                    value = value[key]
                else:
                    outcome = (
                        "confirmed" if same_json(value, requirement["expected"]) else "contradicted"
                    )
                    reason = (
                        "expected value observed"
                        if outcome == "confirmed"
                        else "different value observed"
                    )
        status = (
            "contradicted"
            if "contradicted" in (action, outcome)
            else "confirmed"
            if outcome == "confirmed" and action in ("confirmed", "not_required")
            else "unobserved"
        )
        results.append(
            {
                "id": requirement["id"],
                "action": action,
                "outcome": outcome,
                "status": status,
                "reason": reason,
                "action_id": action_id,
                "observation_id": requirement["observation_id"],
            }
        )
    counts = {
        status: sum(row["status"] == status for row in results)
        for status in ("confirmed", "contradicted", "unobserved")
    }
    return {
        "schema_version": 1,
        "results": results,
        "counts": counts,
        "exit_code": int(any(row["status"] != "confirmed" for row in results)),
    }
