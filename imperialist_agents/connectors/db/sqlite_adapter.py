from __future__ import annotations
import sqlite3
from typing import Iterable, Any, List, Tuple
from pathlib import Path
from .base import Database

class SQLiteDB(Database):
    def __init__(self, url: str):
        # very small parser: sqlite:///path
        assert url.startswith("sqlite:///"), "Only sqlite URLs supported in demo"
        self.path = Path(url.replace("sqlite:///", "")).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)

    def execute(self, sql: str, params: Iterable[Any] | None = None) -> List[Tuple[Any, ...]]:
        cur = self.conn.cursor()
        cur.execute(sql, params or [])
        self.conn.commit()
        try:
            rows = cur.fetchall()
        except sqlite3.ProgrammingError:
            rows = []
        return rows
