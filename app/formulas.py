"""Derived values computed on the fly — never stored as columns (docs/lld.md §2)."""


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def calculate_estimated_daily_calories(weight_kg: float, height_cm: float, age: int) -> int:
    """Sex-neutral Mifflin-St Jeor variant with a flat 1.4 activity multiplier.

    This is the MAINTENANCE figure, not goal-adjusted — the guardrail's crash-diet
    threshold (docs/nfr-guardrail-spec.md §3.1.3) compares against 75% of this value,
    which would silently weaken if it were pre-reduced for a "lose weight" goal.
    """
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 78
    return round(bmr * 1.4)
