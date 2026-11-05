"""The HabitRepository class: all SQLite access, saving and loading habits."""

import os
import sqlite3
from datetime import datetime

from habit_tracker.habit import Habit


class HabitRepository:
    """Saves and loads habits in an SQLite database."""

    def __init__(self, db_path):
        self.first_start = db_path == ":memory:" or not os.path.exists(db_path)
        if db_path != ":memory:":
            folder = os.path.dirname(db_path)
            if folder:
                os.makedirs(folder, exist_ok=True)
        self.connection = sqlite3.connect(db_path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._create_tables()

    def _create_tables(self):
        """Create both tables if they do not exist yet."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS Habit (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                period TEXT NOT NULL,
                category TEXT NOT NULL,
                creation_time TEXT NOT NULL
            )""")
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS HabitCompletion (
                time_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES Habit (habit_id) ON DELETE CASCADE
            )""")
        self.connection.commit()

    def save_habit(self, habit):
        """Insert a new habit or update an existing one, with its completions."""
        if habit.habit_id is None:
            cursor = self.connection.execute(
                "INSERT INTO Habit (name, period, category, creation_time) "
                "VALUES (?, ?, ?, ?)",
                (habit.name, habit.period, habit.category,
                 habit.creation_time.isoformat()),
            )
            habit.habit_id = cursor.lastrowid
        else:
            self.connection.execute(
                "UPDATE Habit SET name = ?, period = ?, category = ?, "
                "creation_time = ? WHERE habit_id = ?",
                (habit.name, habit.period, habit.category,
                 habit.creation_time.isoformat(), habit.habit_id),
            )
        self.connection.execute(
            "DELETE FROM HabitCompletion WHERE habit_id = ?", (habit.habit_id,)
        )
        self.connection.executemany(
            "INSERT INTO HabitCompletion (habit_id, timestamp) VALUES (?, ?)",
            [(habit.habit_id, time.isoformat()) for time in habit.completions],
        )
        self.connection.commit()

    def load_habits(self):
        """Return all saved habits as Habit objects."""
        habits = []
        rows = self.connection.execute(
            "SELECT habit_id, name, period, category, creation_time "
            "FROM Habit ORDER BY habit_id"
        ).fetchall()
        for habit_id, name, period, category, creation_time in rows:
            habit = Habit(name, period, category,
                          datetime.fromisoformat(creation_time), habit_id)
            timestamps = self.connection.execute(
                "SELECT timestamp FROM HabitCompletion "
                "WHERE habit_id = ? ORDER BY timestamp",
                (habit_id,),
            ).fetchall()
            habit.completions = [datetime.fromisoformat(row[0]) for row in timestamps]
            habits.append(habit)
        return habits

    def delete_habit(self, habit):
        """Delete a habit; its completions are deleted with it."""
        self.connection.execute(
            "DELETE FROM Habit WHERE habit_id = ?", (habit.habit_id,)
        )
        self.connection.commit()

    def close(self):
        """Close the database connection."""
        self.connection.close()