"""Analytics functions: streaks, consistency and habit filters."""


def list_habit_names(habits):
    """Return the names of all given habits."""
    return list(map(lambda habit: habit.name, habits))


def habits_with_period(habits, period):
    """Return only the habits that have the given period."""
    return list(filter(lambda habit: habit.period == period, habits))