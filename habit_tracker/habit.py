"""The Habit class: one habit with its period, category and completions."""

from datetime import datetime


class Habit:
    """A habit that is repeated every day, week or month.

    It stores its name, period, category, creation time and the
    timestamps of all completions."""
    def __init__(self, name, period, category, creation_time=None, habit_id=None):
        self.name = name
        self.period = period
        self.category = category
        self.creation_time = creation_time if creation_time is not None else datetime.now()
        self.habit_id = habit_id
        self.completions = []

    def _cycle_key(self, moment):
        """Return a label that is equal for all moments in the same cycle."""
        if self.period == "daily":
            return moment.date()
        if self.period == "weekly":
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
        if self._cycle_key(time) != self._cycle_key(now):
            return False
        for done in self.completions:
            if self._cycle_key(done) == self._cycle_key(now):
                return False
        self.completions.append(time)
        return True
