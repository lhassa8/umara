"""
Tests for the connections module.
"""

from __future__ import annotations

import threading
import time

import pytest

from umara.connections import (
    ConnectionInfo,
    ConnectionManager,
    ConnectionPool,
    close_all_connections,
    get_connection_info,
    list_connections,
    temp_connection,
)


class TestConnectionInfo:
    """Tests for ConnectionInfo dataclass."""

    def test_connection_info_creation(self):
        """Test creating connection info."""
        info = ConnectionInfo(
            name="test_conn",
            created_at=time.time(),
            last_used=time.time(),
        )
        assert info.name == "test_conn"
        assert info.use_count == 0
        assert info.is_active is True
        assert info.error is None

    def test_connection_info_with_values(self):
        """Test connection info with custom values."""
        info = ConnectionInfo(
            name="test",
            created_at=100.0,
            last_used=200.0,
            use_count=5,
            is_active=False,
        )
        assert info.created_at == 100.0
        assert info.last_used == 200.0
        assert info.use_count == 5
        assert info.is_active is False


class TestConnectionManager:
    """Tests for ConnectionManager singleton."""

    def test_singleton_pattern(self):
        """Test that ConnectionManager is a singleton."""
        manager1 = ConnectionManager()
        manager2 = ConnectionManager()
        assert manager1 is manager2

    def test_register_connection(self):
        """Test registering a connection."""
        manager = ConnectionManager()
        manager.register("test_conn_1", {"type": "mock"})

        conn = manager.get("test_conn_1")
        assert conn == {"type": "mock"}

    def test_get_connection_updates_stats(self):
        """Test that getting a connection updates stats."""
        manager = ConnectionManager()
        manager.register("stats_conn", "connection")

        # Get multiple times
        manager.get("stats_conn")
        manager.get("stats_conn")
        manager.get("stats_conn")

        info = manager.get_info("stats_conn")
        assert info.use_count == 3

    def test_get_nonexistent_connection(self):
        """Test getting a non-existent connection."""
        manager = ConnectionManager()
        assert manager.get("nonexistent_conn") is None

    def test_close_connection(self):
        """Test closing a connection."""
        manager = ConnectionManager()
        manager.register("close_test", "conn")

        result = manager.close("close_test")
        assert result is True

        # Should no longer be retrievable
        assert manager.get("close_test") is None

        # Info should show inactive
        info = manager.get_info("close_test")
        assert info.is_active is False

    def test_close_with_cleanup(self):
        """Test closing a connection with cleanup function."""
        manager = ConnectionManager()
        cleanup_called = []

        def cleanup():
            cleanup_called.append(True)

        manager.register("cleanup_conn", "conn", cleanup=cleanup)
        manager.close("cleanup_conn")

        assert len(cleanup_called) == 1

    def test_close_all(self):
        """Test closing all connections."""
        manager = ConnectionManager()
        manager.register("all_1", "conn1")
        manager.register("all_2", "conn2")

        closed = manager.close_all()
        assert closed >= 2

    def test_list_connections(self):
        """Test listing connections."""
        manager = ConnectionManager()
        manager.register("list_test_1", "conn")
        manager.register("list_test_2", "conn")

        connections = manager.list_connections()
        assert "list_test_1" in connections
        assert "list_test_2" in connections

    def test_get_all_info(self):
        """Test getting info for all connections."""
        manager = ConnectionManager()
        manager.register("info_test", "conn")

        all_info = manager.get_all_info()
        assert isinstance(all_info, dict)
        assert "info_test" in all_info
        assert "created_at" in all_info["info_test"]
        assert "use_count" in all_info["info_test"]
        assert "age_seconds" in all_info["info_test"]


class TestConnectionPool:
    """Tests for ConnectionPool."""

    def test_pool_creation(self):
        """Test creating a connection pool."""
        pool = ConnectionPool(factory=lambda: {"id": "conn"}, size=3)
        assert pool.size == 3
        assert pool.available == 3
        assert pool.in_use == 0

    def test_acquire_connection(self):
        """Test acquiring a connection from the pool."""
        pool = ConnectionPool(factory=lambda: {"type": "test"}, size=2)

        with pool.acquire() as conn:
            assert conn == {"type": "test"}
            assert pool.in_use == 1
            assert pool.available == 1

        # After context exit
        assert pool.in_use == 0
        assert pool.available == 2

    def test_pool_exhaustion(self):
        """Test behavior when pool is exhausted."""
        counter = {"value": 0}

        def factory():
            counter["value"] += 1
            return {"id": counter["value"]}

        pool = ConnectionPool(factory=factory, size=1)

        # First acquire from pool
        with pool.acquire() as conn1:
            assert conn1["id"] == 1
            # Pool exhausted, should create temp connection
            with pool.acquire() as conn2:
                assert conn2["id"] == 2  # New connection created

    def test_close_all_pool(self):
        """Test closing all connections in pool."""
        close_count = {"value": 0}

        class MockConn:
            def close(self):
                close_count["value"] += 1

        pool = ConnectionPool(factory=MockConn, size=3)
        pool.close_all()

        assert close_count["value"] == 3
        assert pool.available == 0


class TestTempConnection:
    """Tests for temp_connection context manager."""

    def test_temp_connection_basic(self):
        """Test basic temp connection usage."""
        with temp_connection(lambda: {"temp": True}) as conn:
            assert conn == {"temp": True}

    def test_temp_connection_with_cleanup(self):
        """Test temp connection with cleanup function."""
        cleaned = []

        def cleanup(conn):
            cleaned.append(conn)

        with temp_connection(lambda: "myconn", cleanup=cleanup) as conn:
            assert conn == "myconn"

        assert "myconn" in cleaned

    def test_temp_connection_auto_close(self):
        """Test temp connection auto-closes objects with close method."""

        class MockConnection:
            closed = False

            def close(self):
                self.closed = True

        with temp_connection(MockConnection) as conn:
            assert not conn.closed

        assert conn.closed


class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_list_connections_func(self):
        """Test list_connections utility function."""
        connections = list_connections()
        assert isinstance(connections, list)

    def test_get_connection_info_func(self):
        """Test get_connection_info utility function."""
        info = get_connection_info()
        assert isinstance(info, dict)

    def test_close_all_connections_func(self):
        """Test close_all_connections utility function."""
        manager = ConnectionManager()
        manager.register("util_close_test", "conn")

        closed = close_all_connections()
        assert isinstance(closed, int)


class TestThreadSafety:
    """Tests for thread safety of connection manager."""

    def test_concurrent_registration(self):
        """Test concurrent connection registration."""
        manager = ConnectionManager()
        errors = []

        def register_conn(i):
            try:
                manager.register(f"thread_test_{i}", f"conn_{i}")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=register_conn, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0

    def test_concurrent_get(self):
        """Test concurrent connection retrieval."""
        manager = ConnectionManager()
        manager.register("concurrent_get", "shared_conn")
        results = []
        errors = []

        def get_conn():
            try:
                conn = manager.get("concurrent_get")
                results.append(conn)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=get_conn) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert all(r == "shared_conn" for r in results)
