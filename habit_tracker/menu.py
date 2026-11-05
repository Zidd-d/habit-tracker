"""The command-line menu: asks the user for input and shows the results."""

from datetime import datetime

from habit_tracker import analytics
from habit_tracker.habit import VALID_PERIODS

UNITS = {"daily": "days", "weekly": "weeks", "monthly": "months"}


class Menu:
    """Text menu that connects the user, the manager and the analytics."""

    def __init__(self, manager):
        self.manager = manager

    def run(self):
        """Show the main menu until the user chooses to exit."""
        actions = {
            "1": self.show_habits,
            "2": self.tick_off_habit,
            "3": self.create_habit,
            "4": self.change_habit,
            "5": self.delete_habit,
            "6": self.show_analytics,
        }
        while True:
            print("\n=== Habit tracker ===")
            print("1. Show my habits")
            print("2. Tick off a habit")
            print("3. Create a habit")
            print("4. Change a habit")
            print("5. Delete a habit")
            print("6. Analytics")
            print("0. Exit")
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye!")
                break
            action = actions.get(choice)
            if action is None:
                print("Please enter a number from the menu.")
            else:
                action()

    # ----- helpers that ask the user for input -----

    def _choose_habit(self):
        """Let the user pick a habit by its list number. Returns None if cancelled."""
        habits = self.manager.habits
        if not habits:
            print("You have no habits yet.")
            return None
        for number, habit in enumerate(habits, start=1):
            print(f"{number}. {habit.name} ({habit.period}, {habit.category})")
        choice = input("Number of the habit (Enter to cancel): ").strip()
        if not choice:
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(habits):
            return habits[int(choice) - 1]
        print("That number is not in the list.")
        return None

    def _choose_period(self):
        """Let the user pick a period. Returns None if the choice is invalid."""
        for number, period in enumerate(VALID_PERIODS, start=1):
            print(f"{number}. {period}")
        choice = input("Choose the period: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(VALID_PERIODS):
            return VALID_PERIODS[int(choice) - 1]
        print("Invalid choice.")
        return None

    def _ask_category(self, prompt):
        """Ask for a category. Returns None if the answer is empty."""
        category = input(prompt).strip()
        if not category:
            print("Category must not be empty.")
            return None
        return category

    # ----- main menu actions -----

    def show_habits(self):
        """Print all habits with their longest streak."""
        habits = self.manager.habits
        if not habits:
            print("You have no habits yet.")
            return
        today = datetime.now()
        for number, habit in enumerate(habits, start=1):
            streak = analytics.longest_streak(habit, today)
            print(
                f"{number}. {habit.name} | {habit.period} | {habit.category} "
                f"| longest streak: {streak} {UNITS[habit.period]}"
            )

    def tick_off_habit(self):
        """Tick off the chosen habit for the current cycle."""
        habit = self._choose_habit()
        if habit is None:
            return
        if self.manager.tick_off(habit):
            print(f"'{habit.name}' ticked off. Well done!")
        else:
            print(f"'{habit.name}' is already done for the current {habit.period} cycle.")

    def create_habit(self):
        """Ask for name, period and category and create a habit."""
        name = input("Name of the new habit: ")
        period = self._choose_period()
        if period is None:
            return
        category = self._ask_category("Category: ")
        if category is None:
            return
        try:
            habit = self.manager.create_habit(name, period, category)
        except ValueError as error:
            print(f"Could not create the habit: {error}")
        else:
            print(f"Habit '{habit.name}' created.")

    def change_habit(self):
        """Rename a habit or change its period or category."""
        habit = self._choose_habit()
        if habit is None:
            return
        print("1. Rename")
        print("2. Change period")
        print("3. Change category")
        choice = input("What do you want to change? ").strip()
        try:
            if choice == "1":
                self.manager.rename_habit(habit, input("New name: "))
            elif choice == "2":
                period = self._choose_period()
                if period is None:
                    return
                self.manager.change_period(habit, period)
            elif choice == "3":
                category = self._ask_category("New category: ")
                if category is None:
                    return
                self.manager.change_category(habit, category)
            else:
                print("Invalid choice.")
                return
        except ValueError as error:
            print(f"Could not change the habit: {error}")
        else:
            print("Habit updated.")

    def delete_habit(self):
        """Delete the chosen habit after a confirmation."""
        habit = self._choose_habit()
        if habit is None:
            return
        answer = input(f"Really delete '{habit.name}' and its history? (y/n): ")
        if answer.strip().lower() == "y":
            self.manager.delete_habit(habit)
            print("Habit deleted.")
        else:
            print("Nothing was deleted.")

    # ----- analytics submenu -----

    def show_analytics(self):
        """Show the analytics options and print the chosen result."""
        print("\n--- Analytics ---")
        print("1. List all habits")
        print("2. List habits with the same period")
        print("3. Longest streak of all habits")
        print("4. Longest streak of one habit")
        print("5. Consistency of one habit")
        choice = input("Choose an option: ").strip()
        habits = self.manager.habits
        today = datetime.now()
        if choice == "1":
            names = analytics.list_habit_names(habits)
            print(", ".join(names) if names else "No habits.")
        elif choice == "2":
            period = self._choose_period()
            if period is not None:
                matching = analytics.habits_with_period(habits, period)
                names = analytics.list_habit_names(matching)
                print(", ".join(names) if names else f"No {period} habits.")
        elif choice == "3":
            best = analytics.habit_with_longest_streak(habits, today)
            if best is None:
                print("No habits.")
            else:
                streak = analytics.longest_streak(best, today)
                print(f"'{best.name}' has the longest streak: {streak} {UNITS[best.period]}.")
        elif choice == "4":
            habit = self._choose_habit()
            if habit is not None:
                streak = analytics.longest_streak(habit, today)
                print(f"Longest streak of '{habit.name}': {streak} {UNITS[habit.period]}.")
        elif choice == "5":
            habit = self._choose_habit()
            if habit is not None:
                days = input("Over how many days? ").strip()
                if not days.isdigit() or int(days) < 1:
                    print("Please enter a whole number of days.")
                else:
                    rate = analytics.consistency(habit, today, int(days))
                    if rate is None:
                        print("Not enough data: no complete cycle fits in this window.")
                    else:
                        print(f"Consistency of '{habit.name}': {rate:.0%}")
        else:
            print("Invalid choice.")