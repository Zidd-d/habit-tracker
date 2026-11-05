"""Tests for the HabitManager."""

import pytest

from habit_tracker.habit_manager import HabitManager
from habit_tracker.habit_repository import HabitRepository
from habit_tracker.predefined_habits import PREDEFINED_HABITS


def make_manager():
    return HabitManager(HabitRepository(":memory:"))


def test_first_start_creates_predefined_habits():
    manager = make_manager()
    assert len(manager.habits) == len(PREDEFINED_HABITS)


def test_create_habit_is_saved():
    manager = make_manager()
    habit = manager.create_habit("Test habit", "daily", "Testing")
    saved = manager.repository.load_habits()
    assert habit in manager.habits
    assert "Test habit" in [h.name for h in saved]


def test_duplicate_name_is_rejected():
    manager = make_manager()
    manager.create_habit("Test habit", "daily", "Testing")
    with pytest.raises(ValueError):
        manager.create_habit("test HABIT", "weekly", "Testing")


def test_rename_to_existing_name_is_rejected():
    manager = make_manager()
    first = manager.create_habit("First", "daily", "Testing")
    manager.create_habit("Second", "daily", "Testing")
    with pytest.raises(ValueError):
        manager.rename_habit(first, "second")


def test_tick_off_is_saved_once_per_cycle():
    manager = make_manager()
    habit = manager.create_habit("Test habit", "daily", "Testing")
    assert manager.tick_off(habit) is True
    assert manager.tick_off(habit) is False
    saved = [h for h in manager.repository.load_habits() if h.name == "Test habit"]
    assert len(saved[0].completions) == 1


def test_delete_habit_removes_it_everywhere():
    manager = make_manager()
    habit = manager.create_habit("Test habit", "daily", "Testing")
    manager.delete_habit(habit)
    saved_names = [h.name for h in manager.repository.load_habits()]
    assert habit not in manager.habits
    assert "Test habit" not in saved_names