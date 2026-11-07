"""Start the menu with four weeks of example data (for demos and screenshots)."""

import os

from habit_tracker.habit_manager import HabitManager
from habit_tracker.habit_repository import HabitRepository
from habit_tracker.menu import Menu
from tests.example_data import build_example_habits

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
DEMO_DB = os.path.join(PROJECT_FOLDER, "data", "demo.db")


def main():
    """Build a fresh demo database from the example data and start the menu."""
    if os.path.exists(DEMO_DB):
        os.remove(DEMO_DB)
    repository = HabitRepository(DEMO_DB)
    for habit in build_example_habits():
        repository.save_habit(habit)
    # The habits are already there, so the manager must not add the predefined ones again.
    repository.first_start = False
    manager = HabitManager(repository)
    Menu(manager).run()
    repository.close()


if __name__ == "__main__":
    main()