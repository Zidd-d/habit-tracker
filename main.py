"""Entry point: run this file to start the habit tracker."""

import os

from habit_tracker.habit_manager import HabitManager
from habit_tracker.habit_repository import HabitRepository
from habit_tracker.menu import Menu

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_FOLDER, "data", "habits.db")


def main():
    """Create the components and start the menu."""
    repository = HabitRepository(DB_PATH)
    manager = HabitManager(repository)
    Menu(manager).run()
    repository.close()


if __name__ == "__main__":
    main()