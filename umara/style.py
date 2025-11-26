"""
Inline styling system for Umara.

Provides a CSS-like syntax for styling components without
needing to know CSS.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Style:
    """
    A style object that can be applied to components.

    Provides a Pythonic way to define CSS-like styles.
    """

    _properties: dict[str, str] = field(default_factory=dict)

    def __init__(self, **kwargs):
        self._properties = {}
        for key, value in kwargs.items():
            # Convert Python naming to CSS naming
            css_key = self._to_css_key(key)
            self._properties[css_key] = self._to_css_value(value)

    def _to_css_key(self, key: str) -> str:
        """Convert Python snake_case to CSS kebab-case."""
        return key.replace("_", "-")

    def _to_css_value(self, value: Any) -> str:
        """Convert Python value to CSS value."""
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        return str(value)

    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith("_"):
            object.__setattr__(self, key, value)
        else:
            css_key = self._to_css_key(key)
            self._properties[css_key] = self._to_css_value(value)

    def __getattr__(self, key: str) -> str | None:
        if key.startswith("_"):
            return object.__getattribute__(self, key)
        css_key = self._to_css_key(key)
        return self._properties.get(css_key)

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for JSON serialization."""
        return self._properties.copy()

    def to_css(self) -> str:
        """Convert to inline CSS string."""
        return "; ".join(f"{k}: {v}" for k, v in self._properties.items())

    def merge(self, other: Style) -> Style:
        """Merge with another style, other takes precedence."""
        merged = Style()
        merged._properties = {**self._properties, **other._properties}
        return merged

    def __or__(self, other: Style) -> Style:
        """Allow style1 | style2 syntax for merging."""
        return self.merge(other)


def style(**kwargs) -> Style:
    """
    Create a style object for component styling.

    Supports CSS properties using Python naming conventions
    (snake_case instead of kebab-case).

    Args:
        **kwargs: CSS properties as keyword arguments

    Returns:
        Style object

    Example:
        um.text('Hello', style=um.style(
            color='#333',
            font_size='18px',
            font_weight='bold',
            margin_bottom='16px'
        ))

    Common Properties:
        Layout:
            - width, height, min_width, max_width, min_height, max_height
            - margin, margin_top, margin_right, margin_bottom, margin_left
            - padding, padding_top, padding_right, padding_bottom, padding_left
            - display, flex_direction, justify_content, align_items, gap

        Typography:
            - color, font_size, font_weight, font_family
            - text_align, line_height, letter_spacing

        Background:
            - background, background_color, background_image

        Border:
            - border, border_radius, border_color, border_width

        Effects:
            - box_shadow, opacity, cursor
            - transition, transform
    """
    return Style(**kwargs)


# Preset styles for common patterns
class Presets:
    """Pre-built style presets for common patterns."""

    @staticmethod
    def card(padding: str = "24px", radius: str = "12px", shadow: str = "md") -> Style:
        """Card preset with shadow and rounded corners."""
        shadow_values = {
            "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
            "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
            "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)",
            "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)",
        }
        return Style(
            padding=padding,
            border_radius=radius,
            box_shadow=shadow_values.get(shadow, shadow),
            background="var(--um-color-surface)",
        )

    @staticmethod
    def centered() -> Style:
        """Center content horizontally and vertically."""
        return Style(
            display="flex",
            justify_content="center",
            align_items="center",
        )

    @staticmethod
    def flex_row(gap: str = "16px", wrap: bool = False) -> Style:
        """Horizontal flex layout."""
        return Style(
            display="flex",
            flex_direction="row",
            gap=gap,
            flex_wrap="wrap" if wrap else "nowrap",
        )

    @staticmethod
    def flex_column(gap: str = "16px") -> Style:
        """Vertical flex layout."""
        return Style(
            display="flex",
            flex_direction="column",
            gap=gap,
        )

    @staticmethod
    def text_gradient(start: str, end: str, direction: str = "to right") -> Style:
        """Apply a gradient to text."""
        return Style(
            background=f"linear-gradient({direction}, {start}, {end})",
            background_clip="text",
            _webkit_background_clip="text",
            color="transparent",
        )

    @staticmethod
    def glass(blur: str = "10px", opacity: float = 0.8) -> Style:
        """Glassmorphism effect."""
        return Style(
            background=f"rgba(255, 255, 255, {opacity})",
            backdrop_filter=f"blur({blur})",
            _webkit_backdrop_filter=f"blur({blur})",
            border="1px solid rgba(255, 255, 255, 0.2)",
        )

    @staticmethod
    def hover_lift() -> Style:
        """Subtle lift effect on hover (applied via CSS class)."""
        return Style(
            transition="transform 0.2s ease, box-shadow 0.2s ease",
            cursor="pointer",
        )


# Export presets
presets = Presets()
