from __future__ import annotations

from pathlib import Path

import pytest

from incident_investigator.database import DatabaseManager


class TestDatabaseManagerConnect:
    def test_connect_opens_in_memory(self) -> None:
        with DatabaseManager(":memory:") as db:
            assert db.connection is not None

    def test_connect_is_idempotent(self) -> None:
        with DatabaseManager(":memory:") as db:
            conn = db.connection
            db.connect()
            assert db.connection is conn

    def test_connection_raises_when_not_connected(self) -> None:
        db = DatabaseManager(":memory:")
        with pytest.raises(RuntimeError, match="not connected"):
            _ = db.connection

    def test_close_allows_reconnect(self) -> None:
        db = DatabaseManager(":memory:")
        db.connect()
        db.close()
        db.connect()
        assert db.connection is not None
        db.close()


class TestDatabaseManagerQueries:
    def test_execute_query_returns_rows(self) -> None:
        with DatabaseManager(":memory:") as db:
            db.execute_script("CREATE TABLE t (id INTEGER, val TEXT);")
            db.connection.execute("INSERT INTO t VALUES (1, 'a'), (2, 'b')")
            rows = db.execute_query("SELECT * FROM t WHERE id = ?", (1,))
            assert len(rows) == 1
            assert rows[0]["val"] == "a"

    def test_execute_query_empty_result(self) -> None:
        with DatabaseManager(":memory:") as db:
            db.execute_script("CREATE TABLE t (id INTEGER);")
            rows = db.execute_query("SELECT * FROM t")
            assert rows == []

    def test_execute_update_returns_rowcount(self) -> None:
        with DatabaseManager(":memory:") as db:
            db.execute_script("CREATE TABLE t (id INTEGER);")
            db.connection.execute("INSERT INTO t VALUES (1), (2), (3)")
            db.connection.commit()
            count = db.execute_update("DELETE FROM t WHERE id > ?", (1,))
            assert count == 2

    def test_execute_script_creates_tables(self) -> None:
        with DatabaseManager(":memory:") as db:
            db.execute_script("CREATE TABLE a (x INTEGER); CREATE TABLE b (y TEXT);")
            db.execute_query("SELECT * FROM a")
            db.execute_query("SELECT * FROM b")


class TestDatabaseManagerFileBacked:
    def test_file_backed_persistence(self, tmp_path: Path) -> None:
        db_path = str(tmp_path / "test.db")
        with DatabaseManager(db_path) as db:
            db.execute_script("CREATE TABLE t (v INTEGER);")
            db.connection.execute("INSERT INTO t VALUES (42)")
            db.connection.commit()

        with DatabaseManager(db_path) as db:
            rows = db.execute_query("SELECT v FROM t")
            assert rows[0]["v"] == 42
