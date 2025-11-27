"""
UI Components for Umara.

All components are designed to be beautiful by default with
polished styling out of the box.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable

from umara.core import Component, ContainerContext, get_context
from umara.state import get_session_state
from umara.style import Style

# =============================================================================
# Typography Components
# =============================================================================


def text(
    content: str,
    *,
    style: Style | None = None,
    color: str | None = None,
    size: str | None = None,
) -> None:
    """
    Display text content.

    Args:
        content: The text to display
        style: Optional Style object for custom styling
        color: Text color (shorthand for style)
        size: Font size (shorthand for style)
    """
    ctx = get_context()
    props = {"content": content}

    style_dict = style.to_dict() if style else {}
    if color:
        style_dict["color"] = color
    if size:
        style_dict["font-size"] = size

    ctx.create_component("text", props=props, style=style_dict or None)


def header(
    content: str,
    *,
    level: int = 1,
    style: Style | None = None,
) -> None:
    """
    Display a header.

    Args:
        content: Header text
        level: Header level (1-6)
        style: Optional Style object
    """
    ctx = get_context()
    props = {"content": content, "level": level}
    style_dict = style.to_dict() if style else None
    ctx.create_component("header", props=props, style=style_dict)


def subheader(
    content: str,
    *,
    style: Style | None = None,
) -> None:
    """
    Display a subheader (h3).

    Args:
        content: Subheader text
        style: Optional Style object
    """
    ctx = get_context()
    props = {"content": content}
    style_dict = style.to_dict() if style else None
    ctx.create_component("subheader", props=props, style=style_dict)


def markdown(
    content: str,
    *,
    style: Style | None = None,
) -> None:
    """
    Display markdown content.

    Args:
        content: Markdown string
        style: Optional Style object
    """
    ctx = get_context()
    props = {"content": content}
    style_dict = style.to_dict() if style else None
    ctx.create_component("markdown", props=props, style=style_dict)


def code(
    content: str,
    *,
    language: str = "python",
    line_numbers: bool = True,
    style: Style | None = None,
) -> None:
    """
    Display code with syntax highlighting.

    Args:
        content: Code string
        language: Programming language for syntax highlighting
        line_numbers: Show line numbers
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "content": content,
        "language": language,
        "lineNumbers": line_numbers,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("code", props=props, style=style_dict)


# =============================================================================
# Feedback Components
# =============================================================================


def success(message: str, *, style: Style | None = None) -> None:
    """Display a success message."""
    ctx = get_context()
    props = {"message": message}
    style_dict = style.to_dict() if style else None
    ctx.create_component("success", props=props, style=style_dict)


def error(message: str, *, style: Style | None = None) -> None:
    """Display an error message."""
    ctx = get_context()
    props = {"message": message}
    style_dict = style.to_dict() if style else None
    ctx.create_component("error", props=props, style=style_dict)


def warning(message: str, *, style: Style | None = None) -> None:
    """Display a warning message."""
    ctx = get_context()
    props = {"message": message}
    style_dict = style.to_dict() if style else None
    ctx.create_component("warning", props=props, style=style_dict)


def info(message: str, *, style: Style | None = None) -> None:
    """Display an info message."""
    ctx = get_context()
    props = {"message": message}
    style_dict = style.to_dict() if style else None
    ctx.create_component("info", props=props, style=style_dict)


# =============================================================================
# Layout Components
# =============================================================================


@contextmanager
def container(
    *,
    padding: str | None = None,
    margin: str | None = None,
    align: str | None = None,
    justify: str | None = None,
    gap: str | None = None,
    style: Style | None = None,
):
    """
    Create a container for grouping elements.

    Args:
        padding: Container padding
        margin: Container margin
        align: Horizontal alignment ('start', 'center', 'end', 'stretch')
        justify: Vertical alignment ('start', 'center', 'end', 'space-between', 'space-around')
        gap: Gap between child elements
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "align": align,
        "justify": justify,
        "gap": gap,
    }
    style_dict = style.to_dict() if style else {}
    if padding:
        style_dict["padding"] = padding
    if margin:
        style_dict["margin"] = margin

    component = ctx.create_component("container", props=props, style=style_dict or None)
    with ContainerContext(component):
        yield


@contextmanager
def columns(
    count: int = 2,
    *,
    gap: str = "16px",
    vertical_align: str | None = None,
    style: Style | None = None,
):
    """
    Create a column layout.

    Args:
        count: Number of columns
        gap: Gap between columns
        vertical_align: Vertical alignment of items ('start', 'center', 'end', 'stretch')
        style: Optional Style object
    """
    ctx = get_context()
    props = {"count": count, "gap": gap, "verticalAlign": vertical_align}
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("columns", props=props, style=style_dict)
    with ContainerContext(component):
        yield


@contextmanager
def column(
    *,
    align: str | None = None,
    justify: str | None = None,
    gap: str | None = None,
    style: Style | None = None,
):
    """
    Create a single column within a columns layout.

    Args:
        align: Horizontal alignment ('start', 'center', 'end', 'stretch')
        justify: Vertical alignment ('start', 'center', 'end', 'space-between')
        gap: Gap between child elements
        style: Optional Style object
    """
    ctx = get_context()
    props = {"align": align, "justify": justify, "gap": gap}
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("column", props=props, style=style_dict)
    with ContainerContext(component):
        yield


@contextmanager
def grid(
    columns: int | str = 3,
    *,
    gap: str = "16px",
    row_gap: str | None = None,
    align: str | None = None,
    justify: str | None = None,
    style: Style | None = None,
):
    """
    Create a CSS grid layout.

    Args:
        columns: Number of columns or CSS grid-template-columns value
        gap: Gap between items
        row_gap: Vertical gap (defaults to gap)
        align: Align items within cells ('start', 'center', 'end', 'stretch')
        justify: Justify items within cells ('start', 'center', 'end', 'stretch')
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "columns": columns,
        "gap": gap,
        "rowGap": row_gap or gap,
        "align": align,
        "justify": justify,
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("grid", props=props, style=style_dict)
    with ContainerContext(component):
        yield


@contextmanager
def card(
    *,
    title: str | None = None,
    subtitle: str | None = None,
    padding: str = "24px",
    shadow: str = "md",
    align: str | None = None,
    justify: str | None = None,
    gap: str | None = None,
    style: Style | None = None,
):
    """
    Create a card component with beautiful default styling.

    Args:
        title: Optional card title
        subtitle: Optional card subtitle
        padding: Card padding
        shadow: Shadow size (sm, md, lg, xl)
        align: Horizontal alignment ('start', 'center', 'end', 'stretch')
        justify: Vertical alignment ('start', 'center', 'end', 'space-between')
        gap: Gap between child elements
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "title": title,
        "subtitle": subtitle,
        "padding": padding,
        "shadow": shadow,
        "align": align,
        "justify": justify,
        "gap": gap,
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("card", props=props, style=style_dict)
    with ContainerContext(component):
        yield


class TabContext:
    """Context manager for tab content."""

    def __init__(self, component: Component, tab_index: int, active_tab: int):
        self.component = component
        self.tab_index = tab_index
        self.active_tab = active_tab
        self._ctx = None

    def __enter__(self):
        self._ctx = get_context()
        # Create a tab content container
        tab_component = self._ctx.create_component("tab", props={"index": self.tab_index})
        self._ctx.push(tab_component)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._ctx:
            self._ctx.pop()
        return False


@contextmanager
def tabs(
    tab_names: list[str],
    *,
    default: int = 0,
    key: str | None = None,
    style: Style | None = None,
):
    """
    Create a tabbed interface.

    Args:
        tab_names: List of tab names
        default: Default active tab index
        key: State key for active tab
        style: Optional Style object

    Example:
        with um.tabs(['Tab 1', 'Tab 2']) as t:
            with t.tab(0):
                um.text('Content for tab 1')
            with t.tab(1):
                um.text('Content for tab 2')
    """
    ctx = get_context()
    state = get_session_state()

    # Get or set the active tab
    state_key = key or f"_tabs_{id(tab_names)}"
    active_tab = state.setdefault(state_key, default)

    props = {
        "tabs": tab_names,
        "activeTab": active_tab,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("tabs", props=props, style=style_dict)

    class TabsContext:
        def __init__(self, comp, active):
            self.component = comp
            self.active_tab = active

        @contextmanager
        def tab(self, index: int):
            """Create content for a specific tab."""
            ctx = get_context()
            ctx.push(self.component)
            tab_comp = ctx.create_component("tab", props={"index": index})
            ctx.pop()
            ctx.push(tab_comp)
            try:
                yield
            finally:
                ctx.pop()

    yield TabsContext(component, active_tab)


@contextmanager
def tab(index: int):
    """Create tab content (use within tabs context)."""
    ctx = get_context()
    component = ctx.create_component("tab", props={"index": index})
    with ContainerContext(component):
        yield


def divider(*, style: Style | None = None) -> None:
    """Create a horizontal divider."""
    ctx = get_context()
    style_dict = style.to_dict() if style else None
    ctx.create_component("divider", style=style_dict)


def spacer(height: str = "24px") -> None:
    """Create vertical space."""
    ctx = get_context()
    ctx.create_component("spacer", props={"height": height})


# =============================================================================
# Widget Components
# =============================================================================


def button(
    label: str,
    *,
    key: str | None = None,
    variant: str = "primary",
    disabled: bool = False,
    loading: bool = False,
    full_width: bool = False,
    icon: str | None = None,
    style: Style | None = None,
) -> bool:
    """
    Create a button.

    Args:
        label: Button label
        key: Unique key for the button
        variant: Button style ('primary', 'secondary', 'outline', 'ghost', 'danger')
        disabled: Whether button is disabled
        loading: Show loading spinner (also disables the button)
        full_width: Take full width
        icon: Optional icon name
        style: Optional Style object

    Returns:
        True if the button was clicked in this render
    """
    ctx = get_context()
    state = get_session_state()

    # Generate state key
    state_key = key or f"_btn_{label}"
    clicked_key = f"{state_key}_clicked"
    was_clicked = bool(state.get(clicked_key, False))

    # Reset click state silently (direct dict access to avoid triggering re-render)
    if was_clicked:
        state._state[clicked_key].value = False

    props = {
        "label": label,
        "variant": variant,
        "disabled": disabled or loading,
        "loading": loading,
        "fullWidth": full_width,
        "icon": icon,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else {}
    if full_width:
        style_dict["width"] = "100%"

    ctx.create_component(
        "button",
        key=state_key,
        props=props,
        style=style_dict or None,
        events={"click": f"{state_key}:click"},
    )

    return was_clicked


def input(
    label: str = "",
    *,
    key: str | None = None,
    value: str = "",
    placeholder: str = "",
    type: str = "text",
    disabled: bool = False,
    label_position: str = "top",
    label_width: str = "120px",
    style: Style | None = None,
) -> str:
    """
    Create a text input.

    Args:
        label: Input label
        key: State key for the input value
        value: Default value
        placeholder: Placeholder text
        type: Input type ('text', 'password', 'email', 'number')
        disabled: Whether input is disabled
        label_position: Position of label ('top' or 'left')
        label_width: Width of label when position is 'left' (e.g., '120px', '30%')
        style: Optional Style object

    Returns:
        Current input value
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_input_{label or 'default'}"
    current_value = state.setdefault(state_key, value)

    props = {
        "label": label,
        "value": current_value,
        "placeholder": placeholder,
        "type": type,
        "disabled": disabled,
        "stateKey": state_key,
        "labelPosition": label_position,
        "labelWidth": label_width,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("input", key=state_key, props=props, style=style_dict)

    return current_value


def text_area(
    label: str = "",
    *,
    key: str | None = None,
    value: str = "",
    placeholder: str = "",
    rows: int = 4,
    disabled: bool = False,
    label_position: str = "top",
    label_width: str = "120px",
    style: Style | None = None,
) -> str:
    """
    Create a text area for multi-line input.

    Args:
        label: Input label
        key: State key
        value: Default value
        placeholder: Placeholder text
        rows: Number of visible rows
        disabled: Whether disabled
        label_position: Position of label ('top' or 'left')
        label_width: Width of label when position is 'left'
        style: Optional Style object

    Returns:
        Current text area value
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_textarea_{label or 'default'}"
    current_value = state.setdefault(state_key, value)

    props = {
        "label": label,
        "value": current_value,
        "placeholder": placeholder,
        "rows": rows,
        "disabled": disabled,
        "stateKey": state_key,
        "labelPosition": label_position,
        "labelWidth": label_width,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("textarea", key=state_key, props=props, style=style_dict)

    return current_value


def slider(
    label: str = "",
    min_value: float = 0,
    max_value: float = 100,
    value: float | None = None,
    *,
    key: str | None = None,
    step: float = 1,
    disabled: bool = False,
    style: Style | None = None,
) -> float:
    """
    Create a range slider.

    Args:
        label: Slider label
        min_value: Minimum value
        max_value: Maximum value
        value: Default value (defaults to min_value)
        key: State key
        step: Step increment
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Current slider value
    """
    ctx = get_context()
    state = get_session_state()

    default_value = value if value is not None else min_value
    state_key = key or f"_slider_{label or 'default'}"
    current_value = state.setdefault(state_key, default_value)

    props = {
        "label": label,
        "min": min_value,
        "max": max_value,
        "value": current_value,
        "step": step,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("slider", props=props, style=style_dict)

    return current_value


def select(
    label: str = "",
    options: list[str | dict[str, str]] | None = None,
    *,
    key: str | None = None,
    default: str | None = None,
    placeholder: str = "Select an option...",
    disabled: bool = False,
    label_position: str = "top",
    label_width: str = "120px",
    style: Style | None = None,
) -> str | None:
    """
    Create a dropdown select.

    Args:
        label: Select label
        options: List of options (strings or dicts with 'value' and 'label')
        key: State key
        default: Default selected value
        placeholder: Placeholder text
        disabled: Whether disabled
        label_position: Position of label ('top' or 'left')
        label_width: Width of label when position is 'left'
        style: Optional Style object

    Returns:
        Currently selected value
    """
    ctx = get_context()
    state = get_session_state()

    options = options or []
    state_key = key or f"_select_{label or 'default'}"
    current_value = state.setdefault(state_key, default)

    props = {
        "label": label,
        "options": options,
        "value": current_value,
        "placeholder": placeholder,
        "disabled": disabled,
        "stateKey": state_key,
        "labelPosition": label_position,
        "labelWidth": label_width,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("select", props=props, style=style_dict)

    return current_value


def multiselect(
    label: str = "",
    options: list[str | dict[str, str]] | None = None,
    *,
    key: str | None = None,
    default: list[str] | None = None,
    placeholder: str = "Select options...",
    disabled: bool = False,
    style: Style | None = None,
) -> list[str]:
    """
    Create a multi-select dropdown.

    Args:
        label: Select label
        options: List of options
        key: State key
        default: Default selected values
        placeholder: Placeholder text
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        List of selected values
    """
    ctx = get_context()
    state = get_session_state()

    options = options or []
    default = default or []
    state_key = key or f"_multiselect_{label or 'default'}"
    current_value = state.setdefault(state_key, default)

    props = {
        "label": label,
        "options": options,
        "value": current_value,
        "placeholder": placeholder,
        "disabled": disabled,
        "stateKey": state_key,
        "multi": True,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("multiselect", props=props, style=style_dict)

    return current_value


def checkbox(
    label: str,
    *,
    key: str | None = None,
    value: bool = False,
    disabled: bool = False,
    style: Style | None = None,
) -> bool:
    """
    Create a checkbox.

    Args:
        label: Checkbox label
        key: State key
        value: Default checked state
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Current checked state
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_checkbox_{label}"
    current_value = state.setdefault(state_key, value)

    props = {
        "label": label,
        "value": current_value,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("checkbox", props=props, style=style_dict)

    return current_value


def toggle(
    label: str,
    *,
    key: str | None = None,
    value: bool = False,
    disabled: bool = False,
    style: Style | None = None,
) -> bool:
    """
    Create a toggle switch.

    Args:
        label: Toggle label
        key: State key
        value: Default state
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Current toggle state
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_toggle_{label}"
    current_value = state.setdefault(state_key, value)

    props = {
        "label": label,
        "value": current_value,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("toggle", props=props, style=style_dict)

    return current_value


def radio(
    label: str,
    options: list[str],
    *,
    key: str | None = None,
    default: str | None = None,
    horizontal: bool = False,
    disabled: bool = False,
    style: Style | None = None,
) -> str | None:
    """
    Create radio buttons.

    Args:
        label: Group label
        options: List of option labels
        key: State key
        default: Default selected option
        horizontal: Arrange horizontally
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Currently selected option
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_radio_{label}"
    current_value = state.setdefault(state_key, default)

    props = {
        "label": label,
        "options": options,
        "value": current_value,
        "horizontal": horizontal,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("radio", props=props, style=style_dict)

    return current_value


def date_input(
    label: str = "",
    *,
    key: str | None = None,
    value: str | None = None,
    min_date: str | None = None,
    max_date: str | None = None,
    disabled: bool = False,
    style: Style | None = None,
) -> str | None:
    """
    Create a date input.

    Args:
        label: Input label
        key: State key
        value: Default date (YYYY-MM-DD format)
        min_date: Minimum selectable date
        max_date: Maximum selectable date
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Selected date string (YYYY-MM-DD)
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_date_{label or 'default'}"
    current_value = state.setdefault(state_key, value)

    props = {
        "label": label,
        "value": current_value,
        "minDate": min_date,
        "maxDate": max_date,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("date", props=props, style=style_dict)

    return current_value


def time_input(
    label: str = "",
    *,
    key: str | None = None,
    value: str | None = None,
    disabled: bool = False,
    style: Style | None = None,
) -> str | None:
    """
    Create a time input.

    Args:
        label: Input label
        key: State key
        value: Default time (HH:MM format)
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Selected time string (HH:MM)
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_time_{label or 'default'}"
    current_value = state.setdefault(state_key, value)

    props = {
        "label": label,
        "value": current_value,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("time", props=props, style=style_dict)

    return current_value


def file_uploader(
    label: str = "",
    *,
    key: str | None = None,
    accept: list[str] | None = None,
    multiple: bool = False,
    max_file_size: int | None = None,
    disabled: bool = False,
    style: Style | None = None,
) -> Any | None:
    """
    Create a file uploader.

    Args:
        label: Uploader label
        key: State key
        accept: Accepted file types (e.g., ['.pdf', '.docx'])
        multiple: Allow multiple files
        max_file_size: Maximum file size in bytes (e.g., 10*1024*1024 for 10MB)
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Uploaded file(s) or None
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_file_{label or 'default'}"
    current_value = state.setdefault(state_key, None)

    props = {
        "label": label,
        "accept": accept,
        "multiple": multiple,
        "maxFileSize": max_file_size,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("fileuploader", props=props, style=style_dict)

    return current_value


def color_picker(
    label: str = "",
    *,
    key: str | None = None,
    value: str = "#6366f1",
    disabled: bool = False,
    style: Style | None = None,
) -> str:
    """
    Create a color picker.

    Args:
        label: Picker label
        key: State key
        value: Default color (hex)
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Selected color (hex)
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_color_{label or 'default'}"
    current_value = state.setdefault(state_key, value)

    props = {
        "label": label,
        "value": current_value,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("colorpicker", props=props, style=style_dict)

    return current_value


# =============================================================================
# Data Display Components
# =============================================================================


def dataframe(
    data: Any,
    *,
    columns: list[str] | None = None,
    height: str | None = None,
    sortable: bool = False,
    style: Style | None = None,
) -> None:
    """
    Display a dataframe or table data.

    Args:
        data: Data to display (list of dicts, pandas DataFrame, etc.)
        columns: Column names (inferred from data if not provided)
        height: Max height with scrolling
        sortable: Enable column sorting by clicking headers
        style: Optional Style object
    """
    ctx = get_context()

    # Convert various data types
    if hasattr(data, "to_dict"):
        # pandas DataFrame
        records = data.to_dict("records")
        cols = columns or list(data.columns)
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        records = data
        cols = columns or list(data[0].keys())
    else:
        records = []
        cols = columns or []

    props = {
        "data": records,
        "columns": cols,
        "height": height,
        "sortable": sortable,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("dataframe", props=props, style=style_dict)


def table(
    data: Any,
    *,
    columns: list[str] | None = None,
    style: Style | None = None,
) -> None:
    """Alias for dataframe."""
    dataframe(data, columns=columns, style=style)


def metric(
    label: str,
    value: Any,
    *,
    delta: float | None = None,
    delta_label: str = "",
    style: Style | None = None,
) -> None:
    """
    Display a metric with optional delta.

    Args:
        label: Metric label
        value: Metric value
        delta: Change value (positive or negative)
        delta_label: Label for delta (e.g., "from last week")
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "label": label,
        "value": str(value),
        "delta": delta,
        "deltaLabel": delta_label,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("metric", props=props, style=style_dict)


def progress(
    value: float,
    *,
    label: str | None = None,
    style: Style | None = None,
) -> None:
    """
    Display a progress bar.

    Args:
        value: Progress value (0-100)
        label: Optional label
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "value": max(0, min(100, value)),
        "label": label,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("progress", props=props, style=style_dict)


@contextmanager
def spinner(text: str = "Loading..."):
    """
    Show a spinner while executing code.

    Args:
        text: Loading text to display
    """
    ctx = get_context()
    ctx.create_component("spinner", props={"text": text})
    yield
    # Spinner is removed when context exits


# =============================================================================
# Media Components
# =============================================================================


def image(
    src: str,
    *,
    alt: str = "",
    width: str | None = None,
    height: str | None = None,
    caption: str | None = None,
    style: Style | None = None,
) -> None:
    """
    Display an image.

    Args:
        src: Image URL or base64 data
        alt: Alt text for accessibility
        width: Image width
        height: Image height
        caption: Image caption
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "src": src,
        "alt": alt,
        "width": width,
        "height": height,
        "caption": caption,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("image", props=props, style=style_dict)


def video(
    src: str,
    *,
    autoplay: bool = False,
    controls: bool = True,
    loop: bool = False,
    muted: bool = False,
    width: str | None = None,
    height: str | None = None,
    style: Style | None = None,
) -> None:
    """
    Display a video.

    Args:
        src: Video URL
        autoplay: Auto-play video
        controls: Show video controls
        loop: Loop video
        muted: Mute audio
        width: Video width
        height: Video height
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "src": src,
        "autoplay": autoplay,
        "controls": controls,
        "loop": loop,
        "muted": muted,
        "width": width,
        "height": height,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("video", props=props, style=style_dict)


def audio(
    src: str,
    *,
    autoplay: bool = False,
    controls: bool = True,
    loop: bool = False,
    style: Style | None = None,
) -> None:
    """
    Display an audio player.

    Args:
        src: Audio URL
        autoplay: Auto-play audio
        controls: Show audio controls
        loop: Loop audio
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "src": src,
        "autoplay": autoplay,
        "controls": controls,
        "loop": loop,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("audio", props=props, style=style_dict)


# =============================================================================
# Chat/Conversation Components
# =============================================================================


@dataclass
class ChatMessage:
    """Represents a chat message."""

    role: str  # 'user', 'assistant', 'system'
    content: str
    avatar: str | None = None
    timestamp: str | None = None
    metadata: dict[str, Any] | None = None


def chat_message(
    content: str,
    *,
    role: str = "assistant",
    avatar: str | None = None,
    name: str | None = None,
    timestamp: str | None = None,
    is_streaming: bool = False,
    style: Style | None = None,
) -> None:
    """
    Display a single chat message.

    Args:
        content: Message content (supports markdown)
        role: Message role ('user', 'assistant', 'system')
        avatar: Avatar URL or emoji
        name: Display name
        timestamp: Message timestamp
        is_streaming: Show typing indicator
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "content": content,
        "role": role,
        "avatar": avatar,
        "name": name,
        "timestamp": timestamp,
        "isStreaming": is_streaming,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("chat_message", props=props, style=style_dict)


def chat_input(
    placeholder: str = "Type a message...",
    *,
    key: str | None = None,
    disabled: bool = False,
    max_length: int | None = None,
    style: Style | None = None,
) -> str | None:
    """
    Display a chat input field. Returns the submitted message.

    Args:
        placeholder: Input placeholder text
        key: State key
        disabled: Whether input is disabled
        max_length: Maximum message length
        style: Optional Style object

    Returns:
        Submitted message or None if no submission
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or "_chat_input"
    submitted_message = state.get(f"{state_key}_submitted", None)

    # Clear submitted message after reading
    if submitted_message:
        state.update(**{f"{state_key}_submitted": None})

    props = {
        "placeholder": placeholder,
        "disabled": disabled,
        "maxLength": max_length,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("chat_input", props=props, style=style_dict)

    return submitted_message


@contextmanager
def chat_container(
    *,
    height: str = "500px",
    key: str | None = None,
    style: Style | None = None,
):
    """
    Create a scrollable chat container for messages.

    Args:
        height: Container height
        key: State key for scroll position
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "height": height,
        "stateKey": key or "_chat_container",
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("chat_container", props=props, style=style_dict)
    with ContainerContext(component):
        yield


def chat(
    messages: list[dict[str, Any]],
    *,
    key: str | None = None,
    height: str = "500px",
    show_input: bool = True,
    input_placeholder: str = "Type a message...",
    on_submit: Callable[[str], None] | None = None,
    user_avatar: str | None = None,
    assistant_avatar: str | None = None,
    style: Style | None = None,
) -> str | None:
    """
    Display a complete chat interface with message history and input.

    This is the easiest way to add an AI chatbot interface to your app.

    Args:
        messages: List of message dicts with 'role' and 'content' keys
        key: State key for the chat
        height: Chat container height
        show_input: Whether to show the input field
        input_placeholder: Input placeholder text
        on_submit: Callback when user submits a message
        user_avatar: Default avatar for user messages
        assistant_avatar: Default avatar for assistant messages
        style: Optional Style object

    Returns:
        Submitted message if user sent one, else None

    Example:
        messages = [
            {"role": "assistant", "content": "Hello! How can I help?"},
            {"role": "user", "content": "What's the weather?"},
        ]

        if user_input := um.chat(messages):
            # Process user input, call AI, update messages
            messages.append({"role": "user", "content": user_input})
            response = call_ai(user_input)
            messages.append({"role": "assistant", "content": response})
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or "_chat"

    # Get submitted message
    submitted = state.get(f"{state_key}_submitted", None)
    if submitted:
        state.update(**{f"{state_key}_submitted": None})

    props = {
        "messages": messages,
        "height": height,
        "showInput": show_input,
        "inputPlaceholder": input_placeholder,
        "userAvatar": user_avatar,
        "assistantAvatar": assistant_avatar,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("chat", props=props, style=style_dict)

    return submitted


# =============================================================================
# Navigation Components
# =============================================================================


@contextmanager
def sidebar(
    *,
    width: str = "280px",
    collapsed: bool = False,
    style: Style | None = None,
):
    """
    Create a sidebar navigation panel.

    Args:
        width: Sidebar width
        collapsed: Whether sidebar is collapsed
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "width": width,
        "collapsed": collapsed,
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("sidebar", props=props, style=style_dict)
    with ContainerContext(component):
        yield


def nav_link(
    label: str,
    *,
    href: str | None = None,
    icon: str | None = None,
    active: bool = False,
    key: str | None = None,
    style: Style | None = None,
) -> bool:
    """
    Create a navigation link.

    Args:
        label: Link label
        href: Link URL (optional, can use as button)
        icon: Icon name
        active: Whether link is active/selected
        key: State key
        style: Optional Style object

    Returns:
        True if clicked
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_nav_{label}"
    was_clicked = bool(state.get(f"{state_key}_clicked", False))
    if was_clicked:
        state.update(**{f"{state_key}_clicked": False})

    props = {
        "label": label,
        "href": href,
        "icon": icon,
        "active": active,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("nav_link", props=props, style=style_dict)

    return was_clicked


def breadcrumbs(
    items: list[dict[str, str]],
    *,
    separator: str = "/",
    style: Style | None = None,
) -> None:
    """
    Display breadcrumb navigation.

    Args:
        items: List of dicts with 'label' and optional 'href' keys
        separator: Separator between items
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "items": items,
        "separator": separator,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("breadcrumbs", props=props, style=style_dict)


def pagination(
    total_pages: int,
    *,
    current_page: int = 1,
    key: str | None = None,
    style: Style | None = None,
) -> int:
    """
    Display pagination controls.

    Args:
        total_pages: Total number of pages
        current_page: Current page (1-indexed)
        key: State key
        style: Optional Style object

    Returns:
        Current page number
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or "_pagination"
    page = state.setdefault(state_key, current_page)

    props = {
        "totalPages": total_pages,
        "currentPage": page,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("pagination", props=props, style=style_dict)

    return page


# =============================================================================
# Container Components
# =============================================================================


@contextmanager
def expander(
    title: str,
    *,
    expanded: bool = False,
    key: str | None = None,
    icon: str | None = None,
    style: Style | None = None,
):
    """
    Create an expandable/collapsible section.

    Args:
        title: Section title
        expanded: Whether initially expanded
        key: State key
        icon: Optional icon
        style: Optional Style object
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_expander_{title}"
    is_expanded = state.setdefault(state_key, expanded)

    props = {
        "title": title,
        "expanded": is_expanded,
        "icon": icon,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("expander", props=props, style=style_dict)
    with ContainerContext(component):
        yield


@contextmanager
def accordion(
    items: list[str],
    *,
    allow_multiple: bool = False,
    key: str | None = None,
    style: Style | None = None,
):
    """
    Create an accordion with multiple collapsible sections.

    Args:
        items: List of section titles
        allow_multiple: Allow multiple sections open
        key: State key
        style: Optional Style object
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or "_accordion"
    open_items: list[str] = state.setdefault(state_key, [])

    props = {
        "items": items,
        "allowMultiple": allow_multiple,
        "openItems": open_items,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("accordion", props=props, style=style_dict)
    with ContainerContext(component):
        yield


@contextmanager
def modal(
    title: str,
    *,
    is_open: bool = False,
    key: str | None = None,
    size: str = "md",
    close_on_overlay: bool = True,
    style: Style | None = None,
):
    """
    Create a modal dialog.

    Args:
        title: Modal title
        is_open: Whether modal is open
        key: State key
        size: Modal size ('sm', 'md', 'lg', 'xl', 'full')
        close_on_overlay: Close when clicking overlay
        style: Optional Style object
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_modal_{title}"
    open_state = state.setdefault(state_key, is_open)

    props = {
        "title": title,
        "isOpen": open_state,
        "size": size,
        "closeOnOverlay": close_on_overlay,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("modal", props=props, style=style_dict)
    with ContainerContext(component):
        yield


def open_modal(key: str) -> None:
    """Open a modal by its key."""
    state = get_session_state()
    state.update(**{key: True})


def close_modal(key: str) -> None:
    """Close a modal by its key."""
    state = get_session_state()
    state.update(**{key: False})


@contextmanager
def popover(
    trigger_label: str,
    *,
    position: str = "bottom",
    key: str | None = None,
    style: Style | None = None,
):
    """
    Create a popover that appears on click.

    Args:
        trigger_label: Label for the trigger button
        position: Position ('top', 'bottom', 'left', 'right')
        key: State key
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "triggerLabel": trigger_label,
        "position": position,
        "stateKey": key or f"_popover_{trigger_label}",
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("popover", props=props, style=style_dict)
    with ContainerContext(component):
        yield


def tooltip(
    content: str,
    *,
    text: str,
    position: str = "top",
    style: Style | None = None,
) -> None:
    """
    Display text with a tooltip on hover.

    Args:
        content: Text to display
        text: Tooltip text
        position: Tooltip position ('top', 'bottom', 'left', 'right')
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "content": content,
        "tooltipText": text,
        "position": position,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("tooltip", props=props, style=style_dict)


# =============================================================================
# Additional Input Components
# =============================================================================


def number_input(
    label: str = "",
    *,
    key: str | None = None,
    value: float = 0,
    min_value: float | None = None,
    max_value: float | None = None,
    step: float = 1,
    disabled: bool = False,
    style: Style | None = None,
) -> float:
    """
    Create a number input with increment/decrement buttons.

    Args:
        label: Input label
        key: State key
        value: Default value
        min_value: Minimum value
        max_value: Maximum value
        step: Step increment
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Current value
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_number_{label or 'default'}"
    current_value = state.setdefault(state_key, value)

    props = {
        "label": label,
        "value": current_value,
        "min": min_value,
        "max": max_value,
        "step": step,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("number_input", props=props, style=style_dict)

    return current_value


def search_input(
    placeholder: str = "Search...",
    *,
    key: str | None = None,
    value: str = "",
    debounce: int = 300,
    style: Style | None = None,
) -> str:
    """
    Create a search input with icon and debounced updates.

    Args:
        placeholder: Placeholder text
        key: State key
        value: Default value
        debounce: Debounce delay in ms
        style: Optional Style object

    Returns:
        Current search value
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or "_search"
    current_value = state.setdefault(state_key, value)

    props = {
        "placeholder": placeholder,
        "value": current_value,
        "debounce": debounce,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("search_input", props=props, style=style_dict)

    return current_value


def rating(
    label: str = "",
    *,
    key: str | None = None,
    value: int = 0,
    max_value: int = 5,
    disabled: bool = False,
    style: Style | None = None,
) -> int:
    """
    Create a star rating input.

    Args:
        label: Input label
        key: State key
        value: Default value
        max_value: Maximum stars
        disabled: Whether disabled
        style: Optional Style object

    Returns:
        Current rating
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_rating_{label or 'default'}"
    current_value = state.setdefault(state_key, value)

    props = {
        "label": label,
        "value": current_value,
        "maxValue": max_value,
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("rating", props=props, style=style_dict)

    return current_value


def tag_input(
    label: str = "",
    *,
    key: str | None = None,
    value: list[str] | None = None,
    placeholder: str = "Add tag...",
    max_tags: int | None = None,
    suggestions: list[str] | None = None,
    style: Style | None = None,
) -> list[str]:
    """
    Create a tag/chip input.

    Args:
        label: Input label
        key: State key
        value: Default tags
        placeholder: Input placeholder
        max_tags: Maximum number of tags
        suggestions: Autocomplete suggestions
        style: Optional Style object

    Returns:
        List of tags
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_tags_{label or 'default'}"
    current_value = state.setdefault(state_key, value or [])

    props = {
        "label": label,
        "value": current_value,
        "placeholder": placeholder,
        "maxTags": max_tags,
        "suggestions": suggestions,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("tag_input", props=props, style=style_dict)

    return current_value


# =============================================================================
# Display Components
# =============================================================================


def badge(
    text: str,
    *,
    variant: str = "default",
    size: str = "md",
    style: Style | None = None,
) -> None:
    """
    Display a badge/chip.

    Args:
        text: Badge text
        variant: Badge variant ('default', 'success', 'warning', 'error', 'info')
        size: Badge size ('sm', 'md', 'lg')
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "text": text,
        "variant": variant,
        "size": size,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("badge", props=props, style=style_dict)


def avatar(
    src: str | None = None,
    *,
    name: str | None = None,
    size: str = "md",
    style: Style | None = None,
) -> None:
    """
    Display an avatar.

    Args:
        src: Image URL
        name: Fallback name for initials
        size: Avatar size ('sm', 'md', 'lg', 'xl')
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "src": src,
        "name": name,
        "size": size,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("avatar", props=props, style=style_dict)


def avatar_group(
    avatars: list[dict[str, str]],
    *,
    max_display: int = 4,
    size: str = "md",
    style: Style | None = None,
) -> None:
    """
    Display a group of overlapping avatars.

    Args:
        avatars: List of avatar dicts with 'src' and/or 'name'
        max_display: Max avatars to show before +N
        size: Avatar size
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "avatars": avatars,
        "maxDisplay": max_display,
        "size": size,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("avatar_group", props=props, style=style_dict)


def stat_card(
    title: str,
    value: str,
    *,
    description: str | None = None,
    icon: str | None = None,
    trend: float | None = None,
    trend_label: str | None = None,
    style: Style | None = None,
) -> None:
    """
    Display a statistic card with icon and trend.

    Args:
        title: Stat title
        value: Stat value
        description: Optional description
        icon: Icon name
        trend: Trend percentage
        trend_label: Trend label
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "title": title,
        "value": value,
        "description": description,
        "icon": icon,
        "trend": trend,
        "trendLabel": trend_label,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("stat_card", props=props, style=style_dict)


def empty_state(
    title: str,
    *,
    description: str | None = None,
    icon: str | None = None,
    action_label: str | None = None,
    key: str | None = None,
    style: Style | None = None,
) -> bool:
    """
    Display an empty state placeholder.

    Args:
        title: Title text
        description: Description text
        icon: Icon name
        action_label: Action button label
        key: State key for button
        style: Optional Style object

    Returns:
        True if action button was clicked
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or f"_empty_{title}"
    was_clicked = bool(state.get(f"{state_key}_clicked", False))
    if was_clicked:
        state.update(**{f"{state_key}_clicked": False})

    props = {
        "title": title,
        "description": description,
        "icon": icon,
        "actionLabel": action_label,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("empty_state", props=props, style=style_dict)

    return was_clicked


def loading_skeleton(
    *,
    variant: str = "text",
    lines: int = 3,
    height: str | None = None,
    style: Style | None = None,
) -> None:
    """
    Display a loading skeleton placeholder.

    Args:
        variant: Skeleton type ('text', 'card', 'avatar', 'image')
        lines: Number of lines for text variant
        height: Custom height
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "variant": variant,
        "lines": lines,
        "height": height,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("skeleton", props=props, style=style_dict)


def timeline(
    items: list[dict[str, Any]],
    *,
    style: Style | None = None,
) -> None:
    """
    Display a timeline of events.

    Args:
        items: List of timeline items with 'title', 'description', 'date', 'icon'
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "items": items,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("timeline", props=props, style=style_dict)


def steps(
    items: list[str],
    *,
    current: int = 0,
    key: str | None = None,
    clickable: bool = False,
    style: Style | None = None,
) -> int:
    """
    Display a step indicator/wizard.

    Args:
        items: List of step labels
        current: Current step index
        key: State key
        clickable: Allow clicking to navigate
        style: Optional Style object

    Returns:
        Current step index
    """
    ctx = get_context()
    state = get_session_state()

    state_key = key or "_steps"
    step = state.setdefault(state_key, current)

    props = {
        "items": items,
        "current": step,
        "clickable": clickable,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("steps", props=props, style=style_dict)

    return step


# =============================================================================
# Chart Components (Simple built-in charts)
# =============================================================================


def line_chart(
    data: list[dict[str, Any]],
    *,
    x: str,
    y: str | list[str],
    title: str | None = None,
    height: str = "300px",
    colors: list[str] | None = None,
    style: Style | None = None,
) -> None:
    """
    Display a line chart.

    Args:
        data: List of data points
        x: Key for x-axis values
        y: Key(s) for y-axis values
        title: Chart title
        height: Chart height
        colors: Line colors
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "data": data,
        "x": x,
        "y": y if isinstance(y, list) else [y],
        "title": title,
        "height": height,
        "colors": colors,
        "chartType": "line",
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("chart", props=props, style=style_dict)


def bar_chart(
    data: list[dict[str, Any]],
    *,
    x: str,
    y: str | list[str],
    title: str | None = None,
    height: str = "300px",
    colors: list[str] | None = None,
    horizontal: bool = False,
    stacked: bool = False,
    style: Style | None = None,
) -> None:
    """
    Display a bar chart.

    Args:
        data: List of data points
        x: Key for x-axis values
        y: Key(s) for y-axis values
        title: Chart title
        height: Chart height
        colors: Bar colors
        horizontal: Horizontal bars
        stacked: Stacked bars
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "data": data,
        "x": x,
        "y": y if isinstance(y, list) else [y],
        "title": title,
        "height": height,
        "colors": colors,
        "horizontal": horizontal,
        "stacked": stacked,
        "chartType": "bar",
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("chart", props=props, style=style_dict)


def area_chart(
    data: list[dict[str, Any]],
    *,
    x: str,
    y: str | list[str],
    title: str | None = None,
    height: str = "300px",
    colors: list[str] | None = None,
    stacked: bool = False,
    style: Style | None = None,
) -> None:
    """
    Display an area chart.

    Args:
        data: List of data points
        x: Key for x-axis values
        y: Key(s) for y-axis values
        title: Chart title
        height: Chart height
        colors: Area colors
        stacked: Stacked areas
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "data": data,
        "x": x,
        "y": y if isinstance(y, list) else [y],
        "title": title,
        "height": height,
        "colors": colors,
        "stacked": stacked,
        "chartType": "area",
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("chart", props=props, style=style_dict)


def pie_chart(
    data: list[dict[str, Any]],
    *,
    label: str,
    value: str,
    title: str | None = None,
    height: str = "300px",
    colors: list[str] | None = None,
    donut: bool = False,
    style: Style | None = None,
) -> None:
    """
    Display a pie/donut chart.

    Args:
        data: List of data points
        label: Key for labels
        value: Key for values
        title: Chart title
        height: Chart height
        colors: Slice colors
        donut: Donut style
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "data": data,
        "label": label,
        "value": value,
        "title": title,
        "height": height,
        "colors": colors,
        "donut": donut,
        "chartType": "pie",
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("chart", props=props, style=style_dict)


# =============================================================================
# Utility Components
# =============================================================================


def copy_button(
    text: str,
    *,
    label: str = "Copy",
    success_label: str = "Copied!",
    style: Style | None = None,
) -> None:
    """
    Display a button that copies text to clipboard.

    Args:
        text: Text to copy
        label: Button label
        success_label: Label after copying
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "text": text,
        "label": label,
        "successLabel": success_label,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("copy_button", props=props, style=style_dict)


def json_viewer(
    data: Any,
    *,
    expanded: bool = True,
    max_depth: int = 3,
    style: Style | None = None,
) -> None:
    """
    Display JSON data in a collapsible tree view.

    Args:
        data: JSON-serializable data
        expanded: Initially expanded
        max_depth: Maximum expansion depth
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "data": data,
        "expanded": expanded,
        "maxDepth": max_depth,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("json_viewer", props=props, style=style_dict)


def html(
    content: str,
    *,
    style: Style | None = None,
) -> None:
    """
    Render raw HTML content.

    WARNING: Only use with trusted content to avoid XSS vulnerabilities.

    Args:
        content: HTML string
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "content": content,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("html", props=props, style=style_dict)


def iframe(
    src: str,
    *,
    height: str = "400px",
    width: str = "100%",
    title: str = "Embedded content",
    style: Style | None = None,
) -> None:
    """
    Embed an iframe.

    Args:
        src: Source URL
        height: Frame height
        width: Frame width
        title: Accessibility title
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "src": src,
        "height": height,
        "width": width,
        "title": title,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("iframe", props=props, style=style_dict)


# =============================================================================
# Smart Write Function (like st.write)
# =============================================================================


def write(*args, **kwargs) -> None:
    """
    Write arguments to the app. Handles multiple types intelligently.

    Supports: strings, numbers, dataframes, dicts, lists, markdown, etc.
    Similar to st.write() - the Swiss Army knife of output.

    Args:
        *args: Arguments to write (strings, dicts, dataframes, etc.)
        **kwargs: Additional options (unsafe_allow_html, etc.)
    """
    get_context()
    kwargs.get("unsafe_allow_html", False)

    for arg in args:
        if arg is None:
            continue
        elif isinstance(arg, str):
            # Check if it looks like markdown
            if any(c in arg for c in ["#", "*", "`", "[", ">"]):
                markdown(arg)
            else:
                text(arg)
        elif isinstance(arg, (int, float)):
            text(str(arg))
        elif isinstance(arg, dict):
            json_viewer(arg)
        elif isinstance(arg, (list, tuple)):
            # Check if it's a list of dicts (table-like)
            if arg and isinstance(arg[0], dict):
                dataframe(arg)
            else:
                json_viewer(list(arg))
        elif hasattr(arg, "to_dict"):
            # Pandas DataFrame or similar
            dataframe(arg)
        elif hasattr(arg, "__html__"):
            html(arg.__html__())
        else:
            text(str(arg))


# =============================================================================
# Additional Text Components
# =============================================================================


def title(
    content: str,
    *,
    anchor: str | None = None,
    style: Style | None = None,
) -> None:
    """
    Display a title (largest heading).

    Args:
        content: Title text
        anchor: Optional anchor ID for linking
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "content": content,
        "level": "title",
        "anchor": anchor,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("heading", props=props, style=style_dict)


def caption(
    content: str,
    *,
    unsafe_allow_html: bool = False,
    style: Style | None = None,
) -> None:
    """
    Display small caption text.

    Args:
        content: Caption text
        unsafe_allow_html: Allow HTML in content
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "content": content,
        "variant": "caption",
        "unsafe_allow_html": unsafe_allow_html,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("text", props=props, style=style_dict)


def latex(
    content: str,
    *,
    style: Style | None = None,
) -> None:
    """
    Display mathematical expressions using LaTeX notation.

    Args:
        content: LaTeX expression (e.g., r"e^{i\\pi} + 1 = 0")
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "content": content,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("latex", props=props, style=style_dict)


def echo(code_location: str = "above"):
    """
    Context manager to display code and run it.

    Args:
        code_location: Where to show code ('above' or 'below')

    Usage:
        with um.echo():
            x = 10
            um.write(x)
    """
    import inspect

    class EchoContext:
        def __init__(self, location):
            self.location = location
            self.frame = None

        def __enter__(self):
            self.frame = inspect.currentframe().f_back
            return self

        def __exit__(self, *args):
            # Get the source code of the with block
            try:
                lineno = self.frame.f_lineno
                # This is a simplified version - real implementation would parse AST
                code(f"# Code executed at line {lineno}", language="python")
            except (AttributeError, TypeError):
                # Frame may not be available in all contexts
                pass

    return EchoContext(code_location)


# =============================================================================
# Additional Button Variants
# =============================================================================


def download_button(
    label: str,
    data: str | bytes | Callable[[], str | bytes],
    *,
    file_name: str = "download.txt",
    mime: str | None = None,
    key: str | None = None,
    disabled: bool = False,
    variant: str = "secondary",
    on_click: Callable[[], None] | None = None,
    style: Style | None = None,
) -> bool:
    """
    Display a download button.

    Supports static data, bytes, or a callable that generates data on-demand.
    Common use cases include generating CSVs, PDFs, or other files dynamically.

    Args:
        label: Button label
        data: Data to download. Can be:
            - str: Text content
            - bytes: Binary content
            - Callable: Function that returns str or bytes (called on click)
        file_name: Name for downloaded file
        mime: MIME type of the file (auto-detected if None)
        key: Unique key for the widget
        disabled: Whether button is disabled
        variant: Button style variant
        on_click: Optional callback when button is clicked
        style: Optional Style object

    Returns:
        True if button was clicked

    Example:
        # Static data
        um.download_button("Download", "Hello, World!", file_name="hello.txt")

        # Dynamic CSV generation
        def generate_csv():
            import io
            df.to_csv(buf := io.StringIO())
            return buf.getvalue()

        um.download_button("Export CSV", generate_csv, file_name="data.csv")

        # Dynamic PDF
        def generate_pdf():
            return create_pdf_bytes()

        um.download_button("Export PDF", generate_pdf, file_name="report.pdf")
    """
    import base64

    ctx = get_context()
    component_key = key or f"download_button_{id(label)}"

    # Handle callable data (dynamic generation)
    if callable(data):
        # Generate data now (will be re-generated on each render)
        actual_data = data()
    else:
        actual_data = data

    # Convert data to base64 if bytes
    if isinstance(actual_data, bytes):
        data_str = base64.b64encode(actual_data).decode("utf-8")
        is_binary = True
    else:
        data_str = actual_data
        is_binary = False

    # Auto-detect MIME type from file extension if not provided
    if mime is None:
        mime = _get_mime_type(file_name)

    props = {
        "label": label,
        "data": data_str,
        "file_name": file_name,
        "mime": mime,
        "is_binary": is_binary,
        "disabled": disabled,
        "variant": variant,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("download_button", key=component_key, props=props, style=style_dict)

    state = get_session_state()
    was_clicked = bool(state.get(component_key, False))

    # Execute on_click callback if provided
    if was_clicked and on_click:
        on_click()

    return was_clicked


def _get_mime_type(filename: str) -> str:
    """Auto-detect MIME type from file extension."""
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    mime_types = {
        # Text
        "txt": "text/plain",
        "csv": "text/csv",
        "json": "application/json",
        "xml": "application/xml",
        "html": "text/html",
        "htm": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "md": "text/markdown",
        # Images
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "svg": "image/svg+xml",
        "webp": "image/webp",
        "ico": "image/x-icon",
        # Documents
        "pdf": "application/pdf",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "ppt": "application/vnd.ms-powerpoint",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        # Archives
        "zip": "application/zip",
        "tar": "application/x-tar",
        "gz": "application/gzip",
        "rar": "application/vnd.rar",
        "7z": "application/x-7z-compressed",
        # Audio/Video
        "mp3": "audio/mpeg",
        "wav": "audio/wav",
        "mp4": "video/mp4",
        "webm": "video/webm",
        # Data
        "parquet": "application/octet-stream",
        "feather": "application/octet-stream",
        "pickle": "application/octet-stream",
        "pkl": "application/octet-stream",
    }
    return mime_types.get(ext, "application/octet-stream")


def link_button(
    label: str,
    url: str,
    *,
    disabled: bool = False,
    variant: str = "secondary",
    style: Style | None = None,
) -> None:
    """
    Display a button that links to a URL.

    Args:
        label: Button label
        url: URL to open when clicked
        disabled: Whether button is disabled
        variant: Button style variant
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "label": label,
        "url": url,
        "disabled": disabled,
        "variant": variant,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("link_button", props=props, style=style_dict)


# =============================================================================
# Form Components
# =============================================================================


@contextmanager
def form(
    key: str,
    *,
    clear_on_submit: bool = False,
    border: bool = True,
    style: Style | None = None,
):
    """
    Create a form that batches input widgets.

    All widgets inside a form are submitted together when form_submit_button is clicked.

    Args:
        key: Unique key for the form
        clear_on_submit: Clear form values after submit
        border: Show border around form
        style: Optional Style object

    Usage:
        with um.form('my_form'):
            name = um.input('Name')
            if um.form_submit_button('Submit'):
                um.success(f'Hello {name}')
    """
    ctx = get_context()
    props = {
        "form_key": key,
        "clear_on_submit": clear_on_submit,
        "border": border,
    }
    style_dict = style.to_dict() if style else None

    with ctx.container("form", props=props, style=style_dict):
        yield


def form_submit_button(
    label: str = "Submit",
    *,
    disabled: bool = False,
    variant: str = "primary",
    style: Style | None = None,
) -> bool:
    """
    Display a form submit button. Only works inside a form context.

    Args:
        label: Button label
        disabled: Whether button is disabled
        variant: Button style variant
        style: Optional Style object

    Returns:
        True if the form was submitted
    """
    ctx = get_context()
    props = {
        "label": label,
        "disabled": disabled,
        "variant": variant,
        "is_form_submit": True,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("form_submit_button", props=props, style=style_dict)

    state = get_session_state()
    # Check if form was submitted
    return bool(state.get("_form_submitted", False))


# =============================================================================
# Toast Notifications
# =============================================================================


def toast(
    message: str,
    *,
    icon: str | None = None,
    duration: int = 4000,
) -> None:
    """
    Display a toast notification.

    Args:
        message: Message to display
        icon: Optional icon (emoji or icon name)
        duration: How long to show toast (milliseconds)
    """
    ctx = get_context()
    props = {
        "message": message,
        "icon": icon,
        "duration": duration,
    }
    ctx.create_component("toast", props=props)


# =============================================================================
# Status Components
# =============================================================================


@contextmanager
def status(
    label: str,
    *,
    expanded: bool = True,
    state: str = "running",
    style: Style | None = None,
):
    """
    Display a status container with expandable details.

    Args:
        label: Status label
        expanded: Whether details are expanded
        state: Status state ('running', 'complete', 'error')
        style: Optional Style object

    Usage:
        with um.status('Processing...') as s:
            um.write('Step 1...')
            s.update(label='Almost done...')
            um.write('Step 2...')
        s.update(label='Done!', state='complete')
    """
    ctx = get_context()

    class StatusUpdater:
        def __init__(self):
            self.label = label
            self.state = state

        def update(
            self, label: str | None = None, state: str | None = None, expanded: bool | None = None
        ):
            if label:
                self.label = label
            if state:
                self.state = state

    updater = StatusUpdater()
    props = {
        "label": label,
        "expanded": expanded,
        "state": state,
    }
    style_dict = style.to_dict() if style else None

    with ctx.container("status", props=props, style=style_dict):
        yield updater


def exception(e: Exception) -> None:
    """
    Display an exception with traceback.

    Args:
        e: Exception to display
    """
    import traceback

    ctx = get_context()
    tb = traceback.format_exception(type(e), e, e.__traceback__)
    props = {
        "exception_type": type(e).__name__,
        "message": str(e),
        "traceback": "".join(tb),
    }
    ctx.create_component("exception", props=props)


# =============================================================================
# Additional Input Widgets
# =============================================================================


def select_slider(
    label: str,
    options: list[Any],
    *,
    value: Any | None = None,
    key: str | None = None,
    disabled: bool = False,
    label_visibility: str = "visible",
    style: Style | None = None,
) -> Any:
    """
    Display a slider that selects from a list of options.

    Args:
        label: Slider label
        options: List of options to select from
        value: Default value
        key: Unique key for the widget
        disabled: Whether slider is disabled
        label_visibility: 'visible', 'hidden', or 'collapsed'
        style: Optional Style object

    Returns:
        Selected option value
    """
    ctx = get_context()
    component_key = key or f"select_slider_{id(label)}"

    default_value = value if value is not None else options[0] if options else None

    props = {
        "label": label,
        "options": options,
        "default": default_value,
        "disabled": disabled,
        "label_visibility": label_visibility,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("select_slider", key=component_key, props=props, style=style_dict)

    state = get_session_state()
    return state.get(component_key, default_value)


def pills(
    label: str,
    options: list[str],
    *,
    selection_mode: str = "single",
    default: str | list[str] | None = None,
    key: str | None = None,
    disabled: bool = False,
    style: Style | None = None,
) -> str | list[str] | None:
    """
    Display pill-shaped selection buttons.

    Args:
        label: Label for the pills
        options: List of pill options
        selection_mode: 'single' or 'multi'
        default: Default selection
        key: Unique key for the widget
        disabled: Whether pills are disabled
        style: Optional Style object

    Returns:
        Selected option(s)
    """
    ctx = get_context()
    component_key = key or f"pills_{id(label)}"

    props = {
        "label": label,
        "options": options,
        "selection_mode": selection_mode,
        "default": default,
        "disabled": disabled,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("pills", key=component_key, props=props, style=style_dict)

    state = get_session_state()
    result = state.get(component_key, default)
    # Cast to expected return type
    if isinstance(result, str):
        return result
    if isinstance(result, list):
        return result
    return None


def feedback(
    sentiment_mapping: dict[int, str] | None = None,
    *,
    key: str | None = None,
    disabled: bool = False,
    style: Style | None = None,
) -> int | None:
    """
    Display a feedback widget (thumbs up/down or star rating).

    Args:
        sentiment_mapping: Dict mapping scores to labels, e.g., {0: "Bad", 1: "Good"}
        key: Unique key for the widget
        disabled: Whether widget is disabled
        style: Optional Style object

    Returns:
        Selected feedback score or None
    """
    ctx = get_context()
    component_key = key or f"feedback_{id(sentiment_mapping)}"

    actual_mapping: dict[int, str]
    if sentiment_mapping is None:
        actual_mapping = {0: "Thumbs down", 1: "Thumbs up"}
    else:
        actual_mapping = sentiment_mapping

    props = {
        "sentiment_mapping": actual_mapping,
        "disabled": disabled,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("feedback", key=component_key, props=props, style=style_dict)

    state = get_session_state()
    return state.get(component_key, None)


def segmented_control(
    label: str,
    options: list[str],
    *,
    default: str | None = None,
    key: str | None = None,
    disabled: bool = False,
    style: Style | None = None,
) -> str | None:
    """
    Display a segmented control (button group for single selection).

    Args:
        label: Label for the control
        options: List of options
        default: Default selected option
        key: Unique key for the widget
        disabled: Whether control is disabled
        style: Optional Style object

    Returns:
        Selected option
    """
    ctx = get_context()
    component_key = key or f"segmented_{id(label)}"

    default_value = default if default else options[0] if options else None

    props = {
        "label": label,
        "options": options,
        "default": default_value,
        "disabled": disabled,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("segmented_control", key=component_key, props=props, style=style_dict)

    state = get_session_state()
    return state.get(component_key, default_value)


def camera_input(
    label: str,
    *,
    key: str | None = None,
    disabled: bool = False,
    label_visibility: str = "visible",
    style: Style | None = None,
) -> bytes | None:
    """
    Display a camera input widget for taking photos.

    Args:
        label: Widget label
        key: Unique key for the widget
        disabled: Whether input is disabled
        label_visibility: 'visible', 'hidden', or 'collapsed'
        style: Optional Style object

    Returns:
        Image data as bytes or None
    """
    ctx = get_context()
    component_key = key or f"camera_{id(label)}"

    props = {
        "label": label,
        "disabled": disabled,
        "label_visibility": label_visibility,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("camera_input", key=component_key, props=props, style=style_dict)

    state = get_session_state()
    return state.get(component_key, None)


def audio_input(
    label: str,
    *,
    key: str | None = None,
    disabled: bool = False,
    style: Style | None = None,
) -> bytes | None:
    """
    Display an audio recording input.

    Args:
        label: Widget label
        key: Unique key for the widget
        disabled: Whether input is disabled
        style: Optional Style object

    Returns:
        Audio data as bytes or None
    """
    ctx = get_context()
    component_key = key or f"audio_input_{id(label)}"

    props = {
        "label": label,
        "disabled": disabled,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("audio_input", key=component_key, props=props, style=style_dict)

    state = get_session_state()
    return state.get(component_key, None)


# =============================================================================
# Additional Chart Components
# =============================================================================


def scatter_chart(
    data: list[dict] | Any,
    *,
    x: str | None = None,
    y: str | None = None,
    color: str | None = None,
    size: str | None = None,
    title: str | None = None,
    height: str = "300px",
    style: Style | None = None,
) -> None:
    """
    Display a scatter chart.

    Args:
        data: Data to plot (list of dicts or DataFrame)
        x: Column name for x-axis
        y: Column name for y-axis
        color: Column name for color encoding
        size: Column name for size encoding
        title: Chart title
        height: Chart height
        style: Optional Style object
    """
    ctx = get_context()

    if hasattr(data, "to_dict"):
        data = data.to_dict("records")

    props = {
        "data": data,
        "x": x,
        "y": y,
        "color": color,
        "size": size,
        "title": title,
        "height": height,
        "chart_type": "scatter",
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("chart", props=props, style=style_dict)


def map(
    data: list[dict] | Any | None = None,
    *,
    latitude: str = "lat",
    longitude: str = "lon",
    zoom: int = 10,
    height: str = "400px",
    style: Style | None = None,
) -> None:
    """
    Display a map with optional data points.

    Args:
        data: Data with lat/lon columns (list of dicts or DataFrame)
        latitude: Column name for latitude
        longitude: Column name for longitude
        zoom: Initial zoom level
        height: Map height
        style: Optional Style object
    """
    ctx = get_context()

    if data is not None and hasattr(data, "to_dict"):
        data = data.to_dict("records")

    props = {
        "data": data,
        "latitude": latitude,
        "longitude": longitude,
        "zoom": zoom,
        "height": height,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("map", props=props, style=style_dict)


# =============================================================================
# Plotly Charts
# =============================================================================


def plotly_chart(
    figure: Any,
    *,
    use_container_width: bool = True,
    theme: str | None = None,
    key: str | None = None,
    style: Style | None = None,
) -> None:
    """
    Display a Plotly chart.

    Supports any Plotly figure object (go.Figure, px charts, etc).
    The Plotly.js library is automatically loaded from CDN.

    Args:
        figure: A Plotly figure object (go.Figure or plotly express chart)
        use_container_width: If True, chart uses full container width
        theme: Override the Plotly theme ('plotly', 'plotly_white', 'plotly_dark', etc.)
        key: Unique key for the component
        style: Optional Style object

    Example:
        import plotly.express as px
        import umara as um

        fig = px.line(df, x='date', y='value', title='My Chart')
        um.plotly_chart(fig)
    """
    ctx = get_context()

    # Convert figure to JSON for frontend rendering
    if hasattr(figure, "to_json"):
        # Plotly figure object
        import json

        figure_json = json.loads(figure.to_json())
    elif isinstance(figure, dict):
        # Already a dict representation
        figure_json = figure
    else:
        raise ValueError(
            "figure must be a Plotly figure object or dict. "
            "Install plotly with: pip install plotly"
        )

    props = {
        "figure": figure_json,
        "use_container_width": use_container_width,
        "theme": theme,
        "key": key,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("plotly_chart", props=props, style=style_dict)


# =============================================================================
# Streaming Output
# =============================================================================


def write_stream(
    stream: Any,
    *,
    key: str | None = None,
    style: Style | None = None,
) -> str:
    """
    Write a streaming response, yielding chunks as they arrive.

    Ideal for displaying LLM responses that stream token-by-token.
    Works with any iterator/generator that yields strings.

    Args:
        stream: An iterator/generator that yields string chunks
        key: Unique key for the component
        style: Optional Style object

    Returns:
        The complete concatenated response string

    Example:
        import umara as um
        import openai

        client = openai.OpenAI()
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Tell me a story"}],
            stream=True
        )

        # Extracts content from OpenAI stream objects automatically
        response = um.write_stream(stream)
    """
    ctx = get_context()

    # Generate a unique key for this stream
    if key is None:
        import uuid

        key = f"_stream_{uuid.uuid4().hex[:8]}"

    # Collect all chunks
    full_response = []

    # Create the streaming text container
    props = {
        "key": key,
        "streaming": True,
        "content": "",
    }

    style_dict = style.to_dict() if style else None
    component = ctx.create_component("streaming_text", props=props, style=style_dict)
    component_id = component.id

    # Process the stream
    for chunk in stream:
        # Handle different stream formats
        if isinstance(chunk, str):
            text = chunk
        elif hasattr(chunk, "choices"):
            # OpenAI-style response
            delta = chunk.choices[0].delta if chunk.choices else None
            text = delta.content if delta and hasattr(delta, "content") and delta.content else ""
        elif hasattr(chunk, "text"):
            # Anthropic-style response
            text = chunk.text if chunk.text else ""
        elif hasattr(chunk, "content"):
            # Generic content attribute
            text = chunk.content if chunk.content else ""
        else:
            # Try string conversion
            text = str(chunk)

        if text:
            full_response.append(text)
            # Update the component with new content
            ctx.update_component(
                component_id, {"content": "".join(full_response), "streaming": True}
            )

    # Mark streaming as complete
    final_text = "".join(full_response)
    ctx.update_component(component_id, {"content": final_text, "streaming": False})

    return final_text


# =============================================================================
# Data Editor
# =============================================================================


def data_editor(
    data: list[dict] | Any,
    *,
    num_rows: str = "fixed",
    disabled: bool | list[str] = False,
    column_config: dict | None = None,
    hide_index: bool = True,
    key: str | None = None,
    height: str | None = None,
    style: Style | None = None,
) -> list[dict] | Any:
    """
    Display an editable dataframe.

    Args:
        data: Data to edit (list of dicts or DataFrame)
        num_rows: 'fixed' or 'dynamic' (allow adding/deleting rows)
        disabled: True to disable all, or list of column names to disable
        column_config: Column configuration dict
        hide_index: Hide row index
        key: Unique key for the widget
        height: Fixed height for the editor
        style: Optional Style object

    Returns:
        Edited data in same format as input
    """
    ctx = get_context()
    component_key = key or f"data_editor_{id(data)}"

    is_dataframe = hasattr(data, "to_dict") and callable(getattr(data, "to_dict"))
    if is_dataframe:
        data_list = data.to_dict("records")  # type: ignore[union-attr]
    else:
        data_list = data

    props = {
        "data": data_list,
        "num_rows": num_rows,
        "disabled": disabled,
        "column_config": column_config,
        "hide_index": hide_index,
        "height": height,
    }

    style_dict = style.to_dict() if style else None
    ctx.create_component("data_editor", key=component_key, props=props, style=style_dict)

    state = get_session_state()
    edited_data = state.get(component_key, data_list)

    # Convert back to DataFrame if input was DataFrame
    if is_dataframe and edited_data:
        try:
            import pandas as pd

            return pd.DataFrame(edited_data)
        except ImportError:
            return edited_data

    return edited_data


# =============================================================================
# Dialog (Improved Modal)
# =============================================================================


@contextmanager
def dialog(
    title: str,
    *,
    width: str = "medium",
    style: Style | None = None,
):
    """
    Create a dialog/modal window.

    Args:
        title: Dialog title
        width: Dialog width ('small', 'medium', 'large')
        style: Optional Style object

    Usage:
        @um.dialog('Settings')
        def settings_dialog():
            um.write('Dialog content')
            if um.button('Close'):
                um.rerun()

        if um.button('Open Settings'):
            settings_dialog()
    """
    ctx = get_context()
    props = {
        "title": title,
        "width": width,
    }
    style_dict = style.to_dict() if style else None

    with ctx.container("dialog", props=props, style=style_dict):
        yield


# =============================================================================
# Page Configuration
# =============================================================================


def set_page_config(
    page_title: str | None = None,
    page_icon: str | None = None,
    layout: str = "centered",
    initial_sidebar_state: str = "auto",
    menu_items: dict[str, str] | None = None,
) -> None:
    """
    Configure the page. Must be called before any other Umara commands.

    Args:
        page_title: Page title shown in browser tab
        page_icon: Page icon (emoji or URL)
        layout: 'centered' or 'wide'
        initial_sidebar_state: 'auto', 'expanded', or 'collapsed'
        menu_items: Custom menu items dict
    """
    from umara.core import get_app

    app = get_app()

    if page_title:
        app.title = page_title

    app.config = {
        "page_icon": page_icon,
        "layout": layout,
        "initial_sidebar_state": initial_sidebar_state,
        "menu_items": menu_items or {},
    }


# =============================================================================
# Execution Flow
# =============================================================================


def rerun() -> None:
    """
    Rerun the app from the top.

    Raises a special exception to trigger a rerun.
    """
    from umara.core import RerunException

    raise RerunException()


def stop() -> None:
    """
    Stop execution of the app at this point.

    Raises a special exception to stop execution.
    """
    from umara.core import StopException

    raise StopException()


# =============================================================================
# Logo Component
# =============================================================================


def logo(
    image: str,
    *,
    link: str | None = None,
    icon_image: str | None = None,
    style: Style | None = None,
) -> None:
    """
    Display an app logo in the sidebar.

    Args:
        image: Logo image URL or path
        link: Optional URL to link to when logo is clicked
        icon_image: Optional smaller icon version for collapsed sidebar
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "image": image,
        "link": link,
        "icon_image": icon_image,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("logo", props=props, style=style_dict)
