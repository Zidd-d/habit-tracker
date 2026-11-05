"""Tests for the HabitRepository (in-memory SQLite)."""

from datetime import datetime

from habit_tracker.habit import Habit
from habit_tracker.habit_repository import HabitRepository


def test_save_assigns_id_and_load_returns_habit():
    repo = HabitRepository(":memory:")
    habit = Habit("Read", "daily", "Learning", creation_time=datetime(2026, 11, 2, 8, 0))
    repo.save_habit(habit)
    loaded = repo.load_habits()
    assert habit.habit_id is not None
    assert len(loaded) == 1
    assert loaded[0].name == "Read"
    assert loaded[0].creation_time == datetime(2026, 11, 2, 8, 0)


def test_completions_are_saved_and_loaded():
    repo = HabitRepository(":memory:")
    habit = Habit("Read", "daily", "Learning")
    habit.completions = [datetime(2026, 11, 2, 9, 0), datetime(2026, 11, 3, 9, 0)]
    repo.save_habit(habit)
    assert repo.load_habits()[0].completions == habit.completions


def test_saving_again_updates_existing_habit():
    repo = HabitRepository(":memory:")
    habit = Habit("Read", "daily", "Learning")
    repo.save_habit(habit)
    habit.rename("Read a book")
    repo.save_habit(habit)
    loaded = repo.load_habits()
    assert len(loaded) == 1
    assert loaded[0].name == "Read a book"


def test_delete_removes_habit_and_completions():
    repo = HabitRepository(":memory:")
    habit = Habit("Read", "daily", "Learning")
    habit.completions = [datetime(2026, 11, 2, 9, 0)]
    repo.save_habit(habit)
    repo.delete_habit(habit)
    count = repo.connection.execute("SELECT COUNT(*) FROM HabitCompletion").fetchone()[0]
    assert repo.load_habits() == []
    assert count == 0


def test_first_start_flag_and_folder_creation(tmp_path):
    db_file = tmp_path / "data" / "habits.db"
    first = HabitRepository(str(db_file))
    assert first.first_start is True
    first.close()
    second = HabitRepository(str(db_file))
    assert second.first_start is False
    second.close()
