"""
Theming system for Umara.

Provides beautiful default themes and easy customization through
design tokens for colors, spacing, typography, and more.
"""

from __future__ import annotations

import copy
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColorPalette:
    """Color palette with semantic color tokens."""

    # Primary colors
    primary: str = "#6366f1"  # Indigo
    primary_hover: str = "#4f46e5"
    primary_active: str = "#4338ca"
    primary_light: str = "#e0e7ff"
    primary_dark: str = "#3730a3"

    # Secondary colors
    secondary: str = "#64748b"  # Slate
    secondary_hover: str = "#475569"
    secondary_active: str = "#334155"
    secondary_light: str = "#f1f5f9"
    secondary_dark: str = "#1e293b"

    # Accent colors
    accent: str = "#f59e0b"  # Amber
    accent_hover: str = "#d97706"
    accent_active: str = "#b45309"
    accent_light: str = "#fef3c7"

    # Semantic colors
    success: str = "#10b981"  # Emerald
    success_light: str = "#d1fae5"
    success_dark: str = "#047857"

    warning: str = "#f59e0b"  # Amber
    warning_light: str = "#fef3c7"
    warning_dark: str = "#b45309"

    error: str = "#ef4444"  # Red
    error_light: str = "#fee2e2"
    error_dark: str = "#b91c1c"

    info: str = "#3b82f6"  # Blue
    info_light: str = "#dbeafe"
    info_dark: str = "#1d4ed8"

    # Background colors
    background: str = "#ffffff"
    background_secondary: str = "#f8fafc"
    background_tertiary: str = "#f1f5f9"

    # Surface colors (cards, modals, etc.)
    surface: str = "#ffffff"
    surface_hover: str = "#f8fafc"
    surface_active: str = "#f1f5f9"

    # Border colors
    border: str = "#e2e8f0"
    border_hover: str = "#cbd5e1"
    border_focus: str = "#6366f1"

    # Text colors
    text: str = "#0f172a"
    text_secondary: str = "#475569"
    text_tertiary: str = "#94a3b8"
    text_inverse: str = "#ffffff"
    text_disabled: str = "#cbd5e1"

    # Overlay
    overlay: str = "rgba(15, 23, 42, 0.5)"


@dataclass
class Spacing:
    """Spacing scale using a consistent multiplier."""

    base: int = 4  # 4px base unit
    xs: str = "4px"
    sm: str = "8px"
    md: str = "16px"
    lg: str = "24px"
    xl: str = "32px"
    xxl: str = "48px"
    xxxl: str = "64px"


@dataclass
class Typography:
    """Typography settings."""

    # Font families
    font_family: str = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    font_family_mono: str = "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace"

    # Font sizes
    text_xs: str = "0.75rem"  # 12px
    text_sm: str = "0.875rem"  # 14px
    text_base: str = "1rem"  # 16px
    text_lg: str = "1.125rem"  # 18px
    text_xl: str = "1.25rem"  # 20px
    text_2xl: str = "1.5rem"  # 24px
    text_3xl: str = "1.875rem"  # 30px
    text_4xl: str = "2.25rem"  # 36px
    text_5xl: str = "3rem"  # 48px

    # Font weights
    font_light: int = 300
    font_normal: int = 400
    font_medium: int = 500
    font_semibold: int = 600
    font_bold: int = 700

    # Line heights
    leading_none: float = 1.0
    leading_tight: float = 1.25
    leading_snug: float = 1.375
    leading_normal: float = 1.5
    leading_relaxed: float = 1.625
    leading_loose: float = 2.0

    # Letter spacing
    tracking_tighter: str = "-0.05em"
    tracking_tight: str = "-0.025em"
    tracking_normal: str = "0"
    tracking_wide: str = "0.025em"
    tracking_wider: str = "0.05em"


@dataclass
class Borders:
    """Border settings."""

    radius_none: str = "0"
    radius_sm: str = "4px"
    radius_md: str = "8px"
    radius_lg: str = "12px"
    radius_xl: str = "16px"
    radius_2xl: str = "24px"
    radius_full: str = "9999px"

    width_none: str = "0"
    width_thin: str = "1px"
    width_medium: str = "2px"
    width_thick: str = "4px"


@dataclass
class Shadows:
    """Shadow presets for depth."""

    none: str = "none"
    sm: str = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    md: str = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)"
    lg: str = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)"
    xl: str = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)"
    xxl: str = "0 25px 50px -12px rgba(0, 0, 0, 0.25)"
    inner: str = "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)"

    # Colored shadows for buttons/cards
    primary: str = "0 4px 14px 0 rgba(99, 102, 241, 0.4)"
    success: str = "0 4px 14px 0 rgba(16, 185, 129, 0.4)"
    error: str = "0 4px 14px 0 rgba(239, 68, 68, 0.4)"


@dataclass
class Transitions:
    """Animation and transition settings."""

    duration_fast: str = "150ms"
    duration_normal: str = "200ms"
    duration_slow: str = "300ms"
    duration_slower: str = "500ms"

    easing_default: str = "cubic-bezier(0.4, 0, 0.2, 1)"
    easing_in: str = "cubic-bezier(0.4, 0, 1, 1)"
    easing_out: str = "cubic-bezier(0, 0, 0.2, 1)"
    easing_in_out: str = "cubic-bezier(0.4, 0, 0.2, 1)"
    easing_bounce: str = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"


@dataclass
class Theme:
    """Complete theme configuration."""

    name: str = "light"
    colors: ColorPalette = field(default_factory=ColorPalette)
    spacing: Spacing = field(default_factory=Spacing)
    typography: Typography = field(default_factory=Typography)
    borders: Borders = field(default_factory=Borders)
    shadows: Shadows = field(default_factory=Shadows)
    transitions: Transitions = field(default_factory=Transitions)

    def to_css_variables(self) -> dict[str, str]:
        """Convert theme to CSS custom properties."""
        variables = {}

        # Colors
        for key, value in self.colors.__dict__.items():
            css_key = f"--um-color-{key.replace('_', '-')}"
            variables[css_key] = value

        # Spacing
        for key, value in self.spacing.__dict__.items():
            if key != "base":
                css_key = f"--um-spacing-{key.replace('_', '-')}"
                variables[css_key] = value

        # Typography
        variables["--um-font-family"] = self.typography.font_family
        variables["--um-font-family-mono"] = self.typography.font_family_mono
        for key, value in self.typography.__dict__.items():
            if key.startswith("text_"):
                css_key = f"--um-{key.replace('_', '-')}"
                variables[css_key] = value
            elif key.startswith("font_") and key != "font_family" and key != "font_family_mono":
                css_key = f"--um-{key.replace('_', '-')}"
                variables[css_key] = str(value)
            elif key.startswith("leading_"):
                css_key = f"--um-{key.replace('_', '-')}"
                variables[css_key] = str(value)

        # Borders
        for key, value in self.borders.__dict__.items():
            css_key = f"--um-{key.replace('_', '-')}"
            variables[css_key] = value

        # Shadows
        for key, value in self.shadows.__dict__.items():
            css_key = f"--um-shadow-{key.replace('_', '-')}"
            variables[css_key] = value

        # Transitions
        for key, value in self.transitions.__dict__.items():
            css_key = f"--um-{key.replace('_', '-')}"
            variables[css_key] = value

        return variables

    def to_dict(self) -> dict[str, Any]:
        """Convert theme to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "colors": self.colors.__dict__,
            "spacing": self.spacing.__dict__,
            "typography": self.typography.__dict__,
            "borders": self.borders.__dict__,
            "shadows": self.shadows.__dict__,
            "transitions": self.transitions.__dict__,
        }


# Built-in themes
def _create_light_theme() -> Theme:
    """Create the default light theme."""
    return Theme(name="light")


def _create_dark_theme() -> Theme:
    """Create a dark theme."""
    colors = ColorPalette(
        # Primary colors (slightly adjusted for dark mode)
        primary="#818cf8",
        primary_hover="#a5b4fc",
        primary_active="#6366f1",
        primary_light="#312e81",
        primary_dark="#c7d2fe",
        # Secondary colors
        secondary="#94a3b8",
        secondary_hover="#cbd5e1",
        secondary_active="#64748b",
        secondary_light="#1e293b",
        secondary_dark="#e2e8f0",
        # Accent
        accent="#fbbf24",
        accent_hover="#fcd34d",
        accent_active="#f59e0b",
        accent_light="#451a03",
        # Semantic colors
        success="#34d399",
        success_light="#064e3b",
        success_dark="#6ee7b7",
        warning="#fbbf24",
        warning_light="#451a03",
        warning_dark="#fcd34d",
        error="#f87171",
        error_light="#450a0a",
        error_dark="#fca5a5",
        info="#60a5fa",
        info_light="#1e3a5f",
        info_dark="#93c5fd",
        # Backgrounds
        background="#0f172a",
        background_secondary="#1e293b",
        background_tertiary="#334155",
        # Surfaces
        surface="#1e293b",
        surface_hover="#334155",
        surface_active="#475569",
        # Borders
        border="#334155",
        border_hover="#475569",
        border_focus="#818cf8",
        # Text
        text="#f8fafc",
        text_secondary="#cbd5e1",
        text_tertiary="#64748b",
        text_inverse="#0f172a",
        text_disabled="#475569",
        # Overlay
        overlay="rgba(0, 0, 0, 0.7)",
    )

    shadows = Shadows(
        sm="0 1px 2px 0 rgba(0, 0, 0, 0.3)",
        md="0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3)",
        lg="0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -4px rgba(0, 0, 0, 0.3)",
        xl="0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.3)",
        xxl="0 25px 50px -12px rgba(0, 0, 0, 0.5)",
        primary="0 4px 14px 0 rgba(129, 140, 248, 0.3)",
        success="0 4px 14px 0 rgba(52, 211, 153, 0.3)",
        error="0 4px 14px 0 rgba(248, 113, 113, 0.3)",
    )

    return Theme(name="dark", colors=colors, shadows=shadows)


def _create_ocean_theme() -> Theme:
    """Create an ocean-inspired theme."""
    colors = ColorPalette(
        # Primary - Ocean blue
        primary="#0ea5e9",
        primary_hover="#0284c7",
        primary_active="#0369a1",
        primary_light="#e0f2fe",
        primary_dark="#075985",
        # Secondary - Teal
        secondary="#14b8a6",
        secondary_hover="#0d9488",
        secondary_active="#0f766e",
        secondary_light="#ccfbf1",
        secondary_dark="#115e59",
        # Accent - Coral
        accent="#f97316",
        accent_hover="#ea580c",
        accent_active="#c2410c",
        accent_light="#ffedd5",
        # Backgrounds - Subtle blue tint
        background="#f0f9ff",
        background_secondary="#e0f2fe",
        background_tertiary="#bae6fd",
        # Surfaces
        surface="#ffffff",
        surface_hover="#f0f9ff",
        surface_active="#e0f2fe",
        # Borders
        border="#bae6fd",
        border_hover="#7dd3fc",
        border_focus="#0ea5e9",
        # Text
        text="#0c4a6e",
        text_secondary="#0369a1",
        text_tertiary="#0284c7",
    )

    shadows = Shadows(
        primary="0 4px 14px 0 rgba(14, 165, 233, 0.4)",
        success="0 4px 14px 0 rgba(20, 184, 166, 0.4)",
    )

    return Theme(name="ocean", colors=colors, shadows=shadows)


def _create_forest_theme() -> Theme:
    """Create a forest-inspired theme."""
    colors = ColorPalette(
        # Primary - Forest green
        primary="#059669",
        primary_hover="#047857",
        primary_active="#065f46",
        primary_light="#d1fae5",
        primary_dark="#064e3b",
        # Secondary - Earthy brown
        secondary="#78716c",
        secondary_hover="#57534e",
        secondary_active="#44403c",
        secondary_light="#f5f5f4",
        secondary_dark="#292524",
        # Accent - Golden
        accent="#ca8a04",
        accent_hover="#a16207",
        accent_active="#854d0e",
        accent_light="#fef9c3",
        # Backgrounds - Warm cream
        background="#fefdf8",
        background_secondary="#fef9e7",
        background_tertiary="#fef3c7",
        # Surfaces
        surface="#ffffff",
        surface_hover="#fefdf8",
        surface_active="#fef9e7",
        # Borders
        border="#d6d3d1",
        border_hover="#a8a29e",
        border_focus="#059669",
        # Text
        text="#1c1917",
        text_secondary="#44403c",
        text_tertiary="#78716c",
    )

    shadows = Shadows(
        primary="0 4px 14px 0 rgba(5, 150, 105, 0.4)",
    )

    return Theme(name="forest", colors=colors, shadows=shadows)


def _create_slate_theme() -> Theme:
    """Create a sophisticated corporate gray theme."""
    colors = ColorPalette(
        # Primary - Slate blue
        primary="#475569",
        primary_hover="#334155",
        primary_active="#1e293b",
        primary_light="#e2e8f0",
        primary_dark="#0f172a",
        # Secondary - Cool gray
        secondary="#6b7280",
        secondary_hover="#4b5563",
        secondary_active="#374151",
        secondary_light="#f3f4f6",
        secondary_dark="#1f2937",
        # Accent - Professional blue
        accent="#3b82f6",
        accent_hover="#2563eb",
        accent_active="#1d4ed8",
        accent_light="#dbeafe",
        # Backgrounds
        background="#f8fafc",
        background_secondary="#f1f5f9",
        background_tertiary="#e2e8f0",
        # Surfaces
        surface="#ffffff",
        surface_hover="#f8fafc",
        surface_active="#f1f5f9",
        # Borders
        border="#e2e8f0",
        border_hover="#cbd5e1",
        border_focus="#475569",
        # Text
        text="#0f172a",
        text_secondary="#334155",
        text_tertiary="#64748b",
    )

    shadows = Shadows(
        primary="0 4px 14px 0 rgba(71, 85, 105, 0.35)",
    )

    return Theme(name="slate", colors=colors, shadows=shadows)


def _create_nord_theme() -> Theme:
    """Create a theme inspired by the Nord color palette - arctic, clean, professional."""
    colors = ColorPalette(
        # Primary - Nord blue
        primary="#5e81ac",
        primary_hover="#81a1c1",
        primary_active="#4c566a",
        primary_light="#e5e9f0",
        primary_dark="#2e3440",
        # Secondary - Nord frost
        secondary="#88c0d0",
        secondary_hover="#8fbcbb",
        secondary_active="#81a1c1",
        secondary_light="#eceff4",
        secondary_dark="#4c566a",
        # Accent - Nord aurora (purple)
        accent="#b48ead",
        accent_hover="#a3be8c",
        accent_active="#bf616a",
        accent_light="#e5e9f0",
        # Backgrounds - Nord snow
        background="#eceff4",
        background_secondary="#e5e9f0",
        background_tertiary="#d8dee9",
        # Surfaces
        surface="#ffffff",
        surface_hover="#eceff4",
        surface_active="#e5e9f0",
        # Borders
        border="#d8dee9",
        border_hover="#4c566a",
        border_focus="#5e81ac",
        # Text - Nord polar night
        text="#2e3440",
        text_secondary="#3b4252",
        text_tertiary="#4c566a",
        # Semantic colors - Nord aurora
        success="#a3be8c",
        success_light="#e5e9f0",
        success_dark="#8fbf8f",
        warning="#ebcb8b",
        warning_light="#eceff4",
        warning_dark="#d08770",
        error="#bf616a",
        error_light="#e5e9f0",
        error_dark="#a54e56",
        info="#81a1c1",
        info_light="#e5e9f0",
        info_dark="#5e81ac",
    )

    shadows = Shadows(
        primary="0 4px 14px 0 rgba(94, 129, 172, 0.35)",
        success="0 4px 14px 0 rgba(163, 190, 140, 0.35)",
        error="0 4px 14px 0 rgba(191, 97, 106, 0.35)",
    )

    return Theme(name="nord", colors=colors, shadows=shadows)


def _create_midnight_theme() -> Theme:
    """Create a deep purple/indigo dark theme for analytics dashboards."""
    colors = ColorPalette(
        # Primary - Vibrant indigo
        primary="#a78bfa",
        primary_hover="#c4b5fd",
        primary_active="#8b5cf6",
        primary_light="#2e1065",
        primary_dark="#ddd6fe",
        # Secondary - Muted purple
        secondary="#a1a1aa",
        secondary_hover="#d4d4d8",
        secondary_active="#71717a",
        secondary_light="#27272a",
        secondary_dark="#e4e4e7",
        # Accent - Electric cyan
        accent="#22d3ee",
        accent_hover="#67e8f9",
        accent_active="#06b6d4",
        accent_light="#164e63",
        # Backgrounds - Deep purple-black
        background="#0c0a1d",
        background_secondary="#1a1730",
        background_tertiary="#2d2a45",
        # Surfaces
        surface="#1a1730",
        surface_hover="#2d2a45",
        surface_active="#3d3a5a",
        # Borders
        border="#3d3a5a",
        border_hover="#4d4a6a",
        border_focus="#a78bfa",
        # Text
        text="#faf5ff",
        text_secondary="#d8b4fe",
        text_tertiary="#a78bfa",
        text_inverse="#0c0a1d",
        text_disabled="#4d4a6a",
        # Semantic
        success="#4ade80",
        success_light="#14532d",
        success_dark="#86efac",
        warning="#fbbf24",
        warning_light="#451a03",
        warning_dark="#fcd34d",
        error="#f87171",
        error_light="#450a0a",
        error_dark="#fca5a5",
        info="#60a5fa",
        info_light="#1e3a5f",
        info_dark="#93c5fd",
        # Overlay
        overlay="rgba(12, 10, 29, 0.8)",
    )

    shadows = Shadows(
        sm="0 1px 2px 0 rgba(0, 0, 0, 0.4)",
        md="0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -2px rgba(0, 0, 0, 0.4)",
        lg="0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4)",
        xl="0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.4)",
        xxl="0 25px 50px -12px rgba(0, 0, 0, 0.6)",
        primary="0 4px 14px 0 rgba(167, 139, 250, 0.4)",
        success="0 4px 14px 0 rgba(74, 222, 128, 0.3)",
        error="0 4px 14px 0 rgba(248, 113, 113, 0.3)",
    )

    return Theme(name="midnight", colors=colors, shadows=shadows)


def _create_rose_theme() -> Theme:
    """Create a warm, modern rose/pink theme for fintech and consumer apps."""
    colors = ColorPalette(
        # Primary - Rose
        primary="#e11d48",
        primary_hover="#be123c",
        primary_active="#9f1239",
        primary_light="#ffe4e6",
        primary_dark="#881337",
        # Secondary - Warm gray
        secondary="#78716c",
        secondary_hover="#57534e",
        secondary_active="#44403c",
        secondary_light="#f5f5f4",
        secondary_dark="#292524",
        # Accent - Coral
        accent="#fb7185",
        accent_hover="#f43f5e",
        accent_active="#e11d48",
        accent_light="#fff1f2",
        # Backgrounds - Subtle rose tint
        background="#fff1f2",
        background_secondary="#ffe4e6",
        background_tertiary="#fecdd3",
        # Surfaces
        surface="#ffffff",
        surface_hover="#fff1f2",
        surface_active="#ffe4e6",
        # Borders
        border="#fecdd3",
        border_hover="#fda4af",
        border_focus="#e11d48",
        # Text
        text="#1c1917",
        text_secondary="#44403c",
        text_tertiary="#78716c",
    )

    shadows = Shadows(
        primary="0 4px 14px 0 rgba(225, 29, 72, 0.35)",
    )

    return Theme(name="rose", colors=colors, shadows=shadows)


def _create_copper_theme() -> Theme:
    """Create a warm, premium theme with copper and earth tones for luxury/finance apps."""
    colors = ColorPalette(
        # Primary - Copper/Bronze
        primary="#b45309",
        primary_hover="#92400e",
        primary_active="#78350f",
        primary_light="#fef3c7",
        primary_dark="#451a03",
        # Secondary - Stone
        secondary="#78716c",
        secondary_hover="#57534e",
        secondary_active="#44403c",
        secondary_light="#f5f5f4",
        secondary_dark="#292524",
        # Accent - Gold
        accent="#d97706",
        accent_hover="#b45309",
        accent_active="#92400e",
        accent_light="#fef9c3",
        # Backgrounds - Warm cream
        background="#fffbeb",
        background_secondary="#fef3c7",
        background_tertiary="#fde68a",
        # Surfaces
        surface="#ffffff",
        surface_hover="#fffbeb",
        surface_active="#fef3c7",
        # Borders
        border="#fde68a",
        border_hover="#fcd34d",
        border_focus="#b45309",
        # Text
        text="#1c1917",
        text_secondary="#44403c",
        text_tertiary="#78716c",
    )

    shadows = Shadows(
        primary="0 4px 14px 0 rgba(180, 83, 9, 0.35)",
    )

    return Theme(name="copper", colors=colors, shadows=shadows)


def _create_lavender_theme() -> Theme:
    """Create a calming lavender theme for healthcare, wellness, and creative apps."""
    colors = ColorPalette(
        # Primary - Violet
        primary="#7c3aed",
        primary_hover="#6d28d9",
        primary_active="#5b21b6",
        primary_light="#ede9fe",
        primary_dark="#4c1d95",
        # Secondary - Cool gray
        secondary="#6b7280",
        secondary_hover="#4b5563",
        secondary_active="#374151",
        secondary_light="#f3f4f6",
        secondary_dark="#1f2937",
        # Accent - Fuchsia
        accent="#c026d3",
        accent_hover="#a21caf",
        accent_active="#86198f",
        accent_light="#fae8ff",
        # Backgrounds - Soft purple tint
        background="#faf5ff",
        background_secondary="#f3e8ff",
        background_tertiary="#e9d5ff",
        # Surfaces
        surface="#ffffff",
        surface_hover="#faf5ff",
        surface_active="#f3e8ff",
        # Borders
        border="#e9d5ff",
        border_hover="#d8b4fe",
        border_focus="#7c3aed",
        # Text
        text="#1f2937",
        text_secondary="#4b5563",
        text_tertiary="#6b7280",
    )

    shadows = Shadows(
        primary="0 4px 14px 0 rgba(124, 58, 237, 0.35)",
    )

    return Theme(name="lavender", colors=colors, shadows=shadows)


def _create_sunset_theme() -> Theme:
    """Create a warm, energetic orange theme for creative and marketing tools."""
    colors = ColorPalette(
        # Primary - Vibrant orange
        primary="#ea580c",
        primary_hover="#c2410c",
        primary_active="#9a3412",
        primary_light="#ffedd5",
        primary_dark="#7c2d12",
        # Secondary - Warm stone
        secondary="#78716c",
        secondary_hover="#57534e",
        secondary_active="#44403c",
        secondary_light="#f5f5f4",
        secondary_dark="#292524",
        # Accent - Amber
        accent="#f59e0b",
        accent_hover="#d97706",
        accent_active="#b45309",
        accent_light="#fef3c7",
        # Backgrounds - Warm orange tint
        background="#fff7ed",
        background_secondary="#ffedd5",
        background_tertiary="#fed7aa",
        # Surfaces
        surface="#ffffff",
        surface_hover="#fff7ed",
        surface_active="#ffedd5",
        # Borders
        border="#fed7aa",
        border_hover="#fdba74",
        border_focus="#ea580c",
        # Text
        text="#1c1917",
        text_secondary="#44403c",
        text_tertiary="#78716c",
    )

    shadows = Shadows(
        primary="0 4px 14px 0 rgba(234, 88, 12, 0.35)",
    )

    return Theme(name="sunset", colors=colors, shadows=shadows)


def _create_mint_theme() -> Theme:
    """Create a fresh, modern teal/mint theme for tech startups and SaaS apps."""
    colors = ColorPalette(
        # Primary - Teal
        primary="#0d9488",
        primary_hover="#0f766e",
        primary_active="#115e59",
        primary_light="#ccfbf1",
        primary_dark="#134e4a",
        # Secondary - Cool gray
        secondary="#6b7280",
        secondary_hover="#4b5563",
        secondary_active="#374151",
        secondary_light="#f3f4f6",
        secondary_dark="#1f2937",
        # Accent - Cyan
        accent="#06b6d4",
        accent_hover="#0891b2",
        accent_active="#0e7490",
        accent_light="#cffafe",
        # Backgrounds - Fresh mint tint
        background="#f0fdfa",
        background_secondary="#ccfbf1",
        background_tertiary="#99f6e4",
        # Surfaces
        surface="#ffffff",
        surface_hover="#f0fdfa",
        surface_active="#ccfbf1",
        # Borders
        border="#99f6e4",
        border_hover="#5eead4",
        border_focus="#0d9488",
        # Text
        text="#134e4a",
        text_secondary="#115e59",
        text_tertiary="#0f766e",
    )

    shadows = Shadows(
        primary="0 4px 14px 0 rgba(13, 148, 136, 0.35)",
    )

    return Theme(name="mint", colors=colors, shadows=shadows)


# Theme registry
BUILTIN_THEMES: dict[str, Theme] = {
    "light": _create_light_theme(),
    "dark": _create_dark_theme(),
    "ocean": _create_ocean_theme(),
    "forest": _create_forest_theme(),
    "slate": _create_slate_theme(),
    "nord": _create_nord_theme(),
    "midnight": _create_midnight_theme(),
    "rose": _create_rose_theme(),
    "copper": _create_copper_theme(),
    "lavender": _create_lavender_theme(),
    "sunset": _create_sunset_theme(),
    "mint": _create_mint_theme(),
}

# Custom themes added by users
_custom_themes: dict[str, Theme] = {}

# Current theme context
_current_theme: ContextVar[Theme] = ContextVar("current_theme", default=BUILTIN_THEMES["light"])


def set_theme(theme: str | Theme) -> None:
    """
    Set the current theme.

    Args:
        theme: Either a theme name ('light', 'dark', 'ocean', 'forest')
               or a Theme instance.
    """
    if isinstance(theme, str):
        if theme in BUILTIN_THEMES:
            _current_theme.set(BUILTIN_THEMES[theme])
        elif theme in _custom_themes:
            _current_theme.set(_custom_themes[theme])
        else:
            available = list(BUILTIN_THEMES.keys()) + list(_custom_themes.keys())
            raise ValueError(f"Unknown theme '{theme}'. Available: {available}")
    elif isinstance(theme, Theme):
        _current_theme.set(theme)
    else:
        raise TypeError(f"Expected str or Theme, got {type(theme)}")


def get_theme() -> Theme:
    """Get the current theme."""
    return _current_theme.get()


def create_theme(name: str, base: str = "light", **overrides) -> Theme:
    """
    Create a custom theme based on an existing theme.

    Args:
        name: Name for the new theme
        base: Base theme to extend ('light', 'dark', 'ocean', 'forest')
        **overrides: Override specific theme values

    Returns:
        New Theme instance

    Example:
        um.create_theme(
            'my-theme',
            base='dark',
            colors={'primary': '#ff6b6b', 'accent': '#4ecdc4'}
        )
    """
    if base not in BUILTIN_THEMES and base not in _custom_themes:
        raise ValueError(f"Unknown base theme '{base}'")

    base_theme = BUILTIN_THEMES.get(base) or _custom_themes[base]
    new_theme = copy.deepcopy(base_theme)
    new_theme.name = name

    # Apply overrides
    for key, value in overrides.items():
        if key == "colors" and isinstance(value, dict):
            for color_key, color_value in value.items():
                if hasattr(new_theme.colors, color_key):
                    setattr(new_theme.colors, color_key, color_value)
        elif key == "spacing" and isinstance(value, dict):
            for spacing_key, spacing_value in value.items():
                if hasattr(new_theme.spacing, spacing_key):
                    setattr(new_theme.spacing, spacing_key, spacing_value)
        elif key == "typography" and isinstance(value, dict):
            for typo_key, typo_value in value.items():
                if hasattr(new_theme.typography, typo_key):
                    setattr(new_theme.typography, typo_key, typo_value)
        elif key == "borders" and isinstance(value, dict):
            for border_key, border_value in value.items():
                if hasattr(new_theme.borders, border_key):
                    setattr(new_theme.borders, border_key, border_value)
        elif key == "shadows" and isinstance(value, dict):
            for shadow_key, shadow_value in value.items():
                if hasattr(new_theme.shadows, shadow_key):
                    setattr(new_theme.shadows, shadow_key, shadow_value)

    # Register the theme
    _custom_themes[name] = new_theme
    return new_theme


def list_themes() -> list[str]:
    """List all available theme names."""
    return list(BUILTIN_THEMES.keys()) + list(_custom_themes.keys())
