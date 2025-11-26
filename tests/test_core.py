"""
Unit tests for umara.core module.
"""

import pytest

from umara.core import (
    Component,
    ComponentContext,
    ContainerContext,
    RerunException,
    Session,
    StopException,
    UmaraApp,
    get_app,
    get_context,
    set_context,
)


class TestComponent:
    """Tests for Component dataclass."""

    @pytest.mark.unit
    def test_component_creation(self):
        """Test basic component creation."""
        component = Component(
            id="test-1",
            type="button",
            props={"label": "Click me"},
        )
        assert component.id == "test-1"
        assert component.type == "button"
        assert component.props == {"label": "Click me"}
        assert component.children == []
        assert component.style is None
        assert component.events == {}

    @pytest.mark.unit
    def test_component_with_all_fields(self):
        """Test component with all fields populated."""
        component = Component(
            id="test-2",
            type="card",
            props={"title": "Test Card"},
            children=[],
            style={"padding": "16px"},
            events={"click": "handle_click"},
        )
        assert component.style == {"padding": "16px"}
        assert component.events == {"click": "handle_click"}

    @pytest.mark.unit
    def test_component_to_dict(self, sample_component):
        """Test component serialization to dictionary."""
        result = sample_component.to_dict()

        assert result["id"] == "test-component-1"
        assert result["type"] == "button"
        assert result["props"]["label"] == "Test Button"
        assert result["style"] == {"color": "blue"}
        assert result["events"] == {"click": "on_click"}
        assert result["children"] == []

    @pytest.mark.unit
    def test_component_to_dict_with_children(self):
        """Test component serialization with nested children."""
        child = Component(id="child-1", type="text", props={"content": "Hello"})
        parent = Component(
            id="parent-1",
            type="container",
            props={},
            children=[child],
        )

        result = parent.to_dict()
        assert len(result["children"]) == 1
        assert result["children"][0]["id"] == "child-1"
        assert result["children"][0]["type"] == "text"


class TestComponentContext:
    """Tests for ComponentContext class."""

    @pytest.mark.unit
    def test_context_initialization(self):
        """Test context is properly initialized."""
        ctx = ComponentContext()
        assert ctx._stack == []
        assert ctx._root is None
        assert ctx._components == {}
        assert ctx._id_counter == 0

    @pytest.mark.unit
    def test_generate_id(self):
        """Test unique ID generation."""
        ctx = ComponentContext()
        id1 = ctx.generate_id("button")
        id2 = ctx.generate_id("button")
        id3 = ctx.generate_id("text")

        assert id1 == "button-1"
        assert id2 == "button-2"
        assert id3 == "text-3"

    @pytest.mark.unit
    def test_create_component(self, component_context):
        """Test component creation within context."""
        component = component_context.create_component(
            type="button",
            props={"label": "Test"},
        )

        assert component.type == "button"
        assert component.props == {"label": "Test"}
        assert component.id in component_context._components

    @pytest.mark.unit
    def test_create_component_with_style(self, component_context):
        """Test component creation with style."""
        component = component_context.create_component(
            type="text",
            props={"content": "Hello"},
            style={"color": "red", "fontSize": "16px"},
        )

        assert component.style == {"color": "red", "fontSize": "16px"}

    @pytest.mark.unit
    def test_root_component_creation(self, component_context):
        """Test that root component is created on first component."""
        assert component_context._root is None

        component_context.create_component(type="text", props={})

        assert component_context._root is not None
        assert component_context._root.type == "root"
        assert len(component_context._root.children) == 1

    @pytest.mark.unit
    def test_push_pop_stack(self, component_context):
        """Test push and pop operations on context stack."""
        component = component_context.create_component(type="container", props={})

        component_context.push(component)
        assert len(component_context._stack) == 1
        assert component_context._stack[-1] == component

        popped = component_context.pop()
        assert popped == component
        assert len(component_context._stack) == 0

    @pytest.mark.unit
    def test_nested_components(self, component_context):
        """Test nested component creation."""
        container = component_context.create_component(type="container", props={})
        component_context.push(container)

        child = component_context.create_component(type="text", props={"content": "Child"})

        component_context.pop()

        assert len(container.children) == 1
        assert container.children[0] == child

    @pytest.mark.unit
    def test_reset(self, component_context):
        """Test context reset."""
        component_context.create_component(type="text", props={})
        component_context.generate_id("test")

        component_context.reset()

        assert component_context._stack == []
        assert component_context._root is None
        assert component_context._components == {}
        assert component_context._id_counter == 0

    @pytest.mark.unit
    def test_to_dict_empty(self):
        """Test to_dict with no components."""
        ctx = ComponentContext()
        result = ctx.to_dict()

        assert result["id"] == "root"
        assert result["type"] == "root"
        assert result["children"] == []

    @pytest.mark.unit
    def test_get_component(self, component_context):
        """Test getting component by ID."""
        component = component_context.create_component(type="button", props={})

        retrieved = component_context.get_component(component.id)
        assert retrieved == component

        not_found = component_context.get_component("nonexistent")
        assert not_found is None


class TestSession:
    """Tests for Session class."""

    @pytest.mark.unit
    def test_session_creation(self):
        """Test session initialization."""
        session = Session("test-session")

        assert session.id == "test-session"
        assert isinstance(session.state, object)
        assert isinstance(session.context, ComponentContext)
        assert session.websocket is None

    @pytest.mark.unit
    def test_register_handler(self):
        """Test event handler registration."""
        session = Session("test")

        def handler(x):
            return x

        session.register_handler("btn-1:click", handler)

        assert session.get_handler("btn-1:click") == handler
        assert session.get_handler("nonexistent") is None

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_send_update_with_websocket(self, mock_websocket):
        """Test sending update when websocket is connected."""
        session = Session("test")
        session.websocket = mock_websocket

        await session.send_update({"type": "update", "data": "test"})

        mock_websocket.send_json.assert_called_once_with({"type": "update", "data": "test"})

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_send_update_without_websocket(self):
        """Test sending update when websocket is not connected."""
        session = Session("test")
        # Should not raise an error
        await session.send_update({"type": "update"})

    @pytest.mark.unit
    def test_queue_update(self):
        """Test queuing updates."""
        session = Session("test")

        session.queue_update({"type": "update1"})
        session.queue_update({"type": "update2"})

        assert len(session._pending_updates) == 2

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_flush_updates(self, mock_websocket):
        """Test flushing queued updates."""
        session = Session("test")
        session.websocket = mock_websocket

        session.queue_update({"type": "update1"})
        session.queue_update({"type": "update2"})

        await session.flush_updates()

        assert mock_websocket.send_json.call_count == 2
        assert len(session._pending_updates) == 0


class TestUmaraApp:
    """Tests for UmaraApp class."""

    @pytest.mark.unit
    def test_app_creation(self):
        """Test app initialization."""
        app = UmaraApp(title="My App")

        assert app.title == "My App"
        assert app.sessions == {}
        assert app._app_func is None

    @pytest.mark.unit
    def test_create_session(self, app):
        """Test session creation."""
        session = app.create_session("session-1")

        assert session.id == "session-1"
        assert "session-1" in app.sessions
        assert app.sessions["session-1"] == session

    @pytest.mark.unit
    def test_create_session_auto_id(self, app):
        """Test session creation with auto-generated ID."""
        session = app.create_session()

        assert session.id is not None
        assert len(session.id) > 0
        assert session.id in app.sessions

    @pytest.mark.unit
    def test_get_session(self, app):
        """Test getting session by ID."""
        created = app.create_session("test-id")

        retrieved = app.get_session("test-id")
        assert retrieved == created

        not_found = app.get_session("nonexistent")
        assert not_found is None

    @pytest.mark.unit
    def test_remove_session(self, app):
        """Test session removal."""
        app.create_session("to-remove")
        assert "to-remove" in app.sessions

        app.remove_session("to-remove")
        assert "to-remove" not in app.sessions

    @pytest.mark.unit
    def test_set_app_function(self, app):
        """Test setting the app function."""

        def my_app():
            pass

        app.set_app_function(my_app)
        assert app._app_func == my_app

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_render_session_no_app_func(self, app, session):
        """Test rendering when no app function is set."""
        result = await app.render_session(session)

        # When no app function, returns minimal dict
        assert "id" in result or "tree" in result

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_render_session_with_app_func(self, app, session):
        """Test rendering with app function."""

        def simple_app():
            from umara import text

            text("Hello World")

        app.set_app_function(simple_app)
        result = await app.render_session(session)

        assert "tree" in result
        assert "theme" in result
        assert "state" in result

    @pytest.mark.unit
    def test_on_start_decorator(self, app):
        """Test on_start decorator."""

        @app.on_start
        def startup():
            pass

        assert startup in app._on_start

    @pytest.mark.unit
    def test_on_stop_decorator(self, app):
        """Test on_stop decorator."""

        @app.on_stop
        def shutdown():
            pass

        assert shutdown in app._on_stop

    @pytest.mark.unit
    @pytest.mark.asyncio
    async def test_handle_state_update(self, app, session):
        """Test handling state updates."""

        def simple_app():
            pass

        app.set_app_function(simple_app)

        await app.handle_state_update(session, "my_key", "my_value")

        assert hasattr(session.state, "my_key")
        assert session.state.my_key == "my_value"


class TestContainerContext:
    """Tests for ContainerContext class."""

    @pytest.mark.unit
    def test_container_context_enter_exit(self, component_context):
        """Test container context manager."""
        component = component_context.create_component(type="card", props={})

        with ContainerContext(component) as ctx:
            assert ctx.component == component
            assert component_context._stack[-1] == component

        assert component not in component_context._stack

    @pytest.mark.unit
    def test_nested_container_contexts(self, component_context):
        """Test nested container contexts."""
        outer = component_context.create_component(type="container", props={})
        inner = component_context.create_component(type="card", props={})

        with ContainerContext(outer):
            child1 = component_context.create_component(type="text", props={})

            with ContainerContext(inner):
                child2 = component_context.create_component(type="text", props={})

            child3 = component_context.create_component(type="text", props={})

        assert child1 in outer.children
        assert child2 in inner.children
        assert child3 in outer.children


class TestExceptions:
    """Tests for custom exceptions."""

    @pytest.mark.unit
    def test_rerun_exception(self):
        """Test RerunException can be raised and caught."""
        with pytest.raises(RerunException):
            raise RerunException()

    @pytest.mark.unit
    def test_stop_exception(self):
        """Test StopException can be raised and caught."""
        with pytest.raises(StopException):
            raise StopException()


class TestGlobalFunctions:
    """Tests for global functions."""

    @pytest.mark.unit
    def test_get_context(self):
        """Test get_context returns a context."""
        ctx = get_context()
        assert isinstance(ctx, ComponentContext)

    @pytest.mark.unit
    def test_set_context(self):
        """Test set_context changes the context."""
        new_ctx = ComponentContext()
        set_context(new_ctx)

        assert get_context() == new_ctx

    @pytest.mark.unit
    def test_get_app(self):
        """Test get_app returns an app instance."""
        app = get_app()
        assert isinstance(app, UmaraApp)
