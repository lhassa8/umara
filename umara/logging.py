"""
Structured logging system for Umara.

Provides consistent, structured logging across the framework with
support for different output formats and log levels.
"""

from __future__ import annotations

import contextvars
import json
import logging
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Any

# Context variable for request/session tracking
_request_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)
_session_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("session_id", default=None)


class LogLevel(Enum):
    """Log levels matching Python's logging module."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


@dataclass
class LogContext:
    """Context information for structured logging."""

    request_id: str | None = None
    session_id: str | None = None
    component: str | None = None
    action: str | None = None
    duration_ms: float | None = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class LogRecord:
    """Structured log record."""

    timestamp: str
    level: str
    message: str
    logger: str
    context: LogContext
    exception: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "timestamp": self.timestamp,
            "level": self.level,
            "message": self.message,
            "logger": self.logger,
        }

        # Add context fields if present
        ctx = asdict(self.context)
        for key, value in ctx.items():
            if value is not None and value != {}:
                if key == "extra":
                    result.update(value)
                else:
                    result[key] = value

        if self.exception:
            result["exception"] = self.exception

        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


class StructuredFormatter(logging.Formatter):
    """Formatter that outputs structured JSON logs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        context = LogContext(
            request_id=_request_id.get(),
            session_id=_session_id.get(),
        )

        # Extract extra context from record
        if hasattr(record, "context"):
            extra_ctx = record.context
            if isinstance(extra_ctx, dict):
                context.extra.update(extra_ctx)
            elif isinstance(extra_ctx, LogContext):
                context = extra_ctx

        if hasattr(record, "component"):
            context.component = record.component

        if hasattr(record, "action"):
            context.action = record.action

        if hasattr(record, "duration_ms"):
            context.duration_ms = record.duration_ms

        exception_str = None
        if record.exc_info:
            exception_str = self.formatException(record.exc_info)

        log_record = LogRecord(
            timestamp=datetime.utcnow().isoformat() + "Z",
            level=record.levelname,
            message=record.getMessage(),
            logger=record.name,
            context=context,
            exception=exception_str,
        )

        return log_record.to_json()


class PrettyFormatter(logging.Formatter):
    """Formatter for human-readable console output."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def __init__(self, use_colors: bool = True):
        super().__init__()
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """Format log record for console."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        level = record.levelname

        if self.use_colors:
            color = self.COLORS.get(level, "")
            level_str = f"{color}{level:8}{self.RESET}"
        else:
            level_str = f"{level:8}"

        # Build the message
        parts = [f"{timestamp} {level_str} {record.getMessage()}"]

        # Add context info
        context_parts = []

        request_id = _request_id.get()
        if request_id:
            context_parts.append(f"req={request_id[:8]}")

        session_id = _session_id.get()
        if session_id:
            context_parts.append(f"session={session_id[:8]}")

        if hasattr(record, "component"):
            context_parts.append(f"component={record.component}")

        if hasattr(record, "duration_ms"):
            context_parts.append(f"duration={record.duration_ms:.2f}ms")

        if context_parts:
            parts.append(f"  [{', '.join(context_parts)}]")

        # Add exception if present
        if record.exc_info:
            parts.append("\n" + self.formatException(record.exc_info))

        return "".join(parts)


class UmaraLogger:
    """
    Main logger class for Umara framework.

    Provides structured logging with context tracking.
    """

    def __init__(
        self,
        name: str = "umara",
        level: LogLevel | int | str = LogLevel.INFO,
        json_output: bool = False,
    ):
        self.name = name
        self._logger = logging.getLogger(name)
        self._logger.setLevel(self._resolve_level(level))
        self._logger.handlers = []  # Clear existing handlers

        # Set up handler
        handler = logging.StreamHandler(sys.stdout)

        if json_output:
            handler.setFormatter(StructuredFormatter())
        else:
            handler.setFormatter(PrettyFormatter())

        self._logger.addHandler(handler)

    def _resolve_level(self, level: LogLevel | int | str) -> int:
        """Resolve log level to integer."""
        if isinstance(level, LogLevel):
            return level.value
        if isinstance(level, str):
            return getattr(logging, level.upper(), logging.INFO)
        return level

    def _log(
        self,
        level: int,
        message: str,
        *args,
        exc_info: bool = False,
        **kwargs,
    ):
        """Internal logging method."""
        extra = {}

        # Extract known kwargs
        if "component" in kwargs:
            extra["component"] = kwargs.pop("component")
        if "action" in kwargs:
            extra["action"] = kwargs.pop("action")
        if "duration_ms" in kwargs:
            extra["duration_ms"] = kwargs.pop("duration_ms")
        if "context" in kwargs:
            extra["context"] = kwargs.pop("context")

        # Remaining kwargs go into context
        if kwargs:
            if "context" not in extra:
                extra["context"] = {}
            extra["context"].update(kwargs)

        self._logger.log(level, message, *args, exc_info=exc_info, extra=extra)

    def debug(self, message: str, *args, **kwargs):
        """Log debug message."""
        self._log(logging.DEBUG, message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message."""
        self._log(logging.INFO, message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message."""
        self._log(logging.WARNING, message, *args, **kwargs)

    def error(self, message: str, *args, exc_info: bool = True, **kwargs):
        """Log error message."""
        self._log(logging.ERROR, message, *args, exc_info=exc_info, **kwargs)

    def critical(self, message: str, *args, exc_info: bool = True, **kwargs):
        """Log critical message."""
        self._log(logging.CRITICAL, message, *args, exc_info=exc_info, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback."""
        self._log(logging.ERROR, message, *args, exc_info=True, **kwargs)


# Global logger instance
_logger: UmaraLogger | None = None


def get_logger(name: str = "umara") -> UmaraLogger:
    """Get or create the global logger instance."""
    global _logger
    if _logger is None:
        _logger = UmaraLogger(name)
    return _logger


def configure_logging(
    level: LogLevel | int | str = LogLevel.INFO,
    json_output: bool = False,
    name: str = "umara",
) -> UmaraLogger:
    """
    Configure the global logger.

    Args:
        level: Log level
        json_output: If True, output structured JSON logs
        name: Logger name

    Returns:
        Configured logger instance
    """
    global _logger
    _logger = UmaraLogger(name=name, level=level, json_output=json_output)
    return _logger


def set_request_id(request_id: str) -> None:
    """Set the current request ID for logging context."""
    _request_id.set(request_id)


def set_session_id(session_id: str) -> None:
    """Set the current session ID for logging context."""
    _session_id.set(session_id)


def clear_context() -> None:
    """Clear logging context."""
    _request_id.set(None)
    _session_id.set(None)


def log_timing(logger: UmaraLogger | None = None, component: str = "unknown"):
    """
    Decorator to log function execution time.

    Args:
        logger: Logger instance (uses global if not provided)
        component: Component name for context

    Example:
        @log_timing(component="database")
        def fetch_data():
            ...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log = logger or get_logger()
            start_time = time.perf_counter()

            try:
                result = func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start_time) * 1000
                log.debug(
                    f"{func.__name__} completed",
                    component=component,
                    action=func.__name__,
                    duration_ms=duration_ms,
                )
                return result
            except Exception as e:
                duration_ms = (time.perf_counter() - start_time) * 1000
                log.error(
                    f"{func.__name__} failed: {e}",
                    component=component,
                    action=func.__name__,
                    duration_ms=duration_ms,
                )
                raise

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            log = logger or get_logger()
            start_time = time.perf_counter()

            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start_time) * 1000
                log.debug(
                    f"{func.__name__} completed",
                    component=component,
                    action=func.__name__,
                    duration_ms=duration_ms,
                )
                return result
            except Exception as e:
                duration_ms = (time.perf_counter() - start_time) * 1000
                log.error(
                    f"{func.__name__} failed: {e}",
                    component=component,
                    action=func.__name__,
                    duration_ms=duration_ms,
                )
                raise

        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    return decorator


# Convenience aliases
def debug(msg, **kw):
    return get_logger().debug(msg, **kw)


def info(msg, **kw):
    return get_logger().info(msg, **kw)


def warning(msg, **kw):
    return get_logger().warning(msg, **kw)


def error(msg, **kw):
    return get_logger().error(msg, **kw)


def critical(msg, **kw):
    return get_logger().critical(msg, **kw)
