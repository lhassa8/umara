"""
Unit tests for umara.components module.
"""

import pytest
from unittest.mock import patch, MagicMock

from umara.core import get_context, set_context, ComponentContext
from umara.state import SessionState, set_session_state
import umara.components as components


class TestTypographyComponents:
    """Tests for typography components."""

    @pytest.mark.unit
    def test_text(self, component_context, session_state):
        """Test text component."""
        components.text("Hello World")

        root = component_context.get_root()
        assert root is not None
        assert len(root.children) == 1
        assert root.children[0].type == "text"
        assert root.children[0].props["content"] == "Hello World"

    @pytest.mark.unit
    def test_text_with_style(self, component_context, session_state):
        """Test text component with custom style."""
        components.text("Styled", color="#ff0000", size="20px", weight="bold")

        root = component_context.get_root()
        text_component = root.children[0]
        assert text_component.props.get("color") == "#ff0000"
        assert text_component.props.get("size") == "20px"
        assert text_component.props.get("weight") == "bold"

    @pytest.mark.unit
    def test_title(self, component_context, session_state):
        """Test title component."""
        components.title("My Title")

        root = component_context.get_root()
        assert root.children[0].type == "title"
        assert root.children[0].props["content"] == "My Title"

    @pytest.mark.unit
    def test_header(self, component_context, session_state):
        """Test header component."""
        components.header("Page Header")

        root = component_context.get_root()
        assert root.children[0].type == "header"
        assert root.children[0].props["content"] == "Page Header"

    @pytest.mark.unit
    def test_subheader(self, component_context, session_state):
        """Test subheader component."""
        components.subheader("Section Title")

        root = component_context.get_root()
        assert root.children[0].type == "subheader"

    @pytest.mark.unit
    def test_caption(self, component_context, session_state):
        """Test caption component."""
        components.caption("Small caption text")

        root = component_context.get_root()
        assert root.children[0].type == "caption"

    @pytest.mark.unit
    def test_markdown(self, component_context, session_state):
        """Test markdown component."""
        components.markdown("# Heading\n\n**Bold** text")

        root = component_context.get_root()
        assert root.children[0].type == "markdown"
        assert "# Heading" in root.children[0].props["content"]

    @pytest.mark.unit
    def test_code(self, component_context, session_state):
        """Test code component."""
        components.code("print('hello')", language="python")

        root = component_context.get_root()
        assert root.children[0].type == "code"
        assert root.children[0].props["language"] == "python"

    @pytest.mark.unit
    def test_latex(self, component_context, session_state):
        """Test latex component."""
        components.latex(r"E = mc^2")

        root = component_context.get_root()
        assert root.children[0].type == "latex"


class TestFeedbackComponents:
    """Tests for feedback/alert components."""

    @pytest.mark.unit
    def test_success(self, component_context, session_state):
        """Test success message."""
        components.success("Operation successful!")

        root = component_context.get_root()
        assert root.children[0].type == "success"
        assert root.children[0].props["message"] == "Operation successful!"

    @pytest.mark.unit
    def test_error(self, component_context, session_state):
        """Test error message."""
        components.error("Something went wrong")

        root = component_context.get_root()
        assert root.children[0].type == "error"

    @pytest.mark.unit
    def test_warning(self, component_context, session_state):
        """Test warning message."""
        components.warning("Please be careful")

        root = component_context.get_root()
        assert root.children[0].type == "warning"

    @pytest.mark.unit
    def test_info(self, component_context, session_state):
        """Test info message."""
        components.info("Here's some information")

        root = component_context.get_root()
        assert root.children[0].type == "info"

    @pytest.mark.unit
    def test_toast(self, component_context, session_state):
        """Test toast notification."""
        components.toast("Quick message!", icon="check", duration=3000)

        root = component_context.get_root()
        assert root.children[0].type == "toast"
        assert root.children[0].props["duration"] == 3000


class TestInputComponents:
    """Tests for input/widget components."""

    @pytest.mark.unit
    def test_button(self, component_context, session_state):
        """Test button component returns False by default."""
        result = components.button("Click me")

        assert result is False
        root = component_context.get_root()
        assert root.children[0].type == "button"
        assert root.children[0].props["label"] == "Click me"

    @pytest.mark.unit
    def test_button_variants(self, component_context, session_state):
        """Test button with different variants."""
        components.button("Primary", variant="primary")
        components.button("Secondary", variant="secondary")
        components.button("Danger", variant="danger")

        root = component_context.get_root()
        assert root.children[0].props["variant"] == "primary"
        assert root.children[1].props["variant"] == "secondary"
        assert root.children[2].props["variant"] == "danger"

    @pytest.mark.unit
    def test_input(self, component_context, session_state):
        """Test text input component."""
        result = components.input("Name", placeholder="Enter name", key="name_input")

        assert result == ""  # Default empty value
        root = component_context.get_root()
        assert root.children[0].type == "input"
        assert root.children[0].props["label"] == "Name"
        assert root.children[0].props["placeholder"] == "Enter name"

    @pytest.mark.unit
    def test_input_with_default(self, component_context, session_state):
        """Test input with default value."""
        result = components.input("Email", default="test@example.com", key="email")

        assert result == "test@example.com"

    @pytest.mark.unit
    def test_text_area(self, component_context, session_state):
        """Test text area component."""
        result = components.text_area("Bio", rows=5, key="bio")

        root = component_context.get_root()
        assert root.children[0].type == "text_area"
        assert root.children[0].props["rows"] == 5

    @pytest.mark.unit
    def test_number_input(self, component_context, session_state):
        """Test number input."""
        result = components.number_input(
            "Quantity",
            min_value=0,
            max_value=100,
            value=10,
            step=1,
            key="qty"
        )

        assert result == 10
        root = component_context.get_root()
        assert root.children[0].type == "number_input"
        assert root.children[0].props["min_value"] == 0
        assert root.children[0].props["max_value"] == 100

    @pytest.mark.unit
    def test_slider(self, component_context, session_state):
        """Test slider component."""
        result = components.slider("Volume", 0, 100, 50, key="volume")

        assert result == 50
        root = component_context.get_root()
        assert root.children[0].type == "slider"

    @pytest.mark.unit
    def test_select(self, component_context, session_state):
        """Test select dropdown."""
        options = ["Option A", "Option B", "Option C"]
        result = components.select("Choose", options=options, key="choice")

        root = component_context.get_root()
        assert root.children[0].type == "select"
        assert root.children[0].props["options"] == options

    @pytest.mark.unit
    def test_multiselect(self, component_context, session_state):
        """Test multiselect component."""
        options = ["Red", "Green", "Blue"]
        result = components.multiselect("Colors", options=options, key="colors")

        assert result == []  # Default empty list
        root = component_context.get_root()
        assert root.children[0].type == "multiselect"

    @pytest.mark.unit
    def test_checkbox(self, component_context, session_state):
        """Test checkbox component."""
        result = components.checkbox("I agree", key="agree")

        assert result is False
        root = component_context.get_root()
        assert root.children[0].type == "checkbox"

    @pytest.mark.unit
    def test_checkbox_default_true(self, component_context, session_state):
        """Test checkbox with default True."""
        result = components.checkbox("Enable", default=True, key="enable")

        assert result is True

    @pytest.mark.unit
    def test_toggle(self, component_context, session_state):
        """Test toggle switch."""
        result = components.toggle("Dark mode", key="dark")

        root = component_context.get_root()
        assert root.children[0].type == "toggle"

    @pytest.mark.unit
    def test_radio(self, component_context, session_state):
        """Test radio buttons."""
        options = ["Small", "Medium", "Large"]
        result = components.radio("Size", options=options, key="size")

        root = component_context.get_root()
        assert root.children[0].type == "radio"

    @pytest.mark.unit
    def test_date_input(self, component_context, session_state):
        """Test date input."""
        result = components.date_input("Birthday", key="bday")

        root = component_context.get_root()
        assert root.children[0].type == "date_input"

    @pytest.mark.unit
    def test_time_input(self, component_context, session_state):
        """Test time input."""
        result = components.time_input("Meeting time", key="time")

        root = component_context.get_root()
        assert root.children[0].type == "time_input"

    @pytest.mark.unit
    def test_color_picker(self, component_context, session_state):
        """Test color picker."""
        result = components.color_picker("Color", value="#ff0000", key="color")

        assert result == "#ff0000"
        root = component_context.get_root()
        assert root.children[0].type == "color_picker"

    @pytest.mark.unit
    def test_rating(self, component_context, session_state):
        """Test rating component."""
        result = components.rating("Rate this", value=3, max_value=5, key="rating")

        assert result == 3
        root = component_context.get_root()
        assert root.children[0].type == "rating"


class TestLayoutComponents:
    """Tests for layout components."""

    @pytest.mark.unit
    def test_container(self, component_context, session_state):
        """Test container component."""
        with components.container():
            components.text("Inside container")

        root = component_context.get_root()
        container = root.children[0]
        assert container.type == "container"
        assert len(container.children) == 1
        assert container.children[0].type == "text"

    @pytest.mark.unit
    def test_columns(self, component_context, session_state):
        """Test columns layout."""
        with components.columns(3):
            with components.column():
                components.text("Col 1")
            with components.column():
                components.text("Col 2")
            with components.column():
                components.text("Col 3")

        root = component_context.get_root()
        cols = root.children[0]
        assert cols.type == "columns"
        assert cols.props["count"] == 3

    @pytest.mark.unit
    def test_card(self, component_context, session_state):
        """Test card component."""
        with components.card(title="My Card", subtitle="Description"):
            components.text("Card content")

        root = component_context.get_root()
        card = root.children[0]
        assert card.type == "card"
        assert card.props["title"] == "My Card"
        assert card.props["subtitle"] == "Description"

    @pytest.mark.unit
    def test_grid(self, component_context, session_state):
        """Test grid layout."""
        with components.grid(columns=2, gap="16px"):
            components.text("Item 1")
            components.text("Item 2")

        root = component_context.get_root()
        grid = root.children[0]
        assert grid.type == "grid"
        assert grid.props["columns"] == 2
        assert grid.props["gap"] == "16px"

    @pytest.mark.unit
    def test_divider(self, component_context, session_state):
        """Test divider component."""
        components.divider()

        root = component_context.get_root()
        assert root.children[0].type == "divider"

    @pytest.mark.unit
    def test_spacer(self, component_context, session_state):
        """Test spacer component."""
        components.spacer(height="32px")

        root = component_context.get_root()
        assert root.children[0].type == "spacer"
        assert root.children[0].props["height"] == "32px"

    @pytest.mark.unit
    def test_expander(self, component_context, session_state):
        """Test expander component."""
        with components.expander("Details", expanded=True, key="exp"):
            components.text("Hidden content")

        root = component_context.get_root()
        expander = root.children[0]
        assert expander.type == "expander"
        assert expander.props["label"] == "Details"
        assert expander.props["expanded"] is True


class TestDataDisplayComponents:
    """Tests for data display components."""

    @pytest.mark.unit
    def test_metric(self, component_context, session_state):
        """Test metric component."""
        components.metric("Revenue", "$48,234", delta=12.5)

        root = component_context.get_root()
        metric = root.children[0]
        assert metric.type == "metric"
        assert metric.props["label"] == "Revenue"
        assert metric.props["value"] == "$48,234"
        assert metric.props["delta"] == 12.5

    @pytest.mark.unit
    def test_progress(self, component_context, session_state):
        """Test progress bar."""
        components.progress(75, label="Loading")

        root = component_context.get_root()
        progress = root.children[0]
        assert progress.type == "progress"
        assert progress.props["value"] == 75

    @pytest.mark.unit
    def test_dataframe(self, component_context, session_state, sample_data):
        """Test dataframe display."""
        components.dataframe(sample_data)

        root = component_context.get_root()
        df = root.children[0]
        assert df.type == "dataframe"
        assert df.props["data"] == sample_data

    @pytest.mark.unit
    def test_table(self, component_context, session_state, sample_data):
        """Test table display."""
        components.table(sample_data)

        root = component_context.get_root()
        table = root.children[0]
        assert table.type == "table"

    @pytest.mark.unit
    def test_badge(self, component_context, session_state):
        """Test badge component."""
        components.badge("New", variant="primary")

        root = component_context.get_root()
        badge = root.children[0]
        assert badge.type == "badge"
        assert badge.props["text"] == "New"
        assert badge.props["variant"] == "primary"

    @pytest.mark.unit
    def test_avatar(self, component_context, session_state):
        """Test avatar component."""
        components.avatar(name="John Doe", size="48px")

        root = component_context.get_root()
        avatar = root.children[0]
        assert avatar.type == "avatar"
        assert avatar.props["name"] == "John Doe"

    @pytest.mark.unit
    def test_stat_card(self, component_context, session_state):
        """Test stat card component."""
        components.stat_card("Users", "12,543", trend=12.5, icon="users")

        root = component_context.get_root()
        card = root.children[0]
        assert card.type == "stat_card"
        assert card.props["label"] == "Users"
        assert card.props["trend"] == 12.5

    @pytest.mark.unit
    def test_json_viewer(self, component_context, session_state):
        """Test JSON viewer."""
        data = {"name": "Test", "value": 123}
        components.json_viewer(data)

        root = component_context.get_root()
        viewer = root.children[0]
        assert viewer.type == "json_viewer"
        assert viewer.props["data"] == data


class TestChartComponents:
    """Tests for chart components."""

    @pytest.mark.unit
    def test_line_chart(self, component_context, session_state, chart_data):
        """Test line chart."""
        components.line_chart(
            chart_data,
            x="month",
            y=["revenue", "profit"],
            title="Revenue Chart"
        )

        root = component_context.get_root()
        chart = root.children[0]
        assert chart.type == "line_chart"
        assert chart.props["x"] == "month"
        assert chart.props["title"] == "Revenue Chart"

    @pytest.mark.unit
    def test_bar_chart(self, component_context, session_state, chart_data):
        """Test bar chart."""
        components.bar_chart(chart_data, x="month", y="revenue")

        root = component_context.get_root()
        chart = root.children[0]
        assert chart.type == "bar_chart"

    @pytest.mark.unit
    def test_area_chart(self, component_context, session_state, chart_data):
        """Test area chart."""
        components.area_chart(chart_data, x="month", y="revenue")

        root = component_context.get_root()
        chart = root.children[0]
        assert chart.type == "area_chart"

    @pytest.mark.unit
    def test_pie_chart(self, component_context, session_state):
        """Test pie chart."""
        data = [
            {"name": "A", "value": 30},
            {"name": "B", "value": 70},
        ]
        components.pie_chart(data, label="name", value="value")

        root = component_context.get_root()
        chart = root.children[0]
        assert chart.type == "pie_chart"

    @pytest.mark.unit
    def test_scatter_chart(self, component_context, session_state):
        """Test scatter chart."""
        data = [
            {"x": 1, "y": 2},
            {"x": 3, "y": 4},
        ]
        components.scatter_chart(data, x="x", y="y")

        root = component_context.get_root()
        chart = root.children[0]
        assert chart.type == "scatter_chart"


class TestNavigationComponents:
    """Tests for navigation components."""

    @pytest.mark.unit
    def test_breadcrumbs(self, component_context, session_state):
        """Test breadcrumbs."""
        items = [
            {"label": "Home", "href": "/"},
            {"label": "Products", "href": "/products"},
        ]
        components.breadcrumbs(items)

        root = component_context.get_root()
        bc = root.children[0]
        assert bc.type == "breadcrumbs"
        assert bc.props["items"] == items

    @pytest.mark.unit
    def test_pagination(self, component_context, session_state):
        """Test pagination."""
        result = components.pagination(total_pages=10, current_page=3, key="page")

        root = component_context.get_root()
        pag = root.children[0]
        assert pag.type == "pagination"
        assert pag.props["total_pages"] == 10

    @pytest.mark.unit
    def test_steps(self, component_context, session_state):
        """Test steps component."""
        steps = ["Step 1", "Step 2", "Step 3"]
        components.steps(steps, current=1, key="wizard")

        root = component_context.get_root()
        s = root.children[0]
        assert s.type == "steps"
        assert s.props["current"] == 1


class TestMediaComponents:
    """Tests for media components."""

    @pytest.mark.unit
    def test_image(self, component_context, session_state):
        """Test image component."""
        components.image("https://example.com/image.png", caption="Test image")

        root = component_context.get_root()
        img = root.children[0]
        assert img.type == "image"
        assert img.props["src"] == "https://example.com/image.png"
        assert img.props["caption"] == "Test image"

    @pytest.mark.unit
    def test_video(self, component_context, session_state):
        """Test video component."""
        components.video("https://example.com/video.mp4")

        root = component_context.get_root()
        vid = root.children[0]
        assert vid.type == "video"

    @pytest.mark.unit
    def test_audio(self, component_context, session_state):
        """Test audio component."""
        components.audio("https://example.com/audio.mp3")

        root = component_context.get_root()
        aud = root.children[0]
        assert aud.type == "audio"


class TestChatComponents:
    """Tests for chat components."""

    @pytest.mark.unit
    def test_chat_message(self, component_context, session_state):
        """Test chat message."""
        components.chat_message("user", "Hello!")

        root = component_context.get_root()
        msg = root.children[0]
        assert msg.type == "chat_message"
        assert msg.props["role"] == "user"
        assert msg.props["content"] == "Hello!"

    @pytest.mark.unit
    def test_chat_input(self, component_context, session_state):
        """Test chat input."""
        result = components.chat_input("Type a message...", key="chat")

        root = component_context.get_root()
        inp = root.children[0]
        assert inp.type == "chat_input"

    @pytest.mark.unit
    def test_chat_container(self, component_context, session_state):
        """Test chat container."""
        with components.chat_container(height="400px"):
            components.chat_message("assistant", "Hi!")

        root = component_context.get_root()
        container = root.children[0]
        assert container.type == "chat_container"
        assert container.props["height"] == "400px"


class TestWriteFunction:
    """Tests for the smart write function."""

    @pytest.mark.unit
    def test_write_string(self, component_context, session_state):
        """Test write with string."""
        components.write("Hello World")

        root = component_context.get_root()
        assert root.children[0].type == "text"

    @pytest.mark.unit
    def test_write_number(self, component_context, session_state):
        """Test write with number."""
        components.write(42)

        root = component_context.get_root()
        assert root.children[0].type == "text"
        assert "42" in root.children[0].props["content"]

    @pytest.mark.unit
    def test_write_dict(self, component_context, session_state):
        """Test write with dictionary."""
        components.write({"key": "value"})

        root = component_context.get_root()
        assert root.children[0].type == "json_viewer"

    @pytest.mark.unit
    def test_write_list_of_dicts(self, component_context, session_state, sample_data):
        """Test write with list of dicts (dataframe-like)."""
        components.write(sample_data)

        root = component_context.get_root()
        assert root.children[0].type == "dataframe"


class TestFormComponents:
    """Tests for form components."""

    @pytest.mark.unit
    def test_form_submit_button(self, component_context, session_state):
        """Test form submit button."""
        result = components.form_submit_button("Submit")

        root = component_context.get_root()
        btn = root.children[0]
        assert btn.type == "form_submit_button"
        assert btn.props["label"] == "Submit"


class TestUtilityComponents:
    """Tests for utility components."""

    @pytest.mark.unit
    def test_spinner(self, component_context, session_state):
        """Test spinner component."""
        components.spinner("Loading...")

        root = component_context.get_root()
        spin = root.children[0]
        assert spin.type == "spinner"

    @pytest.mark.unit
    def test_empty_state(self, component_context, session_state):
        """Test empty state component."""
        components.empty_state(
            title="No results",
            description="Try a different search",
            icon="search"
        )

        root = component_context.get_root()
        empty = root.children[0]
        assert empty.type == "empty_state"
        assert empty.props["title"] == "No results"

    @pytest.mark.unit
    def test_loading_skeleton(self, component_context, session_state):
        """Test loading skeleton."""
        components.loading_skeleton(variant="text", lines=3)

        root = component_context.get_root()
        skeleton = root.children[0]
        assert skeleton.type == "loading_skeleton"

    @pytest.mark.unit
    def test_timeline(self, component_context, session_state):
        """Test timeline component."""
        items = [
            {"title": "Event 1", "description": "First", "time": "9:00"},
            {"title": "Event 2", "description": "Second", "time": "10:00"},
        ]
        components.timeline(items)

        root = component_context.get_root()
        tl = root.children[0]
        assert tl.type == "timeline"
        assert len(tl.props["items"]) == 2
