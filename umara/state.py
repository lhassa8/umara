"""
State management for Umara.

Provides efficient state handling that avoids full script re-runs.
Only components that depend on changed state will re-render.
"""

from __future__ import annotations

import functools
import hashlib
import threading
from collections import defaultdict
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass
class StateValue(Generic[T]):
    """A reactive state value that tracks changes."""

    value: T
    version: int = 0
    subscribers: set = field(default_factory=set)

    def set(self, new_value: T) -> bool:
        """Set value and return True if changed."""
        if self.value != new_value:
            self.value = new_value
            self.version += 1
            return True
        return False


class SessionState:
    """
    Session-scoped state container.

    Each user session has its own state that persists across interactions.
    State changes trigger targeted re-renders instead of full script re-runs.
    """

    def __init__(self):
        self._state: dict[str, StateValue] = {}
        self._lock = threading.RLock()
        self._change_callbacks: list[Callable[[str, Any], None]] = []

    def __getattr__(self, key: str) -> Any:
        # Only treat truly internal attributes as object attributes
        if key.startswith("__") or key in ("_state", "_lock", "_change_callbacks"):
            return object.__getattribute__(self, key)
        with self._lock:
            if key in self._state:
                return self._state[key].value
            raise AttributeError(
                f"State key '{key}' not found. Set it first with session_state.{key} = value"
            )

    def __setattr__(self, key: str, value: Any) -> None:
        # Only treat truly internal attributes (double underscore or specific internal names)
        # as object attributes. Single underscore keys like "_input_Name" are state keys.
        if key.startswith("__") or key in ("_state", "_lock", "_change_callbacks"):
            object.__setattr__(self, key, value)
            return
        with self._lock:
            if key in self._state:
                changed = self._state[key].set(value)
            else:
                self._state[key] = StateValue(value=value)
                changed = True

            if changed:
                for callback in self._change_callbacks:
                    callback(key, value)

    def __contains__(self, key: str) -> bool:
        return key in self._state

    def get(self, key: str, default: T | None = None) -> T | None:
        """Get a state value with optional default."""
        with self._lock:
            if key in self._state:
                return self._state[key].value
            return default

    def setdefault(self, key: str, default: T) -> T:
        """Set a default value if key doesn't exist, return the value."""
        with self._lock:
            if key not in self._state:
                self._state[key] = StateValue(value=default)
            return self._state[key].value

    def update(self, **kwargs) -> None:
        """Update multiple state values at once."""
        with self._lock:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def clear(self) -> None:
        """Clear all state."""
        with self._lock:
            self._state.clear()

    def keys(self):
        """Return all state keys."""
        return self._state.keys()

    def values(self):
        """Return all state values."""
        return [sv.value for sv in self._state.values()]

    def items(self):
        """Return all state key-value pairs."""
        return [(k, sv.value) for k, sv in self._state.items()]

    def on_change(self, callback: Callable[[str, Any], None]) -> None:
        """Register a callback for state changes."""
        self._change_callbacks.append(callback)

    def to_dict(self) -> dict[str, Any]:
        """Export state as dictionary."""
        return {k: sv.value for k, sv in self._state.items()}

    def from_dict(self, data: dict[str, Any]) -> None:
        """Import state from dictionary."""
        with self._lock:
            for key, value in data.items():
                if key in self._state:
                    self._state[key].set(value)
                else:
                    self._state[key] = StateValue(value=value)


# Context variable for session state (per-request/session)
_session_state_var: ContextVar[SessionState | None] = ContextVar("session_state", default=None)


def get_session_state() -> SessionState:
    """Get the current session's state."""
    state = _session_state_var.get()
    if state is None:
        state = SessionState()
        _session_state_var.set(state)
    return state


def set_session_state(state: SessionState) -> None:
    """Set the session state for the current context."""
    _session_state_var.set(state)


# Convenience proxy for session state
class _SessionStateProxy:
    """Proxy that delegates to the current session's state."""

    def __getattr__(self, key: str) -> Any:
        return getattr(get_session_state(), key)

    def __setattr__(self, key: str, value: Any) -> None:
        setattr(get_session_state(), key, value)

    def __contains__(self, key: str) -> bool:
        return key in get_session_state()

    def get(self, key: str, default: Any = None) -> Any:
        return get_session_state().get(key, default)

    def setdefault(self, key: str, default: Any) -> Any:
        return get_session_state().setdefault(key, default)

    def update(self, **kwargs) -> None:
        get_session_state().update(**kwargs)

    def clear(self) -> None:
        get_session_state().clear()


# Global session state proxy
session_state = _SessionStateProxy()


class ComponentState:
    """
    Component-level state that persists across re-renders.

    Used internally by components to maintain their state without
    polluting the session state namespace.
    """

    def __init__(self, component_id: str):
        self._component_id = component_id
        self._state: dict[str, Any] = {}

    def __getitem__(self, key: str) -> Any:
        return self._state.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._state[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._state

    def get(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._state[key] = value


# Component state registry
_component_states: dict[str, dict[str, ComponentState]] = defaultdict(dict)


def get_component_state(session_id: str, component_id: str) -> ComponentState:
    """Get or create component state for a specific component."""
    if component_id not in _component_states[session_id]:
        _component_states[session_id][component_id] = ComponentState(component_id)
    return _component_states[session_id][component_id]


def clear_component_states(session_id: str) -> None:
    """Clear all component states for a session."""
    if session_id in _component_states:
        del _component_states[session_id]


class Cache:
    """
    Simple caching mechanism for expensive computations.

    Caches results based on function arguments, with optional TTL.
    """

    def __init__(self):
        self._cache: dict[str, dict[str, Any]] = {}

    def _make_key(self, func: Callable, args: tuple, kwargs: dict) -> str:
        """Create a cache key from function and arguments."""
        key_parts = [func.__module__, func.__qualname__]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        key_str = "|".join(key_parts)
        return hashlib.md5(key_str.encode(), usedforsecurity=False).hexdigest()

    def get(self, key: str) -> tuple[bool, Any]:
        """Get cached value. Returns (found, value)."""
        if key in self._cache:
            return True, self._cache[key]["value"]
        return False, None

    def set(self, key: str, value: Any) -> None:
        """Set cached value."""
        self._cache[key] = {"value": value}

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        """Decorator to cache function results."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            key = self._make_key(func, args, kwargs)
            found, value = self.get(key)
            if found:
                return value
            result = func(*args, **kwargs)
            self.set(key, result)
            return result

        return wrapper


# Global cache instance
cache = Cache()


class CacheData:
    """
    Streamlit-compatible caching decorator for data functions.

    Caches the output of expensive data operations (API calls, database queries,
    data transformations) based on function arguments.

    Features:
    - TTL (time-to-live) support for automatic cache expiration
    - Hash-based function argument tracking
    - Thread-safe operation
    - Supports DataFrame-like objects

    Example:
        @um.cache_data(ttl=3600)  # Cache for 1 hour
        def fetch_data(url):
            return requests.get(url).json()

        @um.cache_data  # Cache forever
        def expensive_computation(x, y):
            return x ** y
    """

    def __init__(self):
        self._cache: dict[str, dict[str, Any]] = {}
        self._lock = threading.RLock()

    def _make_key(self, func: Callable, args: tuple, kwargs: dict) -> str:
        """Create a cache key from function and arguments."""
        import pickle

        key_parts = [func.__module__, func.__qualname__]

        # Handle args - try to hash, fallback to str representation
        for arg in args:
            try:
                # Try pickle for hashable objects
                key_parts.append(hashlib.md5(pickle.dumps(arg), usedforsecurity=False).hexdigest())
            except (pickle.PicklingError, TypeError):
                # Fallback for unhashable objects
                if hasattr(arg, "to_dict"):
                    # DataFrame-like objects
                    key_parts.append(str(arg.to_dict()))
                else:
                    key_parts.append(str(arg))

        # Handle kwargs
        for k, v in sorted(kwargs.items()):
            try:
                key_parts.append(
                    f"{k}={hashlib.md5(pickle.dumps(v), usedforsecurity=False).hexdigest()}"
                )
            except (pickle.PicklingError, TypeError):
                key_parts.append(f"{k}={v}")

        key_str = "|".join(key_parts)
        return hashlib.md5(key_str.encode(), usedforsecurity=False).hexdigest()

    def _is_expired(self, entry: dict[str, Any]) -> bool:
        """Check if a cache entry has expired."""
        import time

        if entry.get("ttl") is None:
            return False
        return time.time() > entry["expires_at"]

    def get(self, key: str) -> tuple[bool, Any]:
        """Get cached value. Returns (found, value)."""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if not self._is_expired(entry):
                    return True, entry["value"]
                # Clean up expired entry
                del self._cache[key]
            return False, None

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set cached value with optional TTL in seconds."""
        import time

        with self._lock:
            entry = {"value": value, "ttl": ttl}
            if ttl is not None:
                entry["expires_at"] = time.time() + ttl
            self._cache[key] = entry

    def clear(self) -> None:
        """Clear all cached values."""
        with self._lock:
            self._cache.clear()

    def __call__(
        self,
        func: Callable[..., T] | None = None,
        *,
        ttl: int | None = None,
        show_spinner: bool = True,
        max_entries: int | None = None,
    ) -> Callable[..., T] | Callable[[Callable[..., T]], Callable[..., T]]:
        """
        Decorator to cache function results.

        Args:
            func: The function to cache (when used without parentheses)
            ttl: Time-to-live in seconds. None means cache forever.
            show_spinner: Whether to show a spinner while computing (default: True)
            max_entries: Maximum number of entries to keep in cache (LRU eviction)

        Usage:
            @um.cache_data
            def my_func(): ...

            @um.cache_data(ttl=3600)
            def my_func(): ...
        """

        def decorator(fn: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(fn)
            def wrapper(*args: Any, **kwargs: Any) -> T:
                key = self._make_key(fn, args, kwargs)
                found, value = self.get(key)
                if found:
                    return value

                # Execute function and cache result
                result = fn(*args, **kwargs)
                self.set(key, result, ttl=ttl)

                # LRU eviction if max_entries is set
                if max_entries is not None:
                    with self._lock:
                        while len(self._cache) > max_entries:
                            # Remove oldest entry
                            oldest_key = next(iter(self._cache))
                            del self._cache[oldest_key]

                return result

            # Add clear method to the wrapper
            wrapper.clear = lambda: self._clear_func(fn)  # type: ignore
            return wrapper

        # Handle both @cache_data and @cache_data(...) syntax
        if func is not None:
            return decorator(func)
        return decorator

    def _clear_func(self, func: Callable) -> None:
        """Clear cache entries for a specific function."""
        prefix = f"{func.__module__}|{func.__qualname__}"
        with self._lock:
            keys_to_remove = [k for k, v in self._cache.items() if prefix in str(v)]
            for k in keys_to_remove:
                del self._cache[k]


# Streamlit-compatible cache_data decorator
cache_data = CacheData()


class CacheResource:
    """
    Caching decorator for global resources (database connections, ML models).

    Unlike cache_data, cache_resource is designed for objects that should be
    shared across all users and sessions, like database connections or ML models.

    Example:
        @um.cache_resource
        def get_database():
            return create_connection()

        @um.cache_resource(ttl=3600)
        def load_model():
            return load_ml_model()
    """

    def __init__(self):
        self._cache: dict[str, dict[str, Any]] = {}
        self._lock = threading.RLock()

    def _make_key(self, func: Callable) -> str:
        """Create a cache key from function (no args considered for resources)."""
        return f"{func.__module__}|{func.__qualname__}"

    def __call__(
        self,
        func: Callable[..., T] | None = None,
        *,
        ttl: int | None = None,
    ) -> Callable[..., T] | Callable[[Callable[..., T]], Callable[..., T]]:
        """Decorator to cache global resources."""
        import time

        def decorator(fn: Callable[..., T]) -> Callable[..., T]:
            @functools.wraps(fn)
            def wrapper(*args: Any, **kwargs: Any) -> T:
                key = self._make_key(fn)

                with self._lock:
                    if key in self._cache:
                        entry = self._cache[key]
                        # Check expiration
                        if ttl is None or time.time() <= entry.get("expires_at", float("inf")):
                            return entry["value"]

                    # Execute and cache
                    result = fn(*args, **kwargs)
                    entry = {"value": result}
                    if ttl is not None:
                        entry["expires_at"] = time.time() + ttl
                    self._cache[key] = entry
                    return result

            wrapper.clear = lambda: self._clear_func(fn)  # type: ignore
            return wrapper

        if func is not None:
            return decorator(func)
        return decorator

    def _clear_func(self, func: Callable) -> None:
        """Clear cache for a specific function."""
        key = self._make_key(func)
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self) -> None:
        """Clear all cached resources."""
        with self._lock:
            self._cache.clear()


# Streamlit-compatible cache_resource decorator
cache_resource = CacheResource()


def state(default: T | None = None) -> T | None:
    """
    Create a reactive state value.

    This is a convenience function for simple state management.
    For more complex needs, use session_state directly.

    Example:
        count = um.state(0)
        if um.button('Increment'):
            session_state.count = count + 1
    """
    import inspect

    # Get the variable name from the calling frame
    frame = inspect.currentframe()
    if frame and frame.f_back:
        # Try to find the variable name being assigned
        code = frame.f_back.f_code
        # Use a simple approach: hash the call location
        key = f"_state_{code.co_filename}_{frame.f_back.f_lineno}"
        return get_session_state().setdefault(key, default)

    return default
