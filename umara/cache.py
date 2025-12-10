"""
Caching System for Umara.

Provides decorators and utilities for caching expensive operations,
particularly useful for AI applications where API calls are costly.

Advantages over Streamlit's @st.cache_data:
- TTL (time-to-live) support built-in
- LRU eviction for memory management
- Async function support
- Cache statistics and monitoring
- Manual cache invalidation
- Namespace isolation

Example:
    import umara as um
    from umara.cache import cache, cache_resource

    @cache(ttl=3600)  # Cache for 1 hour
    def fetch_embeddings(text: str) -> list[float]:
        return openai.embeddings.create(input=text).data[0].embedding

    @cache_resource
    def get_model():
        return load_expensive_model()
"""

from __future__ import annotations

import asyncio
import functools
import hashlib
import inspect
import json
import pickle
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar, ParamSpec, Generic

P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class CacheEntry:
    """A single cache entry with metadata."""

    value: Any
    created_at: float
    expires_at: float | None
    hits: int = 0
    size_bytes: int = 0

    @property
    def is_expired(self) -> bool:
        """Check if the entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def hit(self) -> Any:
        """Record a cache hit and return the value."""
        self.hits += 1
        return self.value


@dataclass
class CacheStats:
    """Statistics for a cache namespace."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    total_size_bytes: int = 0
    entry_count: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total

    def to_dict(self) -> dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
            "hit_rate": f"{self.hit_rate:.1%}",
            "total_size_bytes": self.total_size_bytes,
            "entry_count": self.entry_count,
        }


class CacheNamespace:
    """A namespace for cached values with LRU eviction."""

    def __init__(
        self,
        name: str,
        max_entries: int = 1000,
        max_size_bytes: int | None = None,
    ):
        self.name = name
        self.max_entries = max_entries
        self.max_size_bytes = max_size_bytes
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._stats = CacheStats()
        self._lock = threading.RLock()

    def get(self, key: str) -> tuple[bool, Any]:
        """
        Get a value from the cache.

        Returns:
            Tuple of (found, value). If not found, value is None.
        """
        with self._lock:
            entry = self._cache.get(key)

            if entry is None:
                self._stats.misses += 1
                return False, None

            if entry.is_expired:
                self._remove(key)
                self._stats.expirations += 1
                self._stats.misses += 1
                return False, None

            # Move to end (most recently used)
            self._cache.move_to_end(key)
            self._stats.hits += 1
            return True, entry.hit()

    def set(
        self,
        key: str,
        value: Any,
        ttl: float | None = None,
    ) -> None:
        """Set a value in the cache."""
        with self._lock:
            # Calculate size
            try:
                size = len(pickle.dumps(value))
            except Exception:
                size = 0

            # Create entry
            now = time.time()
            entry = CacheEntry(
                value=value,
                created_at=now,
                expires_at=now + ttl if ttl else None,
                size_bytes=size,
            )

            # Remove old entry if exists
            if key in self._cache:
                self._remove(key)

            # Evict if necessary
            self._evict_if_needed(size)

            # Add new entry
            self._cache[key] = entry
            self._stats.total_size_bytes += size
            self._stats.entry_count = len(self._cache)

    def _remove(self, key: str) -> None:
        """Remove an entry from the cache."""
        if key in self._cache:
            entry = self._cache.pop(key)
            self._stats.total_size_bytes -= entry.size_bytes
            self._stats.entry_count = len(self._cache)

    def _evict_if_needed(self, incoming_size: int) -> None:
        """Evict entries if needed to make room."""
        # Check entry count
        while len(self._cache) >= self.max_entries:
            oldest_key = next(iter(self._cache))
            self._remove(oldest_key)
            self._stats.evictions += 1

        # Check size limit
        if self.max_size_bytes is not None:
            while (
                self._stats.total_size_bytes + incoming_size > self.max_size_bytes
                and self._cache
            ):
                oldest_key = next(iter(self._cache))
                self._remove(oldest_key)
                self._stats.evictions += 1

    def clear(self) -> None:
        """Clear all entries in this namespace."""
        with self._lock:
            self._cache.clear()
            self._stats.total_size_bytes = 0
            self._stats.entry_count = 0

    def invalidate(self, key: str) -> bool:
        """
        Invalidate a specific cache entry.

        Returns:
            True if the entry was found and removed.
        """
        with self._lock:
            if key in self._cache:
                self._remove(key)
                return True
            return False

    @property
    def stats(self) -> CacheStats:
        """Get cache statistics."""
        return self._stats

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.

        Returns:
            Number of entries removed.
        """
        removed = 0
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items() if entry.is_expired
            ]
            for key in expired_keys:
                self._remove(key)
                self._stats.expirations += 1
                removed += 1
        return removed


class CacheManager:
    """Global cache manager for all namespaces."""

    _instance: "CacheManager | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "CacheManager":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._namespaces = {}
                cls._instance._ns_lock = threading.RLock()
            return cls._instance

    def get_namespace(
        self,
        name: str = "default",
        max_entries: int = 1000,
        max_size_bytes: int | None = None,
    ) -> CacheNamespace:
        """Get or create a cache namespace."""
        with self._ns_lock:
            if name not in self._namespaces:
                self._namespaces[name] = CacheNamespace(
                    name=name,
                    max_entries=max_entries,
                    max_size_bytes=max_size_bytes,
                )
            return self._namespaces[name]

    def clear_all(self) -> None:
        """Clear all cache namespaces."""
        with self._ns_lock:
            for ns in self._namespaces.values():
                ns.clear()

    def clear_namespace(self, name: str) -> bool:
        """Clear a specific namespace."""
        with self._ns_lock:
            if name in self._namespaces:
                self._namespaces[name].clear()
                return True
            return False

    def get_all_stats(self) -> dict[str, dict[str, Any]]:
        """Get statistics for all namespaces."""
        with self._ns_lock:
            return {name: ns.stats.to_dict() for name, ns in self._namespaces.items()}

    def cleanup_all_expired(self) -> int:
        """Clean up expired entries in all namespaces."""
        total = 0
        with self._ns_lock:
            for ns in self._namespaces.values():
                total += ns.cleanup_expired()
        return total


# Global cache manager instance
_manager = CacheManager()


def _make_cache_key(func: Callable, args: tuple, kwargs: dict) -> str:
    """Create a cache key from function and arguments."""
    # Get function identifier
    func_id = f"{func.__module__}.{func.__qualname__}"

    # Serialize arguments
    key_parts = [func_id]

    for arg in args:
        try:
            key_parts.append(json.dumps(arg, sort_keys=True, default=str))
        except (TypeError, ValueError):
            key_parts.append(str(arg))

    for k, v in sorted(kwargs.items()):
        try:
            key_parts.append(f"{k}={json.dumps(v, sort_keys=True, default=str)}")
        except (TypeError, ValueError):
            key_parts.append(f"{k}={v}")

    # Hash the key for consistent length
    key_string = "|".join(key_parts)
    return hashlib.sha256(key_string.encode()).hexdigest()


def cache(
    ttl: float | None = None,
    max_entries: int = 1000,
    namespace: str | None = None,
    key_func: Callable[..., str] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Cache decorator for data/computation results.

    Similar to Streamlit's @st.cache_data but with additional features:
    - TTL (time-to-live) support
    - Custom key generation
    - Namespace isolation
    - Cache statistics

    Args:
        ttl: Time-to-live in seconds. None means no expiration.
        max_entries: Maximum number of entries in the cache.
        namespace: Cache namespace for isolation. Defaults to function name.
        key_func: Custom function to generate cache keys.

    Returns:
        Decorated function with caching.

    Example:
        @cache(ttl=3600)  # 1 hour TTL
        def expensive_computation(x: int) -> int:
            time.sleep(2)
            return x ** 2

        # First call - slow
        result1 = expensive_computation(5)

        # Second call - instant (cached)
        result2 = expensive_computation(5)
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        ns_name = namespace or f"cache:{func.__module__}.{func.__qualname__}"
        ns = _manager.get_namespace(ns_name, max_entries=max_entries)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Generate cache key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = _make_cache_key(func, args, kwargs)

            # Check cache
            found, value = ns.get(key)
            if found:
                return value

            # Compute and cache
            result = func(*args, **kwargs)
            ns.set(key, result, ttl=ttl)
            return result

        # Attach cache control methods
        wrapper.cache_clear = ns.clear  # type: ignore
        wrapper.cache_info = lambda: ns.stats  # type: ignore
        wrapper.cache_invalidate = ns.invalidate  # type: ignore

        return wrapper

    return decorator


def cache_resource(
    ttl: float | None = None,
    namespace: str | None = None,
    validate: Callable[[Any], bool] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Cache decorator for global resources (models, connections, etc.).

    Similar to Streamlit's @st.cache_resource. Use this for objects that
    should be shared across all reruns and sessions, like ML models or
    database connections.

    Args:
        ttl: Time-to-live in seconds. None means no expiration.
        namespace: Cache namespace for isolation.
        validate: Function to validate cached resource is still valid.

    Returns:
        Decorated function with resource caching.

    Example:
        @cache_resource
        def load_model():
            # Only loaded once, shared across all sessions
            return load_expensive_ml_model()

        @cache_resource(validate=lambda conn: conn.is_connected())
        def get_db_connection():
            return create_database_connection()
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        ns_name = namespace or f"resource:{func.__module__}.{func.__qualname__}"
        ns = _manager.get_namespace(ns_name, max_entries=100)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = _make_cache_key(func, args, kwargs)

            # Check cache
            found, value = ns.get(key)
            if found:
                # Validate if validator provided
                if validate is not None:
                    try:
                        if not validate(value):
                            ns.invalidate(key)
                            found = False
                    except Exception:
                        ns.invalidate(key)
                        found = False

            if found:
                return value

            # Create resource and cache
            result = func(*args, **kwargs)
            ns.set(key, result, ttl=ttl)
            return result

        wrapper.cache_clear = ns.clear  # type: ignore
        wrapper.cache_info = lambda: ns.stats  # type: ignore

        return wrapper

    return decorator


def async_cache(
    ttl: float | None = None,
    max_entries: int = 1000,
    namespace: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Cache decorator for async functions.

    Args:
        ttl: Time-to-live in seconds.
        max_entries: Maximum number of entries.
        namespace: Cache namespace.

    Returns:
        Decorated async function with caching.

    Example:
        @async_cache(ttl=300)
        async def fetch_user_data(user_id: str) -> dict:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"/users/{user_id}") as response:
                    return await response.json()
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        ns_name = namespace or f"async:{func.__module__}.{func.__qualname__}"
        ns = _manager.get_namespace(ns_name, max_entries=max_entries)

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            key = _make_cache_key(func, args, kwargs)

            # Check cache
            found, value = ns.get(key)
            if found:
                return value

            # Compute and cache
            result = await func(*args, **kwargs)
            ns.set(key, result, ttl=ttl)
            return result

        wrapper.cache_clear = ns.clear  # type: ignore
        wrapper.cache_info = lambda: ns.stats  # type: ignore

        return wrapper

    return decorator


# =============================================================================
# Convenience Functions
# =============================================================================


def clear_all_caches() -> None:
    """Clear all cache namespaces."""
    _manager.clear_all()


def clear_cache(namespace: str) -> bool:
    """Clear a specific cache namespace."""
    return _manager.clear_namespace(namespace)


def get_cache_stats() -> dict[str, dict[str, Any]]:
    """Get statistics for all caches."""
    return _manager.get_all_stats()


def cleanup_expired() -> int:
    """
    Clean up all expired cache entries.

    Returns:
        Number of entries removed.
    """
    return _manager.cleanup_all_expired()


# =============================================================================
# Memoization helpers
# =============================================================================


def memoize(func: Callable[P, R]) -> Callable[P, R]:
    """
    Simple memoization decorator (no TTL, no limits).

    Use for pure functions with hashable arguments.

    Example:
        @memoize
        def fibonacci(n: int) -> int:
            if n < 2:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)
    """
    memo: dict[str, Any] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = _make_cache_key(func, args, kwargs)
        if key not in memo:
            memo[key] = func(*args, **kwargs)
        return memo[key]

    wrapper.cache_clear = memo.clear  # type: ignore
    return wrapper


# =============================================================================
# Context Manager for temporary cache disabling
# =============================================================================


class _CacheDisabled:
    """Context manager to temporarily disable caching."""

    _disabled = threading.local()

    @classmethod
    def is_disabled(cls) -> bool:
        return getattr(cls._disabled, "value", False)

    def __enter__(self) -> "_CacheDisabled":
        self._disabled.value = True
        return self

    def __exit__(self, *args: Any) -> None:
        self._disabled.value = False


def no_cache() -> _CacheDisabled:
    """
    Context manager to temporarily disable caching.

    Example:
        with no_cache():
            # This call will not use cache
            result = expensive_function()
    """
    return _CacheDisabled()


# =============================================================================
# AI-Specific Caching
# =============================================================================


def cache_embedding(
    ttl: float = 86400,  # 24 hours default
    max_entries: int = 10000,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Specialized cache for embedding functions.

    Optimized for caching text embeddings with sensible defaults.

    Args:
        ttl: Time-to-live (default 24 hours)
        max_entries: Maximum cached embeddings (default 10,000)

    Example:
        @cache_embedding()
        def get_embedding(text: str) -> list[float]:
            return openai.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            ).data[0].embedding
    """
    return cache(ttl=ttl, max_entries=max_entries, namespace="embeddings")


def cache_llm_response(
    ttl: float = 3600,  # 1 hour default
    max_entries: int = 500,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Specialized cache for LLM responses.

    Useful for caching deterministic LLM calls (temperature=0).

    Args:
        ttl: Time-to-live (default 1 hour)
        max_entries: Maximum cached responses (default 500)

    Example:
        @cache_llm_response()
        def classify_sentiment(text: str) -> str:
            response = openai.chat.completions.create(
                model="gpt-4",
                temperature=0,
                messages=[{"role": "user", "content": f"Classify: {text}"}]
            )
            return response.choices[0].message.content
    """
    return cache(ttl=ttl, max_entries=max_entries, namespace="llm_responses")
