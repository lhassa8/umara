"""
Connection management for Umara.

Provides a unified interface for connecting to databases, APIs, and cloud services.
Connections are automatically cached and managed for optimal performance.
"""

from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class BaseConnection(ABC):
    """
    Base class for all connection types.

    Subclass this to create custom connection types for databases,
    APIs, or cloud services.
    """

    def __init__(self, connection_name: str, **kwargs):
        self._connection_name = connection_name
        self._kwargs = kwargs
        self._connection: Any = None
        self._lock = threading.RLock()

    @abstractmethod
    def _connect(self) -> Any:
        """Establish the connection. Override in subclasses."""
        pass

    def reset(self) -> None:
        """Reset/close the connection."""
        with self._lock:
            if self._connection is not None:
                try:
                    if hasattr(self._connection, "close"):
                        self._connection.close()
                except Exception:
                    pass
                self._connection = None

    def _get_connection(self) -> Any:
        """Get or create the connection."""
        with self._lock:
            if self._connection is None:
                self._connection = self._connect()
            return self._connection


class SQLConnection(BaseConnection):
    """
    SQL database connection.

    Supports SQLite, PostgreSQL, MySQL, and other databases via their
    respective Python drivers.

    Example:
        conn = um.connection.sql("my_db", url="sqlite:///data.db")
        df = conn.query("SELECT * FROM users")
    """

    def _connect(self) -> Any:
        """Connect to SQL database."""
        url = self._kwargs.get("url")
        if not url:
            raise ValueError("SQL connection requires 'url' parameter")

        # Try sqlalchemy first
        try:
            from sqlalchemy import create_engine

            engine = create_engine(url, **{k: v for k, v in self._kwargs.items() if k != "url"})
            return engine
        except ImportError:
            pass

        # Fallback to sqlite3 for sqlite URLs
        if url.startswith("sqlite"):
            import sqlite3

            db_path = url.replace("sqlite:///", "").replace("sqlite://", "")
            return sqlite3.connect(db_path, check_same_thread=False)

        raise ImportError(
            "SQL connections require sqlalchemy. Install with: pip install sqlalchemy"
        )

    def query(self, sql: str, params: dict | tuple | None = None, ttl: int | None = None) -> Any:
        """
        Execute a SQL query and return results.

        Args:
            sql: SQL query string
            params: Query parameters (dict for named, tuple for positional)
            ttl: Cache TTL in seconds (None = no caching)

        Returns:
            Query results as a list of dicts, or DataFrame if pandas is available
        """
        conn = self._get_connection()

        # Try pandas for nice DataFrame output
        try:
            import pandas as pd

            if hasattr(conn, "execute"):
                # SQLAlchemy engine
                with conn.connect() as connection:
                    return pd.read_sql(sql, connection, params=params)
            else:
                # sqlite3 connection
                return pd.read_sql(sql, conn, params=params)
        except ImportError:
            pass

        # Fallback to raw execution
        if hasattr(conn, "execute"):
            # SQLAlchemy
            with conn.connect() as connection:
                result = connection.execute(sql, params or {})
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result.fetchall()]
        else:
            # sqlite3
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def execute(self, sql: str, params: dict | tuple | None = None) -> None:
        """Execute a SQL statement (INSERT, UPDATE, DELETE, etc.)."""
        conn = self._get_connection()

        if hasattr(conn, "execute"):
            # SQLAlchemy
            with conn.connect() as connection:
                connection.execute(sql, params or {})
                connection.commit()
        else:
            # sqlite3
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            conn.commit()


class HTTPConnection(BaseConnection):
    """
    HTTP/REST API connection.

    Provides a simple interface for making HTTP requests to REST APIs.

    Example:
        api = um.connection.http("github_api", base_url="https://api.github.com")
        repos = api.get("/users/anthropics/repos")
    """

    def _connect(self) -> Any:
        """Initialize HTTP session."""
        try:
            import httpx

            base_url = self._kwargs.get("base_url", "")
            headers = self._kwargs.get("headers", {})
            timeout = self._kwargs.get("timeout", 30)
            return httpx.Client(base_url=base_url, headers=headers, timeout=timeout)
        except ImportError:
            pass

        try:
            import requests

            return requests.Session()
        except ImportError:
            pass

        raise ImportError(
            "HTTP connections require httpx or requests. "
            "Install with: pip install httpx"
        )

    def _make_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        base_url = self._kwargs.get("base_url", "")
        if base_url and not endpoint.startswith("http"):
            return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return endpoint

    def get(self, endpoint: str, params: dict | None = None, **kwargs) -> Any:
        """Make GET request."""
        session = self._get_connection()
        url = self._make_url(endpoint)

        # Check if httpx or requests
        if hasattr(session, "get"):
            response = session.get(url, params=params, **kwargs)
            response.raise_for_status()
            return response.json()

    def post(self, endpoint: str, data: dict | None = None, json: dict | None = None, **kwargs) -> Any:
        """Make POST request."""
        session = self._get_connection()
        url = self._make_url(endpoint)
        response = session.post(url, data=data, json=json, **kwargs)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict | None = None, json: dict | None = None, **kwargs) -> Any:
        """Make PUT request."""
        session = self._get_connection()
        url = self._make_url(endpoint)
        response = session.put(url, data=data, json=json, **kwargs)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str, **kwargs) -> Any:
        """Make DELETE request."""
        session = self._get_connection()
        url = self._make_url(endpoint)
        response = session.delete(url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else None


class SnowflakeConnection(BaseConnection):
    """Snowflake data warehouse connection."""

    def _connect(self) -> Any:
        try:
            import snowflake.connector

            return snowflake.connector.connect(
                account=self._kwargs.get("account"),
                user=self._kwargs.get("user"),
                password=self._kwargs.get("password"),
                warehouse=self._kwargs.get("warehouse"),
                database=self._kwargs.get("database"),
                schema=self._kwargs.get("schema"),
            )
        except ImportError:
            raise ImportError(
                "Snowflake connections require snowflake-connector-python. "
                "Install with: pip install snowflake-connector-python"
            )

    def query(self, sql: str, params: dict | None = None) -> Any:
        """Execute query and return results."""
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            # Try pandas
            try:
                import pandas as pd

                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(cursor.fetchall(), columns=columns)
            except ImportError:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        finally:
            cursor.close()


# Connection registry
_connections: dict[str, BaseConnection] = {}
_connection_lock = threading.RLock()


class ConnectionManager:
    """
    Connection manager that provides access to different connection types.

    Example:
        # SQL database
        conn = um.connection.sql("my_db", url="sqlite:///app.db")
        data = conn.query("SELECT * FROM users")

        # REST API
        api = um.connection.http("github", base_url="https://api.github.com")
        repos = api.get("/users/octocat/repos")
    """

    def sql(
        self,
        connection_name: str,
        *,
        url: str | None = None,
        **kwargs,
    ) -> SQLConnection:
        """
        Get or create a SQL database connection.

        Args:
            connection_name: Unique name for this connection
            url: Database URL (e.g., "sqlite:///app.db", "postgresql://...")
            **kwargs: Additional connection parameters

        Returns:
            SQLConnection instance
        """
        with _connection_lock:
            key = f"sql:{connection_name}"
            if key not in _connections:
                _connections[key] = SQLConnection(connection_name, url=url, **kwargs)
            return _connections[key]  # type: ignore

    def http(
        self,
        connection_name: str,
        *,
        base_url: str = "",
        headers: dict | None = None,
        timeout: int = 30,
        **kwargs,
    ) -> HTTPConnection:
        """
        Get or create an HTTP/REST API connection.

        Args:
            connection_name: Unique name for this connection
            base_url: Base URL for all requests
            headers: Default headers to include
            timeout: Request timeout in seconds
            **kwargs: Additional connection parameters

        Returns:
            HTTPConnection instance
        """
        with _connection_lock:
            key = f"http:{connection_name}"
            if key not in _connections:
                _connections[key] = HTTPConnection(
                    connection_name,
                    base_url=base_url,
                    headers=headers or {},
                    timeout=timeout,
                    **kwargs,
                )
            return _connections[key]  # type: ignore

    def snowflake(
        self,
        connection_name: str,
        *,
        account: str | None = None,
        user: str | None = None,
        password: str | None = None,
        warehouse: str | None = None,
        database: str | None = None,
        schema: str | None = None,
        **kwargs,
    ) -> SnowflakeConnection:
        """
        Get or create a Snowflake connection.

        Args:
            connection_name: Unique name for this connection
            account: Snowflake account identifier
            user: Username
            password: Password
            warehouse: Warehouse name
            database: Database name
            schema: Schema name

        Returns:
            SnowflakeConnection instance
        """
        with _connection_lock:
            key = f"snowflake:{connection_name}"
            if key not in _connections:
                _connections[key] = SnowflakeConnection(
                    connection_name,
                    account=account,
                    user=user,
                    password=password,
                    warehouse=warehouse,
                    database=database,
                    schema=schema,
                    **kwargs,
                )
            return _connections[key]  # type: ignore

    def reset(self, connection_name: str | None = None) -> None:
        """
        Reset connections.

        Args:
            connection_name: Specific connection to reset, or None to reset all
        """
        with _connection_lock:
            if connection_name:
                # Reset specific connection
                keys_to_reset = [k for k in _connections if connection_name in k]
                for key in keys_to_reset:
                    _connections[key].reset()
                    del _connections[key]
            else:
                # Reset all
                for conn in _connections.values():
                    conn.reset()
                _connections.clear()


# Global connection manager instance
connection = ConnectionManager()
