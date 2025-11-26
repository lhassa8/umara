"""
Core framework for Umara.

Manages the application lifecycle, component tree, and communication
with the frontend.
"""

from __future__ import annotations

import asyncio
import threading
import traceback
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from umara.state import SessionState, StateValue, set_session_state
from umara.themes import get_theme


class RerunException(Exception):
    """Raised to trigger a rerun of the app."""

    pass


class StopException(Exception):
    """Raised to stop execution of the app."""

    pass


@dataclass
class Component:
    """Base component representation."""

    id: str
    type: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list[Component] = field(default_factory=list)
    style: dict[str, str] | None = None
    events: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "type": self.type,
            "props": self.props,
            "children": [c.to_dict() for c in self.children],
            "style": self.style,
            "events": self.events,
        }


class ComponentContext:
    """
    Context for building component trees.

    Tracks the current parent component for nested component creation.
    """

    def __init__(self):
        self._stack: list[Component] = []
        self._root: Component | None = None
        self._components: dict[str, Component] = {}
        self._id_counter = 0

    def generate_id(self, prefix: str = "um") -> str:
        """Generate a unique component ID."""
        self._id_counter += 1
        return f"{prefix}-{self._id_counter}"

    def create_component(
        self,
        type: str,
        props: dict[str, Any] | None = None,
        style: dict[str, str] | None = None,
        events: dict[str, str] | None = None,
        key: str | None = None,
    ) -> Component:
        """Create a new component and add to current parent."""
        component = Component(
            id=key or self.generate_id(type),
            type=type,
            props=props or {},
            style=style,
            events=events or {},
        )
        self._components[component.id] = component

        if self._stack:
            self._stack[-1].children.append(component)
        else:
            if self._root is None:
                self._root = Component(
                    id="root",
                    type="root",
                    children=[component],
                )
            else:
                self._root.children.append(component)

        return component

    def push(self, component: Component) -> None:
        """Push component onto context stack."""
        self._stack.append(component)

    def pop(self) -> Component | None:
        """Pop component from context stack."""
        if self._stack:
            return self._stack.pop()
        return None

    def get_root(self) -> Component | None:
        """Get the root component."""
        return self._root

    def get_component(self, id: str) -> Component | None:
        """Get component by ID."""
        return self._components.get(id)

    def update_component(self, component_id: str, props: dict[str, Any]) -> None:
        """Update props of an existing component (for streaming updates)."""
        component = self._components.get(component_id)
        if component:
            component.props.update(props)

    def reset(self) -> None:
        """Reset the context for a new render."""
        self._stack.clear()
        self._root = None
        self._components.clear()
        self._id_counter = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert entire component tree to dictionary."""
        if self._root:
            return self._root.to_dict()
        return {"id": "root", "type": "root", "children": [], "props": {}}

    @contextmanager
    def container(
        self,
        type: str,
        props: dict[str, Any] | None = None,
        style: dict[str, str] | None = None,
    ):
        """Context manager for container components."""
        component = self.create_component(type, props=props, style=style)
        self.push(component)
        try:
            yield component
        finally:
            self.pop()


# Context variable for component context
_component_context: ContextVar[ComponentContext | None] = ContextVar(
    "component_context", default=None
)


def get_context() -> ComponentContext:
    """Get the current component context."""
    ctx = _component_context.get()
    if ctx is None:
        ctx = ComponentContext()
        _component_context.set(ctx)
    return ctx


def set_context(ctx: ComponentContext) -> None:
    """Set the component context."""
    _component_context.set(ctx)


class Session:
    """
    Represents a connected client session.

    Manages state, component tree, and WebSocket connection.
    """

    def __init__(self, session_id: str):
        self.id = session_id
        self.state = SessionState()
        self.context = ComponentContext()
        self.websocket: Any = None  # WebSocket instance, typed as Any for flexibility
        self._event_handlers: dict[str, Callable] = {}
        self._pending_updates: list[dict[str, Any]] = []
        self._lock = asyncio.Lock()

    def register_handler(self, event_id: str, handler: Callable) -> None:
        """Register an event handler."""
        self._event_handlers[event_id] = handler

    def get_handler(self, event_id: str) -> Callable | None:
        """Get an event handler."""
        return self._event_handlers.get(event_id)

    async def send_update(self, update: dict[str, Any]) -> None:
        """Send an update to the client."""
        if self.websocket:
            try:
                await self.websocket.send_json(update)
            except (ConnectionError, RuntimeError):
                # Connection closed or WebSocket in invalid state - expected during disconnect
                pass

    def queue_update(self, update: dict[str, Any]) -> None:
        """Queue an update for batch sending."""
        self._pending_updates.append(update)

    async def flush_updates(self) -> None:
        """Send all pending updates."""
        if self._pending_updates and self.websocket:
            async with self._lock:
                updates = self._pending_updates.copy()
                self._pending_updates.clear()
                for update in updates:
                    try:
                        await self.websocket.send_json(update)
                    except Exception:
                        break


class UmaraApp:
    """
    Main Umara application class.

    Manages sessions, handles events, and coordinates between
    the Python backend and JavaScript frontend.
    """

    def __init__(self, title: str = "Umara App"):
        self.title = title
        self.sessions: dict[str, Session] = {}
        self._app_func: Callable | None = None
        self._on_start: list[Callable] = []
        self._on_stop: list[Callable] = []
        self._static_dir: Path | None = None
        self._lock = threading.RLock()
        self.config: dict[str, Any] = {}

    def set_app_function(self, func: Callable) -> None:
        """Set the main app function to run."""
        self._app_func = func

    def create_session(self, session_id: str | None = None) -> Session:
        """Create a new session."""
        if session_id is None:
            session_id = str(uuid.uuid4())

        session = Session(session_id)
        with self._lock:
            self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Session | None:
        """Get an existing session."""
        return self.sessions.get(session_id)

    def remove_session(self, session_id: str) -> None:
        """Remove a session."""
        with self._lock:
            if session_id in self.sessions:
                del self.sessions[session_id]

    async def render_session(self, session: Session) -> dict[str, Any]:
        """
        Render the app for a specific session.

        Returns the complete component tree.
        """
        if not self._app_func:
            return {"id": "root", "type": "root", "children": [], "props": {}}

        # Set up context for this session
        session.context.reset()
        set_context(session.context)
        set_session_state(session.state)

        # Run the app function
        try:
            result = self._app_func()
            if asyncio.iscoroutine(result):
                await result
        except Exception as e:
            # Create error component
            session.context.create_component(
                type="error",
                props={
                    "message": str(e),
                    "traceback": traceback.format_exc(),
                },
            )

        # Get the component tree
        tree = session.context.to_dict()

        # Add theme information
        theme = get_theme()

        # Clean up ephemeral click states after render
        # These should only be True for one render cycle
        keys_to_reset = [k for k in session.state._state.keys()
                        if k.endswith('_clicked') or k == '_form_submitted']
        for key in keys_to_reset:
            if key in session.state._state:
                session.state._state[key].value = False

        return {
            "tree": tree,
            "theme": theme.to_dict(),
            "state": session.state.to_dict(),
        }

    async def handle_event(
        self,
        session: Session,
        event_type: str,
        component_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Handle an event from the frontend.

        Returns updated component tree if needed.
        """
        # Handle click events by setting clicked state
        if event_type == "click":
            # Set the clicked state for this component
            # Button components use {state_key}_clicked pattern
            clicked_key = f"{component_id}_clicked"
            session.state._state[clicked_key] = StateValue(True)

            # Check if this is a form submit button by checking payload
            if payload.get("is_form_submit"):
                session.state._state["_form_submitted"] = StateValue(True)

        # Look for custom registered handler
        handler = session.get_handler(f"{component_id}:{event_type}")
        if handler:
            try:
                result = handler(payload)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                return {
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                }

        # Re-render the app
        return await self.render_session(session)

    async def handle_state_update(
        self,
        session: Session,
        key: str,
        value: Any,
    ) -> dict[str, Any]:
        """Handle a state update from the frontend."""
        setattr(session.state, key, value)
        return await self.render_session(session)

    def on_start(self, func: Callable) -> Callable:
        """Decorator to register a startup handler."""
        self._on_start.append(func)
        return func

    def on_stop(self, func: Callable) -> Callable:
        """Decorator to register a shutdown handler."""
        self._on_stop.append(func)
        return func


# Global app instance
_app: UmaraApp | None = None
_app_lock = threading.Lock()


def get_app() -> UmaraApp:
    """Get or create the global app instance."""
    global _app
    with _app_lock:
        if _app is None:
            _app = UmaraApp()
        return _app


def run(
    app_func: Callable | None = None,
    *,
    host: str = "127.0.0.1",
    port: int = 8501,
    title: str = "Umara App",
    debug: bool = False,
    reload: bool = True,
) -> None:
    """
    Run the Umara application.

    This is typically called from the CLI, but can also be used
    programmatically.

    Args:
        app_func: The main app function (optional if using CLI)
        host: Host to bind to
        port: Port to bind to
        title: Page title
        debug: Enable debug mode
        reload: Enable hot reload
    """
    from umara.server import start_server

    app = get_app()
    app.title = title

    if app_func:
        app.set_app_function(app_func)

    # Start the server
    start_server(app, host=host, port=port, debug=debug, reload=reload)


class ContainerContext:
    """Context manager for container components."""

    def __init__(self, component: Component):
        self.component = component
        self._ctx: ComponentContext | None = None

    def __enter__(self):
        self._ctx = get_context()
        self._ctx.push(self.component)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._ctx:
            self._ctx.pop()
        return False
