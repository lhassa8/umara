"""
Fragments System for Umara.

Fragments enable partial reruns of your app - only updating specific
sections instead of re-rendering the entire page. This is a major
performance advantage over Streamlit's full-page reruns.

Example:
    import umara as um
    from umara.fragments import fragment

    @fragment
    def live_metrics():
        '''This section can rerun independently every 5 seconds.'''
        data = fetch_latest_metrics()
        um.metric("Active Users", data["users"])
        um.metric("CPU Usage", f"{data['cpu']}%")

    # Main app
    um.title("Dashboard")

    # This fragment updates independently
    live_metrics()

    # This won't re-render when the fragment updates
    um.write("Static content here")
"""

from __future__ import annotations

import asyncio
import functools
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar, ParamSpec, Generator

from umara.core import get_context, Component

P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class FragmentState:
    """State for a single fragment."""

    id: str
    name: str
    last_run: float = 0.0
    run_count: int = 0
    is_running: bool = False
    error: Exception | None = None
    output: Any = None


@dataclass
class FragmentConfig:
    """Configuration for a fragment."""

    run_every: float | None = None  # Auto-refresh interval in seconds
    on_change: list[str] | None = None  # State keys that trigger rerun
    debounce: float = 0.0  # Debounce time in seconds


class FragmentManager:
    """Manages fragment state and execution."""

    _instance: "FragmentManager | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "FragmentManager":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._fragments: dict[str, FragmentState] = {}
                cls._instance._configs: dict[str, FragmentConfig] = {}
                cls._instance._pending_reruns: set[str] = set()
                cls._instance._fs_lock = threading.RLock()
            return cls._instance

    def register(
        self,
        fragment_id: str,
        name: str,
        config: FragmentConfig,
    ) -> FragmentState:
        """Register a new fragment."""
        with self._fs_lock:
            if fragment_id not in self._fragments:
                self._fragments[fragment_id] = FragmentState(
                    id=fragment_id,
                    name=name,
                )
            self._configs[fragment_id] = config
            return self._fragments[fragment_id]

    def get_state(self, fragment_id: str) -> FragmentState | None:
        """Get fragment state."""
        return self._fragments.get(fragment_id)

    def mark_for_rerun(self, fragment_id: str) -> None:
        """Mark a fragment for rerun."""
        with self._fs_lock:
            self._pending_reruns.add(fragment_id)

    def get_pending_reruns(self) -> set[str]:
        """Get and clear pending reruns."""
        with self._fs_lock:
            pending = self._pending_reruns.copy()
            self._pending_reruns.clear()
            return pending

    def should_auto_rerun(self, fragment_id: str) -> bool:
        """Check if fragment should auto-rerun based on interval."""
        config = self._configs.get(fragment_id)
        state = self._fragments.get(fragment_id)

        if not config or not state or config.run_every is None:
            return False

        elapsed = time.time() - state.last_run
        return elapsed >= config.run_every

    def record_run(self, fragment_id: str, output: Any = None, error: Exception | None = None) -> None:
        """Record a fragment run."""
        with self._fs_lock:
            state = self._fragments.get(fragment_id)
            if state:
                state.last_run = time.time()
                state.run_count += 1
                state.is_running = False
                state.output = output
                state.error = error


# Global fragment manager
_manager = FragmentManager()


def fragment(
    func: Callable[P, R] | None = None,
    *,
    run_every: float | None = None,
    on_change: list[str] | None = None,
    debounce: float = 0.0,
    key: str | None = None,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to create a fragment (partial rerun section).

    Fragments can rerun independently without re-rendering the entire page.
    This is a key performance advantage over Streamlit.

    Args:
        run_every: Auto-refresh interval in seconds.
        on_change: List of state keys that trigger rerun when changed.
        debounce: Debounce time to prevent rapid reruns.
        key: Unique key for this fragment. Auto-generated if not provided.

    Returns:
        Decorated function that runs as a fragment.

    Example:
        @fragment(run_every=5.0)
        def live_chart():
            data = fetch_live_data()
            um.line_chart(data)

        @fragment(on_change=["selected_user"])
        def user_details():
            user = state.selected_user
            um.write(f"Details for {user}")
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        fragment_key = key or f"fragment:{fn.__module__}.{fn.__qualname__}"

        config = FragmentConfig(
            run_every=run_every,
            on_change=on_change,
            debounce=debounce,
        )

        _manager.register(fragment_key, fn.__name__, config)

        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            ctx = get_context()
            state = _manager.get_state(fragment_key)

            if state:
                state.is_running = True

            # Create fragment container
            fragment_component = ctx.create_component(
                "fragment",
                props={
                    "fragment_id": fragment_key,
                    "fragment_name": fn.__name__,
                },
            )
            ctx.push(fragment_component)

            try:
                result = fn(*args, **kwargs)
                _manager.record_run(fragment_key, output=result)
                return result
            except Exception as e:
                _manager.record_run(fragment_key, error=e)
                raise
            finally:
                ctx.pop()

        # Attach fragment control methods
        wrapper.rerun = lambda: _manager.mark_for_rerun(fragment_key)  # type: ignore
        wrapper.fragment_id = fragment_key  # type: ignore
        wrapper.get_state = lambda: _manager.get_state(fragment_key)  # type: ignore

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


@contextmanager
def fragment_container(
    key: str,
    *,
    run_every: float | None = None,
) -> Generator[None, None, None]:
    """
    Context manager for creating a fragment inline.

    Use this when you don't want to create a separate function.

    Args:
        key: Unique key for this fragment.
        run_every: Auto-refresh interval in seconds.

    Example:
        with fragment_container("metrics", run_every=10.0):
            um.metric("CPU", get_cpu_usage())
            um.metric("Memory", get_memory_usage())
    """
    ctx = get_context()

    config = FragmentConfig(run_every=run_every)
    _manager.register(key, key, config)
    state = _manager.get_state(key)

    if state:
        state.is_running = True

    fragment_component = ctx.create_component(
        "fragment",
        props={
            "fragment_id": key,
            "fragment_name": key,
        },
    )
    ctx.push(fragment_component)

    try:
        yield
        _manager.record_run(key)
    except Exception as e:
        _manager.record_run(key, error=e)
        raise
    finally:
        ctx.pop()


def rerun_fragment(fragment_id: str) -> None:
    """
    Trigger a rerun of a specific fragment.

    Args:
        fragment_id: The fragment key to rerun.

    Example:
        # From a button callback
        if um.button("Refresh Data"):
            rerun_fragment("my_data_fragment")
    """
    _manager.mark_for_rerun(fragment_id)


def get_fragment_state(fragment_id: str) -> FragmentState | None:
    """
    Get the state of a fragment.

    Args:
        fragment_id: The fragment key.

    Returns:
        FragmentState or None if not found.
    """
    return _manager.get_state(fragment_id)


# =============================================================================
# Experimental: Async Fragments
# =============================================================================


def async_fragment(
    func: Callable[P, R] | None = None,
    *,
    run_every: float | None = None,
    key: str | None = None,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for async fragments.

    Args:
        run_every: Auto-refresh interval in seconds.
        key: Unique key for this fragment.

    Example:
        @async_fragment(run_every=5.0)
        async def live_data():
            data = await fetch_async_data()
            um.dataframe(data)
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        fragment_key = key or f"async_fragment:{fn.__module__}.{fn.__qualname__}"

        config = FragmentConfig(run_every=run_every)
        _manager.register(fragment_key, fn.__name__, config)

        @functools.wraps(fn)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            ctx = get_context()
            state = _manager.get_state(fragment_key)

            if state:
                state.is_running = True

            fragment_component = ctx.create_component(
                "fragment",
                props={
                    "fragment_id": fragment_key,
                    "fragment_name": fn.__name__,
                    "async": True,
                },
            )
            ctx.push(fragment_component)

            try:
                result = await fn(*args, **kwargs)
                _manager.record_run(fragment_key, output=result)
                return result
            except Exception as e:
                _manager.record_run(fragment_key, error=e)
                raise
            finally:
                ctx.pop()

        wrapper.rerun = lambda: _manager.mark_for_rerun(fragment_key)  # type: ignore
        wrapper.fragment_id = fragment_key  # type: ignore

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


# =============================================================================
# Fragment Groups
# =============================================================================


@dataclass
class FragmentGroup:
    """
    Group of related fragments that can be controlled together.

    Example:
        metrics_group = FragmentGroup("metrics")

        @metrics_group.fragment
        def cpu_metric():
            um.metric("CPU", get_cpu())

        @metrics_group.fragment
        def memory_metric():
            um.metric("Memory", get_memory())

        # Rerun all fragments in the group
        metrics_group.rerun_all()
    """

    name: str
    _fragment_ids: list[str] = field(default_factory=list)

    def fragment(
        self,
        func: Callable[P, R] | None = None,
        *,
        run_every: float | None = None,
        key: str | None = None,
    ) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
        """Add a fragment to this group."""

        def decorator(fn: Callable[P, R]) -> Callable[P, R]:
            fragment_key = key or f"group:{self.name}:{fn.__module__}.{fn.__qualname__}"
            self._fragment_ids.append(fragment_key)

            return fragment(fn, run_every=run_every, key=fragment_key)

        if func is not None:
            return decorator(func)
        return decorator

    def rerun_all(self) -> None:
        """Trigger rerun of all fragments in this group."""
        for fid in self._fragment_ids:
            _manager.mark_for_rerun(fid)

    @property
    def fragment_ids(self) -> list[str]:
        """Get all fragment IDs in this group."""
        return self._fragment_ids.copy()


# =============================================================================
# Polling Helper
# =============================================================================


def poll(
    interval: float,
    key: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Simple polling decorator - runs a function at fixed intervals.

    This is a convenience wrapper around fragment with run_every.

    Args:
        interval: Polling interval in seconds.
        key: Optional unique key.

    Example:
        @poll(interval=10.0)
        def check_status():
            status = get_service_status()
            if status == "down":
                um.error("Service is down!")
            else:
                um.success("Service is healthy")
    """
    return fragment(run_every=interval, key=key)


# =============================================================================
# Conditional Fragment
# =============================================================================


@contextmanager
def conditional_fragment(
    condition: bool,
    key: str,
) -> Generator[bool, None, None]:
    """
    Fragment that only renders when condition is True.

    Useful for expensive computations that should only run when needed.

    Args:
        condition: Whether to render the fragment.
        key: Unique key for this fragment.

    Yields:
        Whether the fragment is being rendered.

    Example:
        show_advanced = um.checkbox("Show advanced stats")

        with conditional_fragment(show_advanced, "advanced_stats") as should_render:
            if should_render:
                # This expensive computation only runs when checkbox is checked
                stats = compute_advanced_stats()
                um.dataframe(stats)
    """
    if condition:
        with fragment_container(key):
            yield True
    else:
        yield False


# =============================================================================
# Fragment Debugging
# =============================================================================


def get_all_fragment_stats() -> dict[str, dict[str, Any]]:
    """
    Get statistics for all registered fragments.

    Useful for debugging and monitoring.

    Returns:
        Dictionary mapping fragment IDs to their stats.
    """
    result = {}
    for fid, state in _manager._fragments.items():
        config = _manager._configs.get(fid)
        result[fid] = {
            "name": state.name,
            "run_count": state.run_count,
            "last_run": state.last_run,
            "is_running": state.is_running,
            "has_error": state.error is not None,
            "run_every": config.run_every if config else None,
        }
    return result
