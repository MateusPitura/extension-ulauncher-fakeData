import os
import sqlite3
import time
from src.utils.get_preferences_path import get_preferences_path


class GeneratorRepository:
    def __init__(self, dirname):
        db_path = f'{get_preferences_path(dirname)}/data.db'
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS generators (
            name TEXT PRIMARY KEY,
            last_used INTEGER
        )
        """)

        self.conn.commit()

    def mark_as_used(self, name):
        self.cursor.execute("""
            INSERT INTO generators (name, last_used)
            VALUES (?, ?)
            ON CONFLICT(name)
            DO UPDATE SET last_used=excluded.last_used
        """, (name, int(time.time())))

        self.conn.commit()

    def get_items(self):
        self.cursor.execute("""
            SELECT name
            FROM generators
            ORDER BY last_used DESC
        """)

        return [row[0] for row in self.cursor.fetchall()]
