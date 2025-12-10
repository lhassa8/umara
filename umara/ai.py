"""
AI/LLM Integration Helpers for Umara.

Provides advanced streaming support, token counting, and helpers for
building AI-powered applications. Goes beyond Streamlit's basic
write_stream to provide true first-class AI integration.

Example:
    import umara as um
    from umara.ai import stream_chat, AIMessage

    messages = [AIMessage("user", "Tell me a joke")]
    response = stream_chat(messages, provider="openai", model="gpt-4")
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Generator,
    Iterator,
    Literal,
    TypeVar,
)

from umara.components import write_stream, chat_message
from umara.core import get_context


@dataclass
class AIMessage:
    """
    Represents a message in a chat conversation.

    Compatible with OpenAI, Anthropic, and other LLM APIs.
    """

    role: Literal["system", "user", "assistant", "function", "tool"]
    content: str
    name: str | None = None
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None

    def to_openai(self) -> dict[str, Any]:
        """Convert to OpenAI message format."""
        msg: dict[str, Any] = {"role": self.role, "content": self.content}
        if self.name:
            msg["name"] = self.name
        if self.tool_calls:
            msg["tool_calls"] = self.tool_calls
        if self.tool_call_id:
            msg["tool_call_id"] = self.tool_call_id
        return msg

    def to_anthropic(self) -> dict[str, Any]:
        """Convert to Anthropic message format."""
        return {"role": self.role, "content": self.content}

    @classmethod
    def system(cls, content: str) -> "AIMessage":
        """Create a system message."""
        return cls("system", content)

    @classmethod
    def user(cls, content: str) -> "AIMessage":
        """Create a user message."""
        return cls("user", content)

    @classmethod
    def assistant(cls, content: str) -> "AIMessage":
        """Create an assistant message."""
        return cls("assistant", content)


@dataclass
class StreamMetrics:
    """Metrics collected during streaming."""

    tokens_generated: int = 0
    start_time: float = 0.0
    end_time: float = 0.0
    chunks_received: int = 0

    @property
    def duration(self) -> float:
        """Total streaming duration in seconds."""
        if self.end_time == 0:
            return time.time() - self.start_time
        return self.end_time - self.start_time

    @property
    def tokens_per_second(self) -> float:
        """Streaming speed in tokens per second."""
        if self.duration == 0:
            return 0.0
        return self.tokens_generated / self.duration


@dataclass
class StreamResult:
    """Result of a streaming operation."""

    content: str
    metrics: StreamMetrics
    finish_reason: str | None = None
    tool_calls: list[dict] | None = None

    def __str__(self) -> str:
        return self.content


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text (rough approximation).

    Uses the ~4 characters per token heuristic.
    For accurate counts, use the tiktoken library.

    Args:
        text: Text to estimate tokens for

    Returns:
        Estimated token count
    """
    return max(1, len(text) // 4)


def stream_with_metrics(
    stream: Iterator[Any] | Generator[Any, None, None],
    *,
    on_token: Callable[[str, StreamMetrics], None] | None = None,
) -> tuple[str, StreamMetrics]:
    """
    Process a stream and collect metrics.

    Args:
        stream: Iterator yielding stream chunks
        on_token: Optional callback for each token

    Returns:
        Tuple of (full_response, metrics)

    Example:
        stream = openai_client.chat.completions.create(
            model="gpt-4", messages=msgs, stream=True
        )
        response, metrics = stream_with_metrics(stream)
        print(f"Generated {metrics.tokens_generated} tokens in {metrics.duration:.2f}s")
    """
    metrics = StreamMetrics(start_time=time.time())
    chunks = []

    for chunk in stream:
        # Extract text from different stream formats
        if isinstance(chunk, str):
            text = chunk
        elif hasattr(chunk, "choices"):
            # OpenAI format
            delta = chunk.choices[0].delta if chunk.choices else None
            text = delta.content if delta and hasattr(delta, "content") and delta.content else ""
        elif hasattr(chunk, "text"):
            # Anthropic format
            text = chunk.text if chunk.text else ""
        elif hasattr(chunk, "content"):
            text = chunk.content if chunk.content else ""
        else:
            text = str(chunk)

        if text:
            chunks.append(text)
            metrics.chunks_received += 1
            metrics.tokens_generated += estimate_tokens(text)

            if on_token:
                on_token(text, metrics)

    metrics.end_time = time.time()
    return "".join(chunks), metrics


async def async_stream_with_metrics(
    stream: AsyncIterator[Any],
    *,
    on_token: Callable[[str, StreamMetrics], None] | None = None,
) -> tuple[str, StreamMetrics]:
    """
    Process an async stream and collect metrics.

    Args:
        stream: Async iterator yielding stream chunks
        on_token: Optional callback for each token

    Returns:
        Tuple of (full_response, metrics)

    Example:
        async with openai_client.chat.completions.create(
            model="gpt-4", messages=msgs, stream=True
        ) as stream:
            response, metrics = await async_stream_with_metrics(stream)
    """
    metrics = StreamMetrics(start_time=time.time())
    chunks = []

    async for chunk in stream:
        # Extract text from different stream formats
        if isinstance(chunk, str):
            text = chunk
        elif hasattr(chunk, "choices"):
            delta = chunk.choices[0].delta if chunk.choices else None
            text = delta.content if delta and hasattr(delta, "content") and delta.content else ""
        elif hasattr(chunk, "text"):
            text = chunk.text if chunk.text else ""
        elif hasattr(chunk, "content"):
            text = chunk.content if chunk.content else ""
        else:
            text = str(chunk)

        if text:
            chunks.append(text)
            metrics.chunks_received += 1
            metrics.tokens_generated += estimate_tokens(text)

            if on_token:
                on_token(text, metrics)

    metrics.end_time = time.time()
    return "".join(chunks), metrics


def write_stream_with_stats(
    stream: Any,
    *,
    key: str | None = None,
    show_stats: bool = True,
) -> StreamResult:
    """
    Stream content to the UI with optional statistics display.

    Enhances write_stream with metrics collection and display.

    Args:
        stream: Stream iterator
        key: Component key
        show_stats: Whether to show streaming statistics after completion

    Returns:
        StreamResult with content and metrics

    Example:
        result = um.ai.write_stream_with_stats(stream)
        print(f"Tokens: {result.metrics.tokens_generated}")
    """
    from umara.components import caption

    metrics = StreamMetrics(start_time=time.time())
    content = write_stream(stream, key=key)
    metrics.end_time = time.time()
    metrics.tokens_generated = estimate_tokens(content)

    if show_stats:
        caption(
            f"Generated ~{metrics.tokens_generated} tokens "
            f"in {metrics.duration:.1f}s "
            f"({metrics.tokens_per_second:.0f} tok/s)"
        )

    return StreamResult(content=content, metrics=metrics)


def chat_stream(
    stream: Any,
    *,
    role: str = "assistant",
    avatar: str | None = None,
    name: str | None = None,
) -> str:
    """
    Stream a chat response with automatic chat message styling.

    Combines chat_message container with write_stream for seamless
    AI chat responses.

    Args:
        stream: Stream iterator from LLM API
        role: Message role (assistant, user, etc.)
        avatar: Optional avatar URL or emoji
        name: Optional display name

    Returns:
        Complete response text

    Example:
        with um.chat_container():
            um.chat_message("user", content="Tell me a joke")

            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Tell me a joke"}],
                stream=True
            )
            response = um.ai.chat_stream(stream)
    """
    ctx = get_context()

    # Create chat message container
    props = {
        "role": role,
        "avatar": avatar,
        "name": name or role.title(),
        "streaming": True,
    }

    component = ctx.create_component("chat_message", props=props)
    ctx.push(component)

    try:
        # Stream content inside the chat message
        response = write_stream(stream)
    finally:
        ctx.pop()

    # Update to mark as not streaming
    ctx.update_component(component.id, {"streaming": False})

    return response


def simulate_stream(
    text: str,
    *,
    chunk_size: int = 10,
    delay: float = 0.02,
) -> Generator[str, None, None]:
    """
    Create a simulated stream from static text.

    Useful for testing and demos without an LLM API.

    Args:
        text: Full text to stream
        chunk_size: Characters per chunk
        delay: Delay between chunks in seconds

    Yields:
        Text chunks

    Example:
        # Demo streaming without API calls
        stream = um.ai.simulate_stream("Hello, how can I help you today?")
        um.write_stream(stream)
    """
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]
        time.sleep(delay)


async def async_simulate_stream(
    text: str,
    *,
    chunk_size: int = 10,
    delay: float = 0.02,
) -> AsyncIterator[str]:
    """
    Create an async simulated stream from static text.

    Args:
        text: Full text to stream
        chunk_size: Characters per chunk
        delay: Delay between chunks in seconds

    Yields:
        Text chunks
    """
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]
        await asyncio.sleep(delay)


# =============================================================================
# Provider-Specific Helpers
# =============================================================================


def extract_openai_content(chunk: Any) -> str:
    """Extract text content from OpenAI stream chunk."""
    if not hasattr(chunk, "choices") or not chunk.choices:
        return ""
    delta = chunk.choices[0].delta
    return delta.content or "" if hasattr(delta, "content") else ""


def extract_anthropic_content(chunk: Any) -> str:
    """Extract text content from Anthropic stream chunk."""
    if hasattr(chunk, "type"):
        if chunk.type == "content_block_delta":
            return chunk.delta.text if hasattr(chunk.delta, "text") else ""
    return ""


def extract_google_content(chunk: Any) -> str:
    """Extract text content from Google Gemini stream chunk."""
    if hasattr(chunk, "text"):
        return chunk.text or ""
    return ""


def create_openai_stream_adapter(stream: Any) -> Generator[str, None, None]:
    """
    Adapt OpenAI stream to yield plain strings.

    Args:
        stream: OpenAI streaming response

    Yields:
        Text content from each chunk
    """
    for chunk in stream:
        text = extract_openai_content(chunk)
        if text:
            yield text


def create_anthropic_stream_adapter(stream: Any) -> Generator[str, None, None]:
    """
    Adapt Anthropic stream to yield plain strings.

    Args:
        stream: Anthropic streaming response

    Yields:
        Text content from each chunk
    """
    for chunk in stream:
        text = extract_anthropic_content(chunk)
        if text:
            yield text


# =============================================================================
# Typing Effect
# =============================================================================


def typewriter(
    text: str,
    *,
    speed: float = 0.03,
    key: str | None = None,
) -> str:
    """
    Display text with a typewriter effect.

    Args:
        text: Text to display
        speed: Delay between characters in seconds
        key: Component key

    Returns:
        The complete text

    Example:
        um.ai.typewriter("Hello! How can I help you today?")
    """
    stream = simulate_stream(text, chunk_size=1, delay=speed)
    return write_stream(stream, key=key)


# =============================================================================
# Thinking/Reasoning Display
# =============================================================================


def show_thinking(
    content: str,
    *,
    collapsed: bool = True,
    title: str = "Thinking...",
) -> None:
    """
    Display AI thinking/reasoning in a collapsible container.

    Useful for showing chain-of-thought or reasoning steps.

    Args:
        content: Thinking content to display
        collapsed: Whether to show collapsed by default
        title: Title for the expander

    Example:
        um.ai.show_thinking("Let me break this down:\\n1. First...")
    """
    from umara.components import expander, markdown

    with expander(title, expanded=not collapsed):
        markdown(content)


# =============================================================================
# Cost Estimation
# =============================================================================


# Pricing per 1M tokens (approximate, as of late 2024)
MODEL_PRICING = {
    # OpenAI
    "gpt-4": {"input": 30.0, "output": 60.0},
    "gpt-4-turbo": {"input": 10.0, "output": 30.0},
    "gpt-4o": {"input": 5.0, "output": 15.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.6},
    "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
    # Anthropic
    "claude-3-opus": {"input": 15.0, "output": 75.0},
    "claude-3-sonnet": {"input": 3.0, "output": 15.0},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    "claude-3.5-sonnet": {"input": 3.0, "output": 15.0},
}


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str,
) -> float:
    """
    Estimate API cost for a request.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        model: Model name

    Returns:
        Estimated cost in USD

    Example:
        cost = um.ai.estimate_cost(500, 1000, "gpt-4")
        print(f"Estimated cost: ${cost:.4f}")
    """
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        # Default fallback pricing
        pricing = {"input": 1.0, "output": 2.0}

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return input_cost + output_cost
