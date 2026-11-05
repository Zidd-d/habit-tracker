"""Tests for the analytics functions."""

from habit_tracker.habit import Habit
from habit_tracker.analytics import list_habit_names, habits_with_period


def test_list_habit_names():
    habits = [Habit("Read", "daily", "Learning"), Habit("Clean", "weekly", "Home")]
    assert list_habit_names(habits) == ["Read", "Clean"]


def test_habits_with_period():
    read = Habit("Read", "daily", "Learning")
    clean = Habit("Clean", "weekly", "Home")
    stretch = Habit("Stretch", "daily", "Health")
    result = habits_with_period([read, clean, stretch], "daily")
    assert result == [read, stretch]