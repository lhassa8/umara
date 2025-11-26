"""
Tests for the Style module.
"""

from umara.style import Style


class TestStyleCreation:
    """Tests for Style creation."""

    def test_empty_style(self):
        """Test creating empty style."""
        style = Style()
        assert style.to_dict() == {}

    def test_style_with_kwargs(self):
        """Test creating style with keyword arguments."""
        style = Style(color="red", background="blue")
        assert style.to_dict() == {"color": "red", "background": "blue"}

    def test_style_camel_preserved(self):
        """Test that camelCase is preserved (only snake_case converts)."""
        style = Style(backgroundColor="red", fontSize="16px")
        d = style.to_dict()
        # camelCase is preserved as-is (only snake_case converts to kebab-case)
        assert "backgroundColor" in d
        assert "fontSize" in d

    def test_style_snake_to_kebab(self):
        """Test that snake_case converts to kebab-case."""
        style = Style(background_color="red", font_size="16px")
        d = style.to_dict()
        assert "background-color" in d
        assert "font-size" in d


class TestStyleProperties:
    """Tests for Style property access."""

    def test_setattr(self):
        """Test setting style properties."""
        style = Style()
        style.color = "red"
        style.background = "blue"
        assert style.to_dict() == {"color": "red", "background": "blue"}

    def test_getattr(self):
        """Test getting style properties."""
        style = Style(color="red")
        assert style.color == "red"

    def test_getattr_missing(self):
        """Test getting missing property returns None."""
        style = Style()
        assert style.color is None


class TestStyleConversion:
    """Tests for Style conversion methods."""

    def test_to_dict(self):
        """Test converting to dictionary."""
        style = Style(color="red", padding="10px")
        d = style.to_dict()
        assert isinstance(d, dict)
        assert d["color"] == "red"
        assert d["padding"] == "10px"

    def test_to_css(self):
        """Test converting to CSS string."""
        style = Style(color="red", padding="10px")
        css = style.to_css()
        assert "color: red" in css
        assert "padding: 10px" in css


class TestStyleMerging:
    """Tests for Style merging."""

    def test_merge(self):
        """Test merging two styles."""
        style1 = Style(color="red", padding="10px")
        style2 = Style(color="blue", margin="5px")
        merged = style1.merge(style2)

        # style2 values take precedence
        assert merged.to_dict()["color"] == "blue"
        assert merged.to_dict()["padding"] == "10px"
        assert merged.to_dict()["margin"] == "5px"

    def test_merge_or_operator(self):
        """Test merging with | operator."""
        style1 = Style(color="red")
        style2 = Style(color="blue", margin="5px")
        merged = style1 | style2

        assert merged.to_dict()["color"] == "blue"
        assert merged.to_dict()["margin"] == "5px"


class TestStyleValues:
    """Tests for Style value conversion."""

    def test_numeric_values(self):
        """Test numeric values are converted properly."""
        style = Style(opacity=0.5, z_index=100)
        d = style.to_dict()
        assert d["opacity"] == "0.5"
        assert d["z-index"] == "100"

    def test_string_values(self):
        """Test string values are preserved."""
        style = Style(color="rgba(255, 0, 0, 0.5)")
        assert style.to_dict()["color"] == "rgba(255, 0, 0, 0.5)"
