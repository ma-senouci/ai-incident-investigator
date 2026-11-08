from __future__ import annotations

import sqlite3
from typing import Any


class DatabaseManager:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._connection: sqlite3.Connection | None = None

    @property
    def db_path(self) -> str:
        return self._db_path

    def connect(self) -> None:
        if self._connection is not None:
            return
        self._connection = sqlite3.connect(self._db_path)
        self._connection.row_factory = sqlite3.Row

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    @property
    def connection(self) -> sqlite3.Connection:
        if self._connection is None:
            raise RuntimeError("DatabaseManager is not connected. Call connect() first.")
        return self._connection

    def execute_query(self, sql: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        cursor = self.connection.execute(sql, params)
        return cursor.fetchall()

    def execute_update(self, sql: str, params: tuple[Any, ...] = ()) -> int:
        cursor = self.connection.execute(sql, params)
        self.connection.commit()
        return cursor.rowcount

    def execute_script(self, sql: str) -> None:
        self.connection.executescript(sql)

    def __enter__(self) -> DatabaseManager:
        self.connect()
        return self

    def __exit__(self, exc_type: type | None, exc_val: Exception | None, exc_tb: Any) -> None:
        self.close()
