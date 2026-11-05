"""Tests for the analytics functions."""

from datetime import datetime

from habit_tracker.habit import Habit
from habit_tracker.analytics import (
    list_habit_names,
    habits_with_period,
    longest_streak,
    habit_with_longest_streak,
)


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