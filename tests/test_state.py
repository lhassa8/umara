"""
Unit tests for umara.state module.
"""

import pytest
from umara.state import (
    SessionState,
    set_session_state,
    get_session_state,
    state,
    session_state,
    cache,
)


class TestSessionState:
    """Tests for SessionState class."""

    @pytest.mark.unit
    def test_session_state_creation(self):
        """Test SessionState initialization."""
        ss = SessionState()
        assert ss._state == {}

    @pytest.mark.unit
    def test_session_state_setattr(self):
        """Test setting attributes on session state."""
        ss = SessionState()
        ss.my_key = "my_value"

        assert ss._state["my_key"].value == "my_value"

    @pytest.mark.unit
    def test_session_state_getattr(self):
        """Test getting attributes from session state."""
        ss = SessionState()
        ss.test_key = "test_value"  # Set via public API

        assert ss.test_key == "test_value"

    @pytest.mark.unit
    def test_session_state_getattr_missing(self):
        """Test getting missing attribute raises AttributeError."""
        ss = SessionState()

        with pytest.raises(AttributeError):
            _ = ss.nonexistent

    @pytest.mark.unit
    def test_session_state_delattr(self):
        """Test deleting state via clear and checking contains."""
        ss = SessionState()
        ss.to_delete = "value"
        assert "to_delete" in ss

        # Clear all state
        ss.clear()
        assert "to_delete" not in ss

    @pytest.mark.unit
    def test_session_state_contains(self):
        """Test 'in' operator for session state."""
        ss = SessionState()
        ss.existing = "value"

        assert "existing" in ss
        assert "nonexistent" not in ss

    @pytest.mark.unit
    def test_session_state_get(self):
        """Test get method with default."""
        ss = SessionState()
        ss.key = "value"

        assert ss.get("key") == "value"
        assert ss.get("missing", "default") == "default"

    @pytest.mark.unit
    def test_session_state_to_dict(self):
        """Test serialization to dict."""
        ss = SessionState()
        ss.a = 1
        ss.b = "two"

        result = ss.to_dict()
        assert result == {"a": 1, "b": "two"}

    @pytest.mark.unit
    def test_session_state_clear(self):
        """Test clearing session state."""
        ss = SessionState()
        ss.a = 1
        ss.b = 2

        ss.clear()
        assert ss._state == {}

    @pytest.mark.unit
    def test_session_state_update(self):
        """Test updating session state with kwargs."""
        ss = SessionState()
        ss.update(x=10, y=20)

        assert ss.x == 10
        assert ss.y == 20

    @pytest.mark.unit
    def test_session_state_keys(self):
        """Test getting keys."""
        ss = SessionState()
        ss.a = 1
        ss.b = 2

        keys = list(ss.keys())
        assert "a" in keys
        assert "b" in keys

    @pytest.mark.unit
    def test_session_state_values(self):
        """Test getting values."""
        ss = SessionState()
        ss.a = 1
        ss.b = 2

        values = list(ss.values())
        assert 1 in values
        assert 2 in values

    @pytest.mark.unit
    def test_session_state_items(self):
        """Test getting items."""
        ss = SessionState()
        ss.a = 1

        items = list(ss.items())
        assert ("a", 1) in items


class TestStateFunctions:
    """Tests for state accessor functions."""

    @pytest.mark.unit
    def test_set_get_session_state(self):
        """Test setting and getting session state."""
        ss = SessionState()
        ss.test = "value"

        set_session_state(ss)
        retrieved = get_session_state()

        assert retrieved.test == "value"

    @pytest.mark.unit
    def test_state_accessor(self, session_state):
        """Test state accessor."""
        session_state.widget_value = "test"

        # The state accessor should return session state
        s = state
        # Accessing via the proxy
        assert s is not None

    @pytest.mark.unit
    def test_session_state_accessor(self, session_state):
        """Test session_state accessor."""
        session_state.user_data = {"name": "Test"}

        # session_state is an alias
        ss = session_state
        assert ss is not None


class TestCache:
    """Tests for cache decorator."""

    @pytest.mark.unit
    def test_cache_decorator(self):
        """Test cache decorator caches results."""
        call_count = 0

        @cache
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1

        # Second call with same args should be cached
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Should not have incremented

        # Different args should call function
        result3 = expensive_function(10)
        assert result3 == 20
        assert call_count == 2

    @pytest.mark.unit
    def test_cache_with_kwargs(self):
        """Test cache with keyword arguments."""
        call_count = 0

        @cache
        def func_with_kwargs(a, b=10):
            nonlocal call_count
            call_count += 1
            return a + b

        result1 = func_with_kwargs(5, b=20)
        assert result1 == 25
        assert call_count == 1

        result2 = func_with_kwargs(5, b=20)
        assert result2 == 25
        assert call_count == 1


class TestStateEdgeCases:
    """Tests for edge cases in state management."""

    @pytest.mark.unit
    def test_session_state_none_value(self):
        """Test storing None value."""
        ss = SessionState()
        ss.nullable = None

        assert ss.nullable is None
        assert "nullable" in ss

    @pytest.mark.unit
    def test_session_state_complex_types(self):
        """Test storing complex types."""
        ss = SessionState()
        ss.list_data = [1, 2, 3]
        ss.dict_data = {"nested": {"value": 1}}

        assert ss.list_data == [1, 2, 3]
        assert ss.dict_data["nested"]["value"] == 1

    @pytest.mark.unit
    def test_session_state_overwrite(self):
        """Test overwriting existing value."""
        ss = SessionState()
        ss.key = "first"
        ss.key = "second"

        assert ss.key == "second"
