"""Tests for the Habit class."""

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