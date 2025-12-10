"""
Connection Helpers for Umara.

Provides decorators and utilities for managing database connections,
API clients, and other external resources. Connections are automatically
cached and shared across reruns.

Example:
    import umara as um
    from umara.connections import connection

    @connection
    def get_db():
        return sqlite3.connect("app.db")

    # Connection is cached and reused
    db = get_db()
    results = db.execute("SELECT * FROM users").fetchall()
"""

from __future__ import annotations

import functools
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar, ParamSpec, Generic, Generator

from umara.cache import cache_resource

P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class ConnectionInfo:
    """Information about a connection."""

    name: str
    created_at: float
    last_used: float
    use_count: int = 0
    is_active: bool = True
    error: Exception | None = None


class ConnectionManager:
    """Manages connection lifecycle and pooling."""

    _instance: "ConnectionManager | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "ConnectionManager":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._connections: dict[str, Any] = {}
                cls._instance._info: dict[str, ConnectionInfo] = {}
                cls._instance._cleanups: dict[str, Callable] = {}
                cls._instance._cm_lock = threading.RLock()
            return cls._instance

    def register(
        self,
        name: str,
        conn: Any,
        cleanup: Callable[[], None] | None = None,
    ) -> None:
        """Register a connection."""
        with self._cm_lock:
            self._connections[name] = conn
            self._info[name] = ConnectionInfo(
                name=name,
                created_at=time.time(),
                last_used=time.time(),
            )
            if cleanup:
                self._cleanups[name] = cleanup

    def get(self, name: str) -> Any | None:
        """Get a connection by name."""
        with self._cm_lock:
            if name in self._connections:
                info = self._info[name]
                info.last_used = time.time()
                info.use_count += 1
                return self._connections[name]
            return None

    def close(self, name: str) -> bool:
        """Close and remove a connection."""
        with self._cm_lock:
            if name in self._connections:
                # Run cleanup if registered
                if name in self._cleanups:
                    try:
                        self._cleanups[name]()
                    except Exception:
                        pass
                    del self._cleanups[name]

                del self._connections[name]
                if name in self._info:
                    self._info[name].is_active = False
                return True
            return False

    def close_all(self) -> int:
        """Close all connections."""
        closed = 0
        with self._cm_lock:
            names = list(self._connections.keys())
            for name in names:
                if self.close(name):
                    closed += 1
        return closed

    def get_info(self, name: str) -> ConnectionInfo | None:
        """Get connection info."""
        return self._info.get(name)

    def list_connections(self) -> list[str]:
        """List all connection names."""
        return list(self._connections.keys())

    def get_all_info(self) -> dict[str, dict[str, Any]]:
        """Get info for all connections."""
        return {
            name: {
                "created_at": info.created_at,
                "last_used": info.last_used,
                "use_count": info.use_count,
                "is_active": info.is_active,
                "age_seconds": time.time() - info.created_at,
            }
            for name, info in self._info.items()
        }


# Global connection manager
_manager = ConnectionManager()


def connection(
    func: Callable[P, R] | None = None,
    *,
    ttl: float | None = None,
    validate: Callable[[Any], bool] | None = None,
    cleanup: Callable[[Any], None] | None = None,
    name: str | None = None,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to create a cached connection.

    Connections are created once and reused across reruns.
    Use this for database connections, API clients, etc.

    Args:
        ttl: Time-to-live in seconds. None means no expiration.
        validate: Function to check if connection is still valid.
        cleanup: Function to clean up the connection when closed.
        name: Custom name for the connection.

    Returns:
        Decorated function with connection caching.

    Example:
        @connection
        def get_db():
            return sqlite3.connect("app.db")

        @connection(ttl=3600)
        def get_api_client():
            return APIClient(api_key=os.environ["API_KEY"])

        @connection(validate=lambda c: c.is_connected())
        def get_redis():
            return redis.Redis()
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        conn_name = name or f"conn:{fn.__module__}.{fn.__qualname__}"

        # Wrap with cache_resource for caching
        cached_fn = cache_resource(ttl=ttl, validate=validate)(fn)

        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Check if we already have it
            existing = _manager.get(conn_name)
            if existing is not None:
                return existing

            # Create new connection
            conn = cached_fn(*args, **kwargs)

            # Register with cleanup
            cleanup_fn = None
            if cleanup:
                cleanup_fn = lambda: cleanup(conn)
            elif hasattr(conn, "close"):
                cleanup_fn = conn.close

            _manager.register(conn_name, conn, cleanup_fn)
            return conn

        # Attach control methods
        wrapper.close = lambda: _manager.close(conn_name)  # type: ignore
        wrapper.info = lambda: _manager.get_info(conn_name)  # type: ignore
        wrapper.connection_name = conn_name  # type: ignore

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


# =============================================================================
# Specialized Connection Decorators
# =============================================================================


def sql_connection(
    connection_string: str | None = None,
    *,
    ttl: float | None = None,
    name: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for SQL database connections.

    Provides automatic connection validation and cleanup.

    Args:
        connection_string: Database connection string (can be passed to factory).
        ttl: Connection TTL in seconds.
        name: Connection name.

    Example:
        @sql_connection()
        def get_db():
            return sqlite3.connect("app.db")

        @sql_connection(ttl=3600)
        def get_postgres():
            return psycopg2.connect(os.environ["DATABASE_URL"])
    """

    def validate_sql(conn: Any) -> bool:
        """Check if SQL connection is still valid."""
        try:
            if hasattr(conn, "execute"):
                conn.execute("SELECT 1")
                return True
            if hasattr(conn, "cursor"):
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                return True
            return True
        except Exception:
            return False

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        return connection(fn, ttl=ttl, validate=validate_sql, name=name)

    return decorator


def api_connection(
    *,
    ttl: float = 3600,  # 1 hour default
    name: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for API client connections.

    Args:
        ttl: Connection TTL (default 1 hour).
        name: Connection name.

    Example:
        @api_connection()
        def get_openai():
            import openai
            return openai.OpenAI()

        @api_connection(ttl=7200)
        def get_anthropic():
            import anthropic
            return anthropic.Anthropic()
    """
    return connection(ttl=ttl, name=name)


# =============================================================================
# Context Manager for Temporary Connections
# =============================================================================


@contextmanager
def temp_connection(
    factory: Callable[[], R],
    cleanup: Callable[[R], None] | None = None,
) -> Generator[R, None, None]:
    """
    Context manager for temporary connections that are closed after use.

    Unlike @connection, this creates a new connection each time and
    ensures it's properly cleaned up.

    Args:
        factory: Function to create the connection.
        cleanup: Function to clean up the connection.

    Example:
        with temp_connection(lambda: sqlite3.connect(":memory:")) as conn:
            conn.execute("CREATE TABLE test (id INTEGER)")
            conn.execute("INSERT INTO test VALUES (1)")
        # Connection is automatically closed
    """
    conn = factory()
    try:
        yield conn
    finally:
        if cleanup:
            cleanup(conn)
        elif hasattr(conn, "close"):
            conn.close()


# =============================================================================
# Connection Pool
# =============================================================================


@dataclass
class ConnectionPool(Generic[R]):
    """
    Simple connection pool for managing multiple connections.

    Example:
        pool = ConnectionPool(
            factory=lambda: psycopg2.connect(DATABASE_URL),
            size=5
        )

        with pool.acquire() as conn:
            conn.execute("SELECT * FROM users")
    """

    factory: Callable[[], R]
    size: int = 5
    _pool: list[R] = field(default_factory=list)
    _in_use: set[int] = field(default_factory=set)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def __post_init__(self) -> None:
        # Pre-create connections
        for _ in range(self.size):
            self._pool.append(self.factory())

    @contextmanager
    def acquire(self) -> Generator[R, None, None]:
        """Acquire a connection from the pool."""
        conn = None
        idx = -1

        with self._lock:
            for i, c in enumerate(self._pool):
                if i not in self._in_use:
                    conn = c
                    idx = i
                    self._in_use.add(i)
                    break

        if conn is None:
            # No available connections, create temporary one
            conn = self.factory()
            try:
                yield conn
            finally:
                if hasattr(conn, "close"):
                    conn.close()
        else:
            try:
                yield conn
            finally:
                with self._lock:
                    self._in_use.discard(idx)

    def close_all(self) -> None:
        """Close all connections in the pool."""
        with self._lock:
            for conn in self._pool:
                if hasattr(conn, "close"):
                    try:
                        conn.close()
                    except Exception:
                        pass
            self._pool.clear()
            self._in_use.clear()

    @property
    def available(self) -> int:
        """Number of available connections."""
        with self._lock:
            return len(self._pool) - len(self._in_use)

    @property
    def in_use(self) -> int:
        """Number of connections in use."""
        with self._lock:
            return len(self._in_use)


# =============================================================================
# Utility Functions
# =============================================================================


def close_connection(name: str) -> bool:
    """Close a connection by name."""
    return _manager.close(name)


def close_all_connections() -> int:
    """Close all managed connections."""
    return _manager.close_all()


def list_connections() -> list[str]:
    """List all connection names."""
    return _manager.list_connections()


def get_connection_info() -> dict[str, dict[str, Any]]:
    """Get info for all connections."""
    return _manager.get_all_info()


# =============================================================================
# AI-Specific Connection Helpers
# =============================================================================


def openai_client(
    *,
    api_key: str | None = None,
    ttl: float = 3600,
) -> Callable[[], Any]:
    """
    Create a cached OpenAI client connection.

    Args:
        api_key: API key (defaults to OPENAI_API_KEY env var).
        ttl: Connection TTL.

    Returns:
        Factory function that returns cached OpenAI client.

    Example:
        client = openai_client()()
        response = client.chat.completions.create(...)
    """

    @connection(ttl=ttl, name="openai_client")
    def factory() -> Any:
        import openai

        if api_key:
            return openai.OpenAI(api_key=api_key)
        return openai.OpenAI()

    return factory


def anthropic_client(
    *,
    api_key: str | None = None,
    ttl: float = 3600,
) -> Callable[[], Any]:
    """
    Create a cached Anthropic client connection.

    Args:
        api_key: API key (defaults to ANTHROPIC_API_KEY env var).
        ttl: Connection TTL.

    Returns:
        Factory function that returns cached Anthropic client.

    Example:
        client = anthropic_client()()
        response = client.messages.create(...)
    """

    @connection(ttl=ttl, name="anthropic_client")
    def factory() -> Any:
        import anthropic

        if api_key:
            return anthropic.Anthropic(api_key=api_key)
        return anthropic.Anthropic()

    return factory
