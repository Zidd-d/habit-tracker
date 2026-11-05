"""The HabitManager class: creates, changes, deletes and ticks off habits."""

from habit_tracker.habit import Habit, VALID_PERIODS
from habit_tracker.predefined_habits import PREDEFINED_HABITS


class HabitManager:
    """Manages all habits and saves every change through the repository."""

    def __init__(self, repository):
        self.repository = repository
        if self.repository.first_start:
            for name, period, category in PREDEFINED_HABITS:
                self.repository.save_habit(Habit(name, period, category))
        self.habits = self.repository.load_habits()

    def _name_taken(self, name, ignore=None):
        """Return True if another habit already has this name (case-insensitive)."""
        return any(
            habit.name.lower() == name.lower() and habit is not ignore
            for habit in self.habits
        )

    def create_habit(self, name, period, category):
        """Create, save and return a new habit."""
        name = name.strip()
        if not name:
            raise ValueError("Name must not be empty")
        if self._name_taken(name):
            raise ValueError("A habit with this name already exists")
        if period not in VALID_PERIODS:
            raise ValueError(f"Period must be one of {VALID_PERIODS}")
        habit = Habit(name, period, category)
        self.repository.save_habit(habit)
        self.habits.append(habit)
        return habit

    def rename_habit(self, habit, new_name):
        """Rename a habit and save it."""
        new_name = new_name.strip()
        if self._name_taken(new_name, ignore=habit):
            raise ValueError("A habit with this name already exists")
        habit.rename(new_name)
        self.repository.save_habit(habit)

    def change_period(self, habit, new_period):
        """Change the period of a habit and save it."""
        habit.change_period(new_period)
        self.repository.save_habit(habit)

    def change_category(self, habit, new_category):
        """Change the category of a habit and save it."""
        habit.change_category(new_category)
        self.repository.save_habit(habit)

    def delete_habit(self, habit):
        """Delete a habit from the database and from the list."""
        self.repository.delete_habit(habit)
        self.habits.remove(habit)

    def tick_off(self, habit, time=None):
        """Tick off a habit. Returns True if a completion was recorded."""
        recorded = habit.tick_off(time)
        if recorded:
            self.repository.save_habit(habit)
        return recorded