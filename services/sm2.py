from datetime import date, timedelta


def sm2_review(
    repetition: int,
    interval_days: int,
    ease_factor: float,
    quality: int
):
    """
    SM-2 algorithm

    quality:
    0-5

    Returns:
    {
        repetition,
        interval_days,
        ease_factor,
        last_reviewed,
        next_due
    }
    """

    if quality < 0 or quality > 5:
        raise ValueError("Quality must be between 0 and 5")

    # --------------------------------------------------
    # FAILED RECALL
    # --------------------------------------------------

    if quality < 3:

        repetition = 0
        interval_days = 1

    else:

        repetition += 1

        if repetition == 1:
            interval_days = 1

        elif repetition == 2:
            interval_days = 6

        else:
            interval_days = round(
                interval_days * ease_factor
            )

    # --------------------------------------------------
    # EASE FACTOR UPDATE
    # --------------------------------------------------

    ease_factor = ease_factor + (
        0.1
        - (5 - quality)
        * (
            0.08
            + (5 - quality) * 0.02
        )
    )

    if ease_factor < 1.3:
        ease_factor = 1.3

    today = date.today()

    next_due = today + timedelta(
        days=interval_days
    )

    return {
        "repetition": repetition,
        "interval_days": interval_days,
        "ease_factor": round(
            ease_factor,
            2
        ),
        "last_reviewed": today.isoformat(),
        "next_due": next_due.isoformat()
    }