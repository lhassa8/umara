"""
Tests for the advanced caching module.
"""

from __future__ import annotations

import asyncio
import time

import pytest

from umara.cache import (
    CacheEntry,
    CacheManager,
    CacheStats,
    async_cache,
    cache,
    cache_embedding,
    cache_llm_response,
    cache_resource,
    clear_all_caches,
    cleanup_expired,
    get_cache_stats,
    memoize,
)


class TestCacheEntry:
    """Tests for CacheEntry dataclass."""

    def test_cache_entry_creation(self):
        """Test creating a cache entry."""
        entry = CacheEntry(value="test", created_at=time.time(), expires_at=None)
        assert entry.value == "test"
        assert entry.hits == 0
        assert entry.expires_at is None

    def test_cache_entry_with_expiration(self):
        """Test cache entry with expiration time."""
        expires = time.time() + 60.0
        entry = CacheEntry(value="test", created_at=time.time(), expires_at=expires)
        assert entry.expires_at == expires

    def test_cache_entry_is_expired(self):
        """Test cache entry expiration."""
        # Entry with no expiration never expires
        entry = CacheEntry(value="test", created_at=time.time(), expires_at=None)
        assert not entry.is_expired

        # Entry with future expiration is not expired
        entry_future = CacheEntry(
            value="test", created_at=time.time(), expires_at=time.time() + 3600
        )
        assert not entry_future.is_expired

        # Entry with past expiration is expired
        entry_past = CacheEntry(
            value="test", created_at=time.time() - 100, expires_at=time.time() - 10
        )
        assert entry_past.is_expired

    def test_cache_entry_hit(self):
        """Test cache entry hit counter."""
        entry = CacheEntry(value="test", created_at=time.time(), expires_at=None)
        assert entry.hits == 0
        entry.hit()
        assert entry.hits == 1
        entry.hit()
        assert entry.hits == 2


class TestCacheStats:
    """Tests for CacheStats dataclass."""

    def test_cache_stats_defaults(self):
        """Test default cache stats."""
        stats = CacheStats()
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.entry_count == 0

    def test_cache_stats_hit_rate(self):
        """Test hit rate calculation."""
        stats = CacheStats(hits=75, misses=25, entry_count=100)
        assert stats.hit_rate == 0.75

        # Test zero total
        empty_stats = CacheStats()
        assert empty_stats.hit_rate == 0.0

    def test_cache_stats_to_dict(self):
        """Test stats to dict conversion."""
        stats = CacheStats(hits=10, misses=5)
        d = stats.to_dict()
        assert isinstance(d, dict)
        assert d["hits"] == 10
        assert d["misses"] == 5


class TestCacheManager:
    """Tests for CacheManager singleton."""

    def test_singleton_pattern(self):
        """Test that CacheManager is a singleton."""
        manager1 = CacheManager()
        manager2 = CacheManager()
        assert manager1 is manager2

    def test_get_namespace(self):
        """Test getting/creating namespaces."""
        manager = CacheManager()
        ns1 = manager.get_namespace("test_ns")
        ns2 = manager.get_namespace("test_ns")
        assert ns1 is ns2

    def test_clear_all(self):
        """Test clearing all namespaces."""
        manager = CacheManager()
        ns = manager.get_namespace("clear_test")
        ns.set("key", "value")
        manager.clear_all()
        # After clear, get returns (False, None)
        found, value = ns.get("key")
        assert not found or value is None


class TestCacheDecorator:
    """Tests for the @cache decorator."""

    def test_basic_caching(self):
        """Test basic function caching."""
        call_count = 0

        @cache()
        def expensive_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        result1 = expensive_func(5)
        assert result1 == 10
        assert call_count == 1

        # Second call with same arg - should be cached
        result2 = expensive_func(5)
        assert result2 == 10
        assert call_count == 1  # Not incremented

        # Different arg - new call
        result3 = expensive_func(10)
        assert result3 == 20
        assert call_count == 2

    def test_cache_with_ttl(self):
        """Test cache with TTL expiration."""
        call_count = 0

        @cache(ttl=0.1)  # 100ms TTL
        def short_lived(x):
            nonlocal call_count
            call_count += 1
            return x

        result1 = short_lived(1)
        assert result1 == 1
        assert call_count == 1

        # Immediate second call - cached
        result2 = short_lived(1)
        assert call_count == 1

        # Wait for TTL to expire
        time.sleep(0.15)

        # Should be a new call
        result3 = short_lived(1)
        assert call_count == 2

    def test_cache_clear(self):
        """Test clearing cache via clear_all_caches."""
        call_count = 0

        @cache(namespace="clear_decorator_test")
        def cached_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call
        cached_func(5)
        assert call_count == 1

        # Cached
        cached_func(5)
        assert call_count == 1

        # Clear all caches
        clear_all_caches()

        # Should be a new call after clearing
        cached_func(5)
        assert call_count == 2


class TestMemoize:
    """Tests for the @memoize decorator."""

    def test_memoize_basic(self):
        """Test basic memoization."""
        call_count = 0

        @memoize
        def fib(n):
            nonlocal call_count
            call_count += 1
            if n <= 1:
                return n
            return fib(n - 1) + fib(n - 2)

        result = fib(10)
        assert result == 55
        # Without memoization, this would be many more calls
        assert call_count <= 11  # At most n+1 unique calls


class TestCacheResource:
    """Tests for the @cache_resource decorator."""

    def test_resource_caching(self):
        """Test resource caching."""
        call_count = 0

        @cache_resource()
        def get_resource():
            nonlocal call_count
            call_count += 1
            return {"connection": "active"}

        resource1 = get_resource()
        resource2 = get_resource()

        assert resource1 is resource2  # Same object
        assert call_count == 1


class TestAsyncCache:
    """Tests for the @async_cache decorator."""

    @pytest.mark.asyncio
    async def test_async_caching(self):
        """Test async function caching."""
        call_count = 0

        @async_cache()
        async def async_fetch(url):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)
            return f"data from {url}"

        result1 = await async_fetch("http://example.com")
        result2 = await async_fetch("http://example.com")

        assert result1 == result2
        assert call_count == 1


class TestAICaching:
    """Tests for AI-specific cache decorators."""

    def test_cache_embedding(self):
        """Test embedding cache decorator."""
        call_count = 0

        @cache_embedding()
        def get_embedding(text):
            nonlocal call_count
            call_count += 1
            return [0.1, 0.2, 0.3]

        emb1 = get_embedding("hello")
        emb2 = get_embedding("hello")

        assert emb1 == emb2
        assert call_count == 1

    def test_cache_llm_response(self):
        """Test LLM response cache decorator."""
        call_count = 0

        @cache_llm_response()
        def get_response(prompt):
            nonlocal call_count
            call_count += 1
            return "AI response"

        resp1 = get_response("What is Python?")
        resp2 = get_response("What is Python?")

        assert resp1 == resp2
        assert call_count == 1


class TestCacheUtilities:
    """Tests for cache utility functions."""

    def test_clear_all_caches(self):
        """Test clearing all caches."""
        call_count = 0

        @cache(namespace="util_test_clear")
        def cached_func(x):
            nonlocal call_count
            call_count += 1
            return x

        cached_func(1)
        assert call_count == 1

        # Cached
        cached_func(1)
        assert call_count == 1

        clear_all_caches()

        # Should be called again after clear
        cached_func(1)
        assert call_count == 2

    def test_get_cache_stats(self):
        """Test getting cache statistics."""
        stats = get_cache_stats()
        assert isinstance(stats, dict)

    def test_cleanup_expired(self):
        """Test cleaning up expired entries."""
        @cache(ttl=0.01, namespace="cleanup_test")
        def expiring_func(x):
            return x

        expiring_func(1)
        time.sleep(0.05)  # Wait for TTL

        removed = cleanup_expired()
        assert isinstance(removed, int)
