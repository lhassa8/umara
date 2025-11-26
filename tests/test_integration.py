"""
Integration tests for Umara WebSocket communication and server.
"""

import pytest

from umara.core import UmaraApp
from umara.server import create_fastapi_app


class TestWebSocketIntegration:
    """Integration tests for WebSocket communication."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_session_lifecycle(self, app):
        """Test complete session lifecycle."""
        # Create session
        session = app.create_session("integration-test")
        assert session.id == "integration-test"
        assert app.get_session("integration-test") is not None

        # Remove session
        app.remove_session("integration-test")
        assert app.get_session("integration-test") is None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_app_render_cycle(self, app, session):
        """Test complete render cycle."""
        render_count = 0

        def test_app():
            nonlocal render_count
            render_count += 1
            from umara import button, text

            text("Hello")
            button("Click")

        app.set_app_function(test_app)

        # First render
        result1 = await app.render_session(session)
        assert "tree" in result1
        assert "theme" in result1
        assert render_count == 1

        # Second render (simulating re-render)
        await app.render_session(session)
        assert render_count == 2

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_state_update_triggers_rerender(self, app, session):
        """Test that state updates trigger re-renders."""

        def test_app():
            from umara import text
            from umara.state import get_session_state

            ss = get_session_state()
            count = ss.get("count", 0)
            text(f"Count: {count}")

        app.set_app_function(test_app)

        # Initial render
        result1 = await app.render_session(session)
        result1["tree"]

        # Update state
        result2 = await app.handle_state_update(session, "count", 5)
        result2["tree"]

        # Verify state was updated
        assert session.state.count == 5

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_event_handler_registration(self, app, session):
        """Test event handler registration and invocation."""
        handler_called = False
        handler_payload = None

        def my_handler(payload):
            nonlocal handler_called, handler_payload
            handler_called = True
            handler_payload = payload

        session.register_handler("btn-1:click", my_handler)

        # Simulate event
        await app.handle_event(
            session,
            event_type="click",
            component_id="btn-1",
            payload={"value": "test"},
        )

        assert handler_called
        assert handler_payload == {"value": "test"}

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_websocket_message_flow(self, app, session, mock_websocket):
        """Test WebSocket message send/receive flow."""
        session.websocket = mock_websocket

        # Queue multiple updates
        session.queue_update({"type": "render", "data": 1})
        session.queue_update({"type": "render", "data": 2})

        # Flush updates
        await session.flush_updates()

        # Verify messages were sent
        assert mock_websocket.send_json.call_count == 2

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_concurrent_sessions(self, app):
        """Test handling multiple concurrent sessions."""
        sessions = []
        for i in range(10):
            s = app.create_session(f"session-{i}")
            sessions.append(s)

        assert len(app.sessions) == 10

        # Each session should be independent
        sessions[0].state.value = "session0"
        sessions[1].state.value = "session1"

        assert sessions[0].state.value != sessions[1].state.value

        # Cleanup
        for s in sessions:
            app.remove_session(s.id)

        assert len(app.sessions) == 0

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_error_handling_in_app(self, app, session):
        """Test error handling when app function raises."""

        def buggy_app():
            raise ValueError("Something went wrong!")

        app.set_app_function(buggy_app)

        # Should not raise, but should return error in tree
        result = await app.render_session(session)

        # Find error component in tree
        tree = result["tree"]
        error_found = any(child.get("type") == "error" for child in tree.get("children", []))
        assert error_found


class TestServerIntegration:
    """Integration tests for the FastAPI server."""

    @pytest.mark.integration
    def test_create_app(self):
        """Test FastAPI app creation."""
        umara_app = UmaraApp(title="Test")
        fastapi_app = create_fastapi_app(umara_app)

        assert fastapi_app is not None

    @pytest.mark.integration
    def test_app_routes_exist(self):
        """Test that required routes are registered."""
        umara_app = UmaraApp(title="Test")
        fastapi_app = create_fastapi_app(umara_app)

        routes = [r.path for r in fastapi_app.routes]

        # Check essential routes exist
        assert "/" in routes or "/{path:path}" in routes


class TestComponentIntegration:
    """Integration tests for component rendering."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_nested_components_render(self, app, session):
        """Test deeply nested components render correctly."""

        def nested_app():
            from umara import card, column, columns, container, text

            with container():
                with card(title="Card 1"):
                    with columns(2):
                        with column():
                            text("Left")
                        with column():
                            text("Right")

        app.set_app_function(nested_app)
        result = await app.render_session(session)

        tree = result["tree"]
        assert tree["children"][0]["type"] == "container"

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_interactive_component_state(self, app, session):
        """Test interactive components maintain state."""

        def interactive_app():
            from umara import button, input
            from umara.state import get_session_state

            ss = get_session_state()
            name = input("Name", default=ss.get("name", ""), key="name")

            if button("Submit"):
                ss.name = name

        app.set_app_function(interactive_app)

        # Initial render
        await app.render_session(session)

        # Simulate state update
        await app.handle_state_update(session, "name", "Alice")

        # Re-render
        await app.render_session(session)

        assert session.state.name == "Alice"

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_theme_applied_to_render(self, app, session):
        """Test that theme is included in render output."""
        from umara.themes import set_theme

        def themed_app():
            from umara import text

            text("Themed text")

        app.set_app_function(themed_app)

        set_theme("dark")
        result = await app.render_session(session)

        assert "theme" in result
        assert result["theme"]["name"] == "dark"


class TestEndToEndScenarios:
    """End-to-end test scenarios."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_dashboard_app_scenario(self, app, session):
        """Test a dashboard-like application."""

        def dashboard_app():
            from umara import column, columns, dataframe, header, line_chart, stat_card

            header("Dashboard")

            with columns(3):
                with column():
                    stat_card("Users", "12.5K", trend=12.3)
                with column():
                    stat_card("Revenue", "$48K", trend=8.1)
                with column():
                    stat_card("Growth", "23%", trend=-2.4)

            data = [
                {"month": "Jan", "value": 100},
                {"month": "Feb", "value": 200},
            ]
            line_chart(data, x="month", y="value")

            dataframe(
                [
                    {"Name": "Alice", "Role": "Engineer"},
                    {"Name": "Bob", "Role": "Designer"},
                ]
            )

        app.set_app_function(dashboard_app)
        result = await app.render_session(session)

        tree = result["tree"]
        assert len(tree["children"]) > 0

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_form_submission_scenario(self, app, session):
        """Test a form submission scenario."""

        def form_app():
            from umara import button, card, input, success
            from umara.state import get_session_state

            ss = get_session_state()

            with card(title="Contact Form"):
                name = input("Name", key="name")
                email = input("Email", key="email")

                if button("Submit"):
                    ss.submitted = True
                    ss.form_data = {"name": name, "email": email}

                if ss.get("submitted"):
                    success("Form submitted!")

        app.set_app_function(form_app)

        # Initial render
        await app.render_session(session)

        # Simulate form input
        await app.handle_state_update(session, "name", "John")
        await app.handle_state_update(session, "email", "john@example.com")

        # Final render
        result = await app.render_session(session)
        assert "tree" in result

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_chat_interface_scenario(self, app, session):
        """Test a chat interface scenario."""

        def chat_app():
            from umara import chat_container, chat_input, chat_message
            from umara.state import get_session_state

            ss = get_session_state()
            messages = ss.get("messages", [{"role": "assistant", "content": "Hello!"}])

            with chat_container(height="400px"):
                for msg in messages:
                    chat_message(msg["role"], msg["content"])

            chat_input("Type a message...", key="chat_input")

        app.set_app_function(chat_app)
        result = await app.render_session(session)

        tree = result["tree"]
        # Should have chat_container as first child
        assert any(child.get("type") == "chat_container" for child in tree.get("children", []))
