"""Hand-written example timestamps (4 weeks per predefined habit) for the tests."""

from datetime import datetime

from habit_tracker.habit import Habit
from habit_tracker.predefined_habits import PREDEFINED_HABITS

# The four weeks run from Monday 5 Oct 2026 to Sunday 1 Nov 2026.
CREATION_TIME = datetime(2026, 10, 5, 7, 0)
# "Today" is the Monday after the four weeks. Its cycle is still open.
EXAMPLE_TODAY = datetime(2026, 11, 2, 12, 0)


def _stamps(hour, *dates):
    """Turn date strings like "10-05" into datetimes at the given hour."""
    return [datetime.fromisoformat(f"2026-{date}T{hour:02d}:00:00") for date in dates]


EXAMPLE_COMPLETIONS = {
    # Misses 14 Oct, 23-24 Oct and 30 Oct.
    "Brush teeth": _stamps(
        21,
        "10-05", "10-06", "10-07", "10-08", "10-09", "10-10", "10-11", "10-12", "10-13",
        "10-15", "10-16", "10-17", "10-18", "10-19", "10-20", "10-21", "10-22",
        "10-25", "10-26", "10-27", "10-28", "10-29",
        "10-31", "11-01",
    ),
    # Patchy: several short runs and long gaps.
    "Read book 30 min": _stamps(
        20,
        "10-05", "10-06", "10-07",
        "10-10", "10-11", "10-12", "10-13",
        "10-16",
        "10-19", "10-20", "10-21", "10-22", "10-23",
        "10-27", "10-28",
        "10-31", "11-01",
    ),
    # Done in week 1, 2 and 4, missed in week 3.
    "Grocery shopping": _stamps(17, "10-10", "10-13", "10-31"),
    # Missed in week 1, then done in weeks 2, 3 and 4.
    "Bring out trash": _stamps(19, "10-14", "10-21", "10-28"),
    # Weekdays only. Friday 16 Oct is missed, Saturday 24 Oct is ticked.
    "Update calendar": _stamps(
        9,
        "10-05", "10-06", "10-07", "10-08", "10-09",
        "10-12", "10-13", "10-14", "10-15",
        "10-19", "10-20", "10-21", "10-22", "10-23", "10-24",
        "10-26", "10-27", "10-28", "10-29", "10-30",
    ),
}


def build_example_habits():
    """Return the five predefined habits, filled with the example completions."""
    habits = []
    for name, period, category in PREDEFINED_HABITS:
        habit = Habit(name, period, category, creation_time=CREATION_TIME)
        habit.completions = list(EXAMPLE_COMPLETIONS[name])
        habits.append(habit)
    return habits