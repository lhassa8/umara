"""
Pytest configuration and shared fixtures for Umara tests.
"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from unittest.mock import MagicMock, AsyncMock

from umara.core import (
    UmaraApp,
    Session,
    ComponentContext,
    Component,
    get_context,
    set_context,
)
from umara.state import SessionState, set_session_state
from umara.themes import set_theme, get_theme


@pytest.fixture
def app() -> UmaraApp:
    """Create a fresh UmaraApp instance."""
    return UmaraApp(title="Test App")


@pytest.fixture
def session(app: UmaraApp) -> Session:
    """Create a fresh session."""
    return app.create_session("test-session-id")


@pytest.fixture
def component_context() -> Generator[ComponentContext, None, None]:
    """Create and set up a component context for testing."""
    ctx = ComponentContext()
    set_context(ctx)
    yield ctx
    # Reset context after test
    set_context(ComponentContext())


@pytest.fixture
def session_state() -> Generator[SessionState, None, None]:
    """Create and set up session state for testing."""
    state = SessionState()
    set_session_state(state)
    yield state


@pytest.fixture
def mock_websocket() -> AsyncMock:
    """Create a mock WebSocket connection."""
    ws = AsyncMock()
    ws.send_json = AsyncMock()
    ws.receive_json = AsyncMock()
    ws.close = AsyncMock()
    return ws


@pytest.fixture(autouse=True)
def reset_theme():
    """Reset theme before each test."""
    set_theme("light")
    yield


@pytest.fixture
def sample_component() -> Component:
    """Create a sample component for testing."""
    return Component(
        id="test-component-1",
        type="button",
        props={"label": "Test Button", "variant": "primary"},
        children=[],
        style={"color": "blue"},
        events={"click": "on_click"},
    )


@pytest.fixture
def sample_data() -> list:
    """Sample data for dataframe/chart tests."""
    return [
        {"name": "Alice", "age": 30, "city": "NYC"},
        {"name": "Bob", "age": 25, "city": "LA"},
        {"name": "Carol", "age": 35, "city": "Chicago"},
    ]


@pytest.fixture
def chart_data() -> list:
    """Sample data for chart tests."""
    return [
        {"month": "Jan", "revenue": 10000, "profit": 2000},
        {"month": "Feb", "revenue": 25000, "profit": 5000},
        {"month": "Mar", "revenue": 45000, "profit": 12000},
    ]


class MockWebSocketClient:
    """Mock WebSocket client for integration testing."""

    def __init__(self):
        self.messages_sent: list = []
        self.messages_received: list = []
        self.is_connected: bool = False

    async def connect(self):
        self.is_connected = True

    async def disconnect(self):
        self.is_connected = False

    async def send(self, message: dict):
        self.messages_sent.append(message)

    async def receive(self) -> dict:
        if self.messages_received:
            return self.messages_received.pop(0)
        return {}

    def add_response(self, message: dict):
        self.messages_received.append(message)


@pytest.fixture
def mock_ws_client() -> MockWebSocketClient:
    """Create a mock WebSocket client."""
    return MockWebSocketClient()
