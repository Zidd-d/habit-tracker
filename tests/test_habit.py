"""Tests for the Habit class."""

import pytest

from habit_tracker.habit import Habit

def test_tick_off_records_completion():
    habit = Habit("Read", "daily", "Learning")
    result = habit.tick_off()
    assert result is True
    assert len(habit.completions) == 1


def test_tick_off_twice_in_same_cycle_does_nothing():
    habit = Habit("Read", "daily", "Learning")
    habit.tick_off()
    result = habit.tick_off()
    assert result is False
    assert len(habit.completions) == 1

def test_rename_changes_name():
    habit = Habit("Read", "daily", "Learning")
    habit.rename("Read a book")
    assert habit.name == "Read a book"


def test_rename_rejects_empty_name():
    habit = Habit("Read", "daily", "Learning")
    with pytest.raises(ValueError):
        habit.rename("   ")
    assert habit.name == "Read"


def test_change_period_keeps_history():
    habit = Habit("Read", "daily", "Learning")
    habit.tick_off()
    habit.change_period("weekly")
    assert habit.period == "weekly"
    assert len(habit.completions) == 1


def test_change_period_rejects_unknown_value():
    habit = Habit("Read", "daily", "Learning")
    with pytest.raises(ValueError):
        habit.change_period("yearly")
    assert habit.period == "daily"


def test_change_category():
    habit = Habit("Read", "daily", "Learning")
    habit.change_category("Health")
    assert habit.category == "Health"