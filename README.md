
# Habit tracker

A command-line habit tracker written in Python. You can create daily, weekly
and monthly habits, tick them off, and analyse your streaks and consistency.
All data is saved in a local SQLite database, so it is still there the next
time you start the program.

## Features

- Five predefined habits to start with, plus your own habits with categories
- Daily, weekly and monthly habits (a week runs Monday to Sunday, a month is a calendar month)
- Tick off a habit once per cycle
- Rename a habit or change its period or category (the history is kept)
- Delete a habit with a confirmation
- Analytics: list all habits, list habits with the same period, longest streak
  of all habits, longest streak of one habit, and consistency over a chosen
  number of days

## Requirements

- Python 3.7 or newer (developed with Python 3.12)
- No extra packages are needed to run the program. `pytest` is only needed to run the tests.

## Installation

1. Download the project from GitHub:

   ```
   git clone https://github.com/Zidd-d/habit-tracker.git
   cd habit-tracker
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv .venv
   .venv\Scripts\activate          # Windows (PowerShell)
   source .venv/bin/activate       # macOS / Linux
   ```

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

## Run the program

```
python main.py
```

You will see a menu. Type the number of an option and press Enter.

| Option | What it does |
|---|---|
| 1 | Show all habits with their longest streak |
| 2 | Tick off a habit for the current day, week or month |
| 3 | Create a new habit (name, period, category) |
| 4 | Rename a habit or change its period or category |
| 5 | Delete a habit |
| 6 | Analytics (see below) |
| 0 | Exit |

Analytics menu:

1. List all habits
2. List habits with the same period
3. Longest streak of all habits
4. Longest streak of one habit
5. Consistency of one habit over a number of days

## How streaks and consistency are counted

- A habit is "done" in a cycle if it was ticked off at least once in that cycle.
- A streak is the number of completed cycles in a row, counted from the day the habit was created.
- The current cycle is not counted as missed while it is still open.
- Consistency is the share of completed cycles in the last N days. Only
  cycles that lie fully inside the window and are already finished are
  counted. If no cycle fits, the program says there is not enough data.
- If you change a habit's period, the new period is applied to its whole history.

## Where the data is stored

The database file is created automatically at `data/habits.db` when you start
the program for the first time. To start again with a clean database, close
the program and delete that file.

## Run the tests

```
pytest
```

The tests use four weeks of hand-written example data for the five predefined
habits (`tests/example_data.py`).

## Project structure

```
habit_tracker_phase2/
  habit_tracker/
    habit.py                 Habit class (data and tick-off rules)
    habit_manager.py         Creates, changes, deletes and ticks off habits
    habit_repository.py      All SQLite access
    analytics.py             Streaks, consistency and filters (functional style)
    menu.py                  Command-line menu
    predefined_habits.py     The five starting habits
  tests/                     pytest tests and example data
  main.py                    Start the program here
  requirements.txt
```