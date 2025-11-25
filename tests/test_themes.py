"""
Unit tests for umara.themes module.
"""

import pytest
from umara.themes import (
    Theme,
    ColorPalette,
    set_theme,
    get_theme,
    create_theme,
    BUILTIN_THEMES,
)


class TestTheme:
    """Tests for Theme class."""

    @pytest.mark.unit
    def test_theme_creation(self):
        """Test basic theme creation."""
        theme = Theme(name="test")

        assert theme.name == "test"
        assert theme.colors is not None
        assert hasattr(theme.colors, "primary")

    @pytest.mark.unit
    def test_theme_with_custom_colors(self):
        """Test theme with custom color palette."""
        colors = ColorPalette(primary="#ff0000")
        theme = Theme(name="custom", colors=colors)

        assert theme.colors.primary == "#ff0000"

    @pytest.mark.unit
    def test_theme_to_dict(self):
        """Test theme serialization."""
        theme = Theme(name="test")

        result = theme.to_dict()
        assert result["name"] == "test"
        assert "colors" in result
        assert "spacing" in result

    @pytest.mark.unit
    def test_theme_to_css_variables(self):
        """Test CSS variable generation."""
        theme = Theme(name="test")
        css_vars = theme.to_css_variables()

        assert "--um-color-primary" in css_vars
        assert "--um-color-background" in css_vars

    @pytest.mark.unit
    def test_built_in_themes_exist(self):
        """Test that all built-in themes are defined."""
        expected_themes = ["light", "dark", "ocean", "forest"]
        for theme_name in expected_themes:
            assert theme_name in BUILTIN_THEMES


class TestThemeFunctions:
    """Tests for theme functions."""

    @pytest.mark.unit
    def test_set_theme_light(self):
        """Test setting light theme."""
        set_theme("light")
        theme = get_theme()

        assert theme.name == "light"

    @pytest.mark.unit
    def test_set_theme_dark(self):
        """Test setting dark theme."""
        set_theme("dark")
        theme = get_theme()

        assert theme.name == "dark"

    @pytest.mark.unit
    def test_set_theme_ocean(self):
        """Test setting ocean theme."""
        set_theme("ocean")
        theme = get_theme()

        assert theme.name == "ocean"

    @pytest.mark.unit
    def test_set_theme_forest(self):
        """Test setting forest theme."""
        set_theme("forest")
        theme = get_theme()

        assert theme.name == "forest"

    @pytest.mark.unit
    def test_set_invalid_theme(self):
        """Test setting invalid theme raises error."""
        with pytest.raises(ValueError):
            set_theme("nonexistent_theme")

    @pytest.mark.unit
    def test_get_theme_returns_theme(self):
        """Test get_theme returns Theme instance."""
        set_theme("light")
        theme = get_theme()

        assert isinstance(theme, Theme)

    @pytest.mark.unit
    def test_create_theme(self):
        """Test creating custom theme."""
        create_theme(
            "custom_test",
            base="dark",
            colors={
                "primary": "#ff6b6b",
                "accent": "#4ecdc4",
            },
        )

        set_theme("custom_test")
        theme = get_theme()

        assert theme.name == "custom_test"
        assert theme.colors.primary == "#ff6b6b"

    @pytest.mark.unit
    def test_create_theme_inherits_base(self):
        """Test that custom theme inherits from base."""
        create_theme(
            "custom_test2",
            base="light",
            colors={
                "primary": "#123456",
            },
        )

        set_theme("custom_test2")
        theme = get_theme()

        # Should have the custom primary
        assert theme.colors.primary == "#123456"
        # Should inherit other colors from light theme
        assert hasattr(theme.colors, "background")


class TestThemeColors:
    """Tests for theme color properties."""

    @pytest.mark.unit
    def test_light_theme_colors(self):
        """Test light theme has appropriate colors."""
        set_theme("light")
        theme = get_theme()

        # Light theme should have light background
        assert theme.colors.background is not None

    @pytest.mark.unit
    def test_dark_theme_colors(self):
        """Test dark theme has appropriate colors."""
        set_theme("dark")
        theme = get_theme()

        # Dark theme should have dark background
        assert theme.colors.background is not None

    @pytest.mark.unit
    def test_theme_has_required_colors(self):
        """Test themes have required color keys."""
        required_colors = ["primary", "background", "text"]

        for theme_name in ["light", "dark", "ocean", "forest"]:
            set_theme(theme_name)
            theme = get_theme()

            for color in required_colors:
                assert hasattr(theme.colors, color), f"{theme_name} missing {color}"


class TestColorPalette:
    """Tests for ColorPalette class."""

    @pytest.mark.unit
    def test_default_palette(self):
        """Test default color palette."""
        palette = ColorPalette()

        assert palette.primary == "#6366f1"
        assert palette.background == "#ffffff"
        assert palette.text == "#0f172a"

    @pytest.mark.unit
    def test_custom_palette(self):
        """Test custom color palette."""
        palette = ColorPalette(
            primary="#custom",
            background="#bg",
        )

        assert palette.primary == "#custom"
        assert palette.background == "#bg"
