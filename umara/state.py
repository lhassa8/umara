"""
State management for Umara.

Provides efficient state handling that avoids full script re-runs.
Only components that depend on changed state will re-render.
"""

from __future__ import annotations

import hashlib
import functools
from typing import Any, Callable, Dict, Generic, Optional, TypeVar
from dataclasses import dataclass, field
from contextvars import ContextVar
from collections import defaultdict
import threading

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
        self._state: Dict[str, StateValue] = {}
        self._lock = threading.RLock()
        self._change_callbacks: list[Callable[[str, Any], None]] = []

    def __getattr__(self, key: str) -> Any:
        if key.startswith("_"):
            return object.__getattribute__(self, key)
        with self._lock:
            if key in self._state:
                return self._state[key].value
            raise AttributeError(f"State key '{key}' not found. Set it first with session_state.{key} = value")

    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith("_"):
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

    def get(self, key: str, default: T = None) -> T:
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

    def to_dict(self) -> Dict[str, Any]:
        """Export state as dictionary."""
        return {k: sv.value for k, sv in self._state.items()}

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Import state from dictionary."""
        with self._lock:
            for key, value in data.items():
                if key in self._state:
                    self._state[key].set(value)
                else:
                    self._state[key] = StateValue(value=value)


# Context variable for session state (per-request/session)
_session_state_var: ContextVar[Optional[SessionState]] = ContextVar(
    "session_state", default=None
)


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
        self._state: Dict[str, Any] = {}

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
_component_states: Dict[str, Dict[str, ComponentState]] = defaultdict(dict)


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
        self._cache: Dict[str, Dict[str, Any]] = {}

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


def state(default: T = None) -> T:
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
        import dis
        code = frame.f_back.f_code
        # Use a simple approach: hash the call location
        key = f"_state_{code.co_filename}_{frame.f_back.f_lineno}"
        return get_session_state().setdefault(key, default)

    return default
