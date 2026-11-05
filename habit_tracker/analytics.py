"""Analytics functions: streaks, consistency and habit filters."""

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
    done = {habit.cycle_key(time) for time in habit.completions}
    keys = [habit.cycle_key(moment) for moment in _cycle_moments(habit, today)]
    if keys and keys[-1] not in done:
        keys = keys[:-1]
    flags = [key in done for key in keys]
    runs = [len(list(group)) for value, group in groupby(flags) if value]
    return max(runs, default=0)


def habit_with_longest_streak(habits, today):
    """Return the habit with the longest streak, or None if there are no habits."""
    return max(habits, key=lambda habit: longest_streak(habit, today), default=None)

