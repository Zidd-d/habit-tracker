"""Analytics functions: streaks, consistency and habit filters.

All functions are pure: they only read the habits they are given and never
change them or touch the database. `today` is a parameter, which makes the
results easy to test.
"""

from datetime import timedelta
from itertools import groupby


def list_habit_names(habits):
    """Return the names of all given habits."""
    return list(map(lambda habit: habit.name, habits))


def habits_with_period(habits, period):
    """Return only the habits that have the given period."""
    return list(filter(lambda habit: habit.period == period, habits))


def _next_cycle_moment(moment, period):
    """Return a moment that lies in the cycle after the one of `moment`."""
    if period == "daily":
        return moment + timedelta(days=1)
    if period == "weekly":
        return moment + timedelta(weeks=1)
    # Monthly: jump to the 1st of the next month (December -> January, next year).
    year = moment.year + moment.month // 12
    month = moment.month % 12 + 1
    return moment.replace(year=year, month=month, day=1)


def _cycle_moments(habit, today):
    """Return one moment per cycle, from creation up to the cycle of today."""
    moments = []
    moment = habit.creation_time
    while habit.cycle_key(moment) <= habit.cycle_key(today):
        moments.append(moment)
        moment = _next_cycle_moment(moment, habit.period)
    return moments


def longest_streak(habit, today):
    """Return the longest streak of consecutive completed cycles."""
    # Labels of all cycles in which the habit was ticked off at least once.
    done = {habit.cycle_key(time) for time in habit.completions}
    # One label per cycle, from the creation of the habit to the current cycle.
    keys = [habit.cycle_key(moment) for moment in _cycle_moments(habit, today)]
    # The current cycle is still open, so it must not count as missed.
    if keys and keys[-1] not in done:
        keys = keys[:-1]
    # True = cycle completed, False = cycle missed.
    flags = [key in done for key in keys]
    # Lengths of all runs of consecutive True values.
    runs = [len(list(group)) for value, group in groupby(flags) if value]
    return max(runs, default=0)


def habit_with_longest_streak(habits, today):
    """Return the habit with the longest streak, or None if there are no habits."""
    return max(habits, key=lambda habit: longest_streak(habit, today), default=None)


def _cycle_bounds(moment, period):
    """Return the first and last day (as dates) of the cycle containing moment."""
    day = moment.date()
    if period == "daily":
        return day, day
    if period == "weekly":
        # weekday() is 0 for Monday, so this is the Monday of that week.
        start = day - timedelta(days=day.weekday())
        return start, start + timedelta(days=6)
    start = day.replace(day=1)
    # Day 28 plus 4 days always lands in the next month; its 1st is the next start.
    next_month_start = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
    return start, next_month_start - timedelta(days=1)


def consistency(habit, today, window_days):
    """Return the share of completed cycles in the last window_days days.

    Only cycles that lie fully inside the window and are already finished
    count. Returns None if no such cycle exists.
    """
    if window_days < 1:
        raise ValueError("The window must be at least one day")
    window_start = today.date() - timedelta(days=window_days - 1)

    def counts(moment):
        # A cycle counts if it starts inside the window and ended before today.
        first_day, last_day = _cycle_bounds(moment, habit.period)
        return first_day >= window_start and last_day < today.date()

    cycles = list(filter(counts, _cycle_moments(habit, today)))
    if not cycles:
        return None
    done = {habit.cycle_key(time) for time in habit.completions}
    completed = [moment for moment in cycles if habit.cycle_key(moment) in done]
    return len(completed) / len(cycles)