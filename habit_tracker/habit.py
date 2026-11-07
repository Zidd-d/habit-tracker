"""The Habit class: one habit with its period, category and completions."""

from datetime import datetime

VALID_PERIODS = ("daily", "weekly", "monthly")


class Habit:
    """A habit that is repeated every day, week or month.

    It stores its name, period, category, creation time and the
    timestamps of all completions.
    """

    def __init__(self, name, period, category, creation_time=None, habit_id=None):
        self.name = name
        self.period = period
        self.category = category
        # Without a given creation time (new habit), use the current time.
        self.creation_time = creation_time if creation_time is not None else datetime.now()
        # None until the repository saves the habit and the database assigns an ID.
        self.habit_id = habit_id
        self.completions = []

    def cycle_key(self, moment):
        """Return a label that is equal for all moments in the same cycle."""
        if self.period == "daily":
            return moment.date()
        if self.period == "weekly":
            # ISO weeks run from Monday to Sunday.
            year, week, _ = moment.isocalendar()
            return (year, week)
        if self.period == "monthly":
            return (moment.year, moment.month)
        raise ValueError(f"Unknown period: {self.period}")

    def tick_off(self, time=None):
        """Record a completion in the current cycle.

        Returns True if it was recorded, False if the time is in the
        future, outside the current cycle, or the cycle is already done.
        """
        now = datetime.now()
        if time is None:
            time = now
        if time > now:
            return False
        if self.cycle_key(time) != self.cycle_key(now):
            return False
        for done in self.completions:
            if self.cycle_key(done) == self.cycle_key(now):
                return False
        self.completions.append(time)
        return True

    def rename(self, new_name):
        """Change the name of the habit. The name must not be empty."""
        if not new_name.strip():
            raise ValueError("Name must not be empty")
        self.name = new_name.strip()

    def change_period(self, new_period):
        """Change the period. History is kept, so streaks can change."""
        if new_period not in VALID_PERIODS:
            raise ValueError(f"Period must be one of {VALID_PERIODS}")
        self.period = new_period

    def change_category(self, new_category):
        """Change the category of the habit."""
        self.category = new_category