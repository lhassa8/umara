"""
Tests for the fragments module (partial reruns).
"""

from __future__ import annotations

import time

import pytest

from umara.fragments import (
    FragmentConfig,
    FragmentGroup,
    FragmentManager,
    FragmentState,
    get_all_fragment_stats,
    poll,
)


class TestFragmentState:
    """Tests for FragmentState dataclass."""

    def test_fragment_state_creation(self):
        """Test creating a fragment state."""
        state = FragmentState(id="test_id", name="test_fragment")
        assert state.id == "test_id"
        assert state.name == "test_fragment"
        assert state.last_run == 0.0
        assert state.run_count == 0
        assert state.is_running is False
        assert state.error is None
        assert state.output is None

    def test_fragment_state_with_values(self):
        """Test fragment state with custom values."""
        state = FragmentState(
            id="test",
            name="test",
            last_run=100.0,
            run_count=5,
            is_running=True,
            output="result",
        )
        assert state.last_run == 100.0
        assert state.run_count == 5
        assert state.is_running is True
        assert state.output == "result"


class TestFragmentConfig:
    """Tests for FragmentConfig dataclass."""

    def test_fragment_config_defaults(self):
        """Test default config values."""
        config = FragmentConfig()
        assert config.run_every is None
        assert config.on_change is None
        assert config.debounce == 0.0

    def test_fragment_config_with_values(self):
        """Test config with custom values."""
        config = FragmentConfig(
            run_every=5.0,
            on_change=["key1", "key2"],
            debounce=0.5,
        )
        assert config.run_every == 5.0
        assert config.on_change == ["key1", "key2"]
        assert config.debounce == 0.5


class TestFragmentManager:
    """Tests for FragmentManager singleton."""

    def test_singleton_pattern(self):
        """Test that FragmentManager is a singleton."""
        manager1 = FragmentManager()
        manager2 = FragmentManager()
        assert manager1 is manager2

    def test_register_fragment(self):
        """Test registering a fragment."""
        manager = FragmentManager()
        config = FragmentConfig(run_every=10.0)
        state = manager.register("test_frag_1", "test_name", config)

        assert state.id == "test_frag_1"
        assert state.name == "test_name"

    def test_get_state(self):
        """Test getting fragment state."""
        manager = FragmentManager()
        config = FragmentConfig()
        manager.register("test_frag_2", "test", config)

        state = manager.get_state("test_frag_2")
        assert state is not None
        assert state.id == "test_frag_2"

        # Non-existent fragment
        assert manager.get_state("nonexistent") is None

    def test_mark_for_rerun(self):
        """Test marking fragment for rerun."""
        manager = FragmentManager()
        config = FragmentConfig()
        manager.register("rerun_test", "test", config)

        manager.mark_for_rerun("rerun_test")
        pending = manager.get_pending_reruns()

        assert "rerun_test" in pending

        # Should be cleared after get
        pending2 = manager.get_pending_reruns()
        assert "rerun_test" not in pending2

    def test_should_auto_rerun(self):
        """Test auto-rerun check."""
        manager = FragmentManager()

        # Fragment with run_every
        config = FragmentConfig(run_every=0.01)
        manager.register("auto_rerun_test", "test", config)
        manager.record_run("auto_rerun_test")

        # Should not rerun immediately
        assert not manager.should_auto_rerun("auto_rerun_test")

        # Wait for interval
        time.sleep(0.02)
        assert manager.should_auto_rerun("auto_rerun_test")

    def test_record_run(self):
        """Test recording a fragment run."""
        manager = FragmentManager()
        config = FragmentConfig()
        manager.register("record_test", "test", config)

        manager.record_run("record_test", output="result")
        state = manager.get_state("record_test")

        assert state.run_count == 1
        assert state.output == "result"
        assert state.last_run > 0
        assert not state.is_running

    def test_record_run_with_error(self):
        """Test recording a fragment run with error."""
        manager = FragmentManager()
        config = FragmentConfig()
        manager.register("error_test", "test", config)

        error = ValueError("test error")
        manager.record_run("error_test", error=error)
        state = manager.get_state("error_test")

        assert state.error is error


class TestFragmentGroup:
    """Tests for FragmentGroup."""

    def test_fragment_group_creation(self):
        """Test creating a fragment group."""
        group = FragmentGroup(name="test_group")
        assert group.name == "test_group"
        assert group.fragment_ids == []

    def test_fragment_group_rerun_all(self):
        """Test rerunning all fragments in a group."""
        group = FragmentGroup(name="rerun_group")
        manager = FragmentManager()

        # Manually add fragment IDs to simulate decorated functions
        group._fragment_ids.append("group:rerun_group:frag1")
        group._fragment_ids.append("group:rerun_group:frag2")

        # Register them
        config = FragmentConfig()
        manager.register("group:rerun_group:frag1", "frag1", config)
        manager.register("group:rerun_group:frag2", "frag2", config)

        group.rerun_all()
        pending = manager.get_pending_reruns()

        assert "group:rerun_group:frag1" in pending
        assert "group:rerun_group:frag2" in pending


class TestPollDecorator:
    """Tests for the poll decorator."""

    def test_poll_returns_decorator(self):
        """Test that poll returns a decorator."""
        decorator = poll(interval=5.0)
        assert callable(decorator)

    def test_poll_with_key(self):
        """Test poll with custom key."""
        decorator = poll(interval=10.0, key="custom_poll")
        assert callable(decorator)


class TestGetAllFragmentStats:
    """Tests for get_all_fragment_stats utility."""

    def test_get_all_fragment_stats(self):
        """Test getting all fragment statistics."""
        manager = FragmentManager()
        config = FragmentConfig(run_every=5.0)
        manager.register("stats_test", "test", config)
        manager.record_run("stats_test")

        stats = get_all_fragment_stats()
        assert isinstance(stats, dict)

        # Our fragment should be in stats
        assert "stats_test" in stats
        assert stats["stats_test"]["name"] == "test"
        assert stats["stats_test"]["run_count"] >= 1
        assert stats["stats_test"]["run_every"] == 5.0
