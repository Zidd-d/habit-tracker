"""Tests for the analytics functions."""

from datetime import datetime

from habit_tracker.habit import Habit
from habit_tracker.analytics import (
    list_habit_names,
    habits_with_period,
    longest_streak,
    habit_with_longest_streak,
    consistency,
)
from tests.example_data import EXAMPLE_TODAY, build_example_habits


def test_list_habit_names():
    habits = [Habit("Read", "daily", "Learning"), Habit("Clean", "weekly", "Home")]
    assert list_habit_names(habits) == ["Read", "Clean"]


def test_habits_with_period():
    read = Habit("Read", "daily", "Learning")
    clean = Habit("Clean", "weekly", "Home")
    stretch = Habit("Stretch", "daily", "Health")
    result = habits_with_period([read, clean, stretch], "daily")
    assert result == [read, stretch]


def make_daily_habit(day_numbers):
    """Helper: daily habit created on 2 Nov 2026, ticked on the given November days."""
    habit = Habit("Read", "daily", "Learning", creation_time=datetime(2026, 11, 2, 8, 0))
    habit.completions = [datetime(2026, 11, day, 9, 0) for day in day_numbers]
    return habit


def test_longest_streak_with_gap():
    habit = make_daily_habit([2, 3, 5])
    assert longest_streak(habit, datetime(2026, 11, 6, 10, 0)) == 2


def test_open_current_cycle_does_not_break_streak():
    habit = make_daily_habit([2, 3, 4])
    assert longest_streak(habit, datetime(2026, 11, 5, 10, 0)) == 3


def test_no_completions_gives_zero():
    habit = make_daily_habit([])
    assert longest_streak(habit, datetime(2026, 11, 6, 10, 0)) == 0


def test_habit_with_longest_streak():
    short = make_daily_habit([2])
    long = make_daily_habit([2, 3, 4])
    result = habit_with_longest_streak([short, long], datetime(2026, 11, 5, 10, 0))
    assert result is long


def test_weekly_streak_over_three_weeks():
    habit = Habit("Clean", "weekly", "Home", creation_time=datetime(2026, 11, 2, 8, 0))
    habit.completions = [
        datetime(2026, 11, 3, 9, 0),
        datetime(2026, 11, 10, 9, 0),
        datetime(2026, 11, 17, 9, 0),
    ]
    assert longest_streak(habit, datetime(2026, 11, 19, 10, 0)) == 3


def test_weekly_streak_with_missed_week():
    habit = Habit("Clean", "weekly", "Home", creation_time=datetime(2026, 11, 2, 8, 0))
    habit.completions = [
        datetime(2026, 11, 3, 9, 0),
        datetime(2026, 11, 17, 9, 0),
    ]
    assert longest_streak(habit, datetime(2026, 11, 19, 10, 0)) == 1


def test_monthly_streak_across_year_boundary():
    habit = Habit("Review", "monthly", "Work", creation_time=datetime(2026, 11, 15, 8, 0))
    habit.completions = [
        datetime(2026, 11, 20, 9, 0),
        datetime(2026, 12, 5, 9, 0),
        datetime(2027, 1, 10, 9, 0),
    ]
    assert longest_streak(habit, datetime(2027, 1, 20, 10, 0)) == 3


def test_consistency_daily_window():
    habit = make_daily_habit([2, 3, 5])
    today = datetime(2026, 11, 6, 10, 0)
    assert consistency(habit, today, 3) == 0.5
    assert consistency(habit, today, 5) == 0.75


def test_consistency_weekly():
    habit = Habit("Clean", "weekly", "Home", creation_time=datetime(2026, 11, 2, 8, 0))
    habit.completions = [datetime(2026, 11, 3, 9, 0), datetime(2026, 11, 17, 9, 0)]
    assert consistency(habit, datetime(2026, 11, 19, 10, 0), 28) == 0.5


def test_consistency_not_enough_data():
    habit = Habit("Clean", "weekly", "Home", creation_time=datetime(2026, 11, 2, 8, 0))
    assert consistency(habit, datetime(2026, 11, 19, 10, 0), 3) is None


# ----- tests with the four weeks of example data -----

EXPECTED_LONGEST_STREAKS = {
    "Brush teeth": 9,
    "Read book 30 min": 5,
    "Grocery shopping": 2,
    "Bring out trash": 3,
    "Update calendar": 6,
}


def get_example_habit(name):
    return next(habit for habit in build_example_habits() if habit.name == name)


def test_example_data_longest_streaks():
    for habit in build_example_habits():
        expected = EXPECTED_LONGEST_STREAKS[habit.name]
        assert longest_streak(habit, EXAMPLE_TODAY) == expected, habit.name


def test_example_data_habit_with_longest_streak():
    best = habit_with_longest_streak(build_example_habits(), EXAMPLE_TODAY)
    assert best.name == "Brush teeth"


def test_example_data_daily_habits():
    names = list_habit_names(habits_with_period(build_example_habits(), "daily"))
    assert names == ["Brush teeth", "Read book 30 min", "Update calendar"]


def test_example_data_consistency_four_weeks():
    assert consistency(get_example_habit("Read book 30 min"), EXAMPLE_TODAY, 29) == 17 / 28
    assert consistency(get_example_habit("Update calendar"), EXAMPLE_TODAY, 29) == 20 / 28
    assert consistency(get_example_habit("Bring out trash"), EXAMPLE_TODAY, 29) == 3 / 4


def test_example_data_consistency_last_week():
    assert consistency(get_example_habit("Brush teeth"), EXAMPLE_TODAY, 7) == 5 / 6
    assert consistency(get_example_habit("Read book 30 min"), EXAMPLE_TODAY, 7) == 4 / 6