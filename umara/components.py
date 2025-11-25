"""
UI Components for Umara.

All components are designed to be beautiful by default with
polished styling out of the box.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union
from contextlib import contextmanager
from dataclasses import dataclass

from umara.core import get_context, ContainerContext, Component
from umara.state import get_session_state
from umara.style import Style


# =============================================================================
# Typography Components
# =============================================================================

def text(
    content: str,
    *,
    style: Optional[Style] = None,
    color: Optional[str] = None,
    size: Optional[str] = None,
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
    style: Optional[Style] = None,
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
    style: Optional[Style] = None,
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
    style: Optional[Style] = None,
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
    style: Optional[Style] = None,
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

def success(message: str, *, style: Optional[Style] = None) -> None:
    """Display a success message."""
    ctx = get_context()
    props = {"message": message}
    style_dict = style.to_dict() if style else None
    ctx.create_component("success", props=props, style=style_dict)


def error(message: str, *, style: Optional[Style] = None) -> None:
    """Display an error message."""
    ctx = get_context()
    props = {"message": message}
    style_dict = style.to_dict() if style else None
    ctx.create_component("error", props=props, style=style_dict)


def warning(message: str, *, style: Optional[Style] = None) -> None:
    """Display a warning message."""
    ctx = get_context()
    props = {"message": message}
    style_dict = style.to_dict() if style else None
    ctx.create_component("warning", props=props, style=style_dict)


def info(message: str, *, style: Optional[Style] = None) -> None:
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
    padding: Optional[str] = None,
    margin: Optional[str] = None,
    style: Optional[Style] = None,
):
    """
    Create a container for grouping elements.

    Args:
        padding: Container padding
        margin: Container margin
        style: Optional Style object
    """
    ctx = get_context()
    style_dict = style.to_dict() if style else {}
    if padding:
        style_dict["padding"] = padding
    if margin:
        style_dict["margin"] = margin

    component = ctx.create_component("container", style=style_dict or None)
    with ContainerContext(component):
        yield


@contextmanager
def columns(
    count: int = 2,
    *,
    gap: str = "16px",
    style: Optional[Style] = None,
):
    """
    Create a column layout.

    Args:
        count: Number of columns
        gap: Gap between columns
        style: Optional Style object
    """
    ctx = get_context()
    props = {"count": count, "gap": gap}
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("columns", props=props, style=style_dict)
    with ContainerContext(component):
        yield


@contextmanager
def column(*, style: Optional[Style] = None):
    """Create a single column within a columns layout."""
    ctx = get_context()
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("column", style=style_dict)
    with ContainerContext(component):
        yield


@contextmanager
def grid(
    columns: Union[int, str] = 3,
    *,
    gap: str = "16px",
    row_gap: Optional[str] = None,
    style: Optional[Style] = None,
):
    """
    Create a CSS grid layout.

    Args:
        columns: Number of columns or CSS grid-template-columns value
        gap: Gap between items
        row_gap: Vertical gap (defaults to gap)
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "columns": columns,
        "gap": gap,
        "rowGap": row_gap or gap,
    }
    style_dict = style.to_dict() if style else None
    component = ctx.create_component("grid", props=props, style=style_dict)
    with ContainerContext(component):
        yield


@contextmanager
def card(
    *,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    padding: str = "24px",
    shadow: str = "md",
    style: Optional[Style] = None,
):
    """
    Create a card component with beautiful default styling.

    Args:
        title: Optional card title
        subtitle: Optional card subtitle
        padding: Card padding
        shadow: Shadow size (sm, md, lg, xl)
        style: Optional Style object
    """
    ctx = get_context()
    props = {
        "title": title,
        "subtitle": subtitle,
        "padding": padding,
        "shadow": shadow,
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
    tab_names: List[str],
    *,
    default: int = 0,
    key: Optional[str] = None,
    style: Optional[Style] = None,
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


def divider(*, style: Optional[Style] = None) -> None:
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
    key: Optional[str] = None,
    variant: str = "primary",
    disabled: bool = False,
    full_width: bool = False,
    icon: Optional[str] = None,
    style: Optional[Style] = None,
) -> bool:
    """
    Create a button.

    Args:
        label: Button label
        key: Unique key for the button
        variant: Button style ('primary', 'secondary', 'outline', 'ghost', 'danger')
        disabled: Whether button is disabled
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
    was_clicked = state.get(f"{state_key}_clicked", False)

    # Reset click state
    if was_clicked:
        state.update(**{f"{state_key}_clicked": False})

    props = {
        "label": label,
        "variant": variant,
        "disabled": disabled,
        "fullWidth": full_width,
        "icon": icon,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else {}
    if full_width:
        style_dict["width"] = "100%"

    component = ctx.create_component(
        "button",
        props=props,
        style=style_dict or None,
        events={"click": f"{state_key}:click"},
    )

    return was_clicked


def input(
    label: str = "",
    *,
    key: Optional[str] = None,
    value: str = "",
    placeholder: str = "",
    type: str = "text",
    disabled: bool = False,
    style: Optional[Style] = None,
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
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("input", props=props, style=style_dict)

    return current_value


def text_area(
    label: str = "",
    *,
    key: Optional[str] = None,
    value: str = "",
    placeholder: str = "",
    rows: int = 4,
    disabled: bool = False,
    style: Optional[Style] = None,
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
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("textarea", props=props, style=style_dict)

    return current_value


def slider(
    label: str = "",
    min_value: float = 0,
    max_value: float = 100,
    value: Optional[float] = None,
    *,
    key: Optional[str] = None,
    step: float = 1,
    disabled: bool = False,
    style: Optional[Style] = None,
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
    options: List[Union[str, Dict[str, str]]] = None,
    *,
    key: Optional[str] = None,
    default: Optional[str] = None,
    placeholder: str = "Select an option...",
    disabled: bool = False,
    style: Optional[Style] = None,
) -> Optional[str]:
    """
    Create a dropdown select.

    Args:
        label: Select label
        options: List of options (strings or dicts with 'value' and 'label')
        key: State key
        default: Default selected value
        placeholder: Placeholder text
        disabled: Whether disabled
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
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("select", props=props, style=style_dict)

    return current_value


def multiselect(
    label: str = "",
    options: List[Union[str, Dict[str, str]]] = None,
    *,
    key: Optional[str] = None,
    default: Optional[List[str]] = None,
    placeholder: str = "Select options...",
    disabled: bool = False,
    style: Optional[Style] = None,
) -> List[str]:
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
    key: Optional[str] = None,
    value: bool = False,
    disabled: bool = False,
    style: Optional[Style] = None,
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
    key: Optional[str] = None,
    value: bool = False,
    disabled: bool = False,
    style: Optional[Style] = None,
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
    options: List[str],
    *,
    key: Optional[str] = None,
    default: Optional[str] = None,
    horizontal: bool = False,
    disabled: bool = False,
    style: Optional[Style] = None,
) -> Optional[str]:
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
    key: Optional[str] = None,
    value: Optional[str] = None,
    min_date: Optional[str] = None,
    max_date: Optional[str] = None,
    disabled: bool = False,
    style: Optional[Style] = None,
) -> Optional[str]:
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
    key: Optional[str] = None,
    value: Optional[str] = None,
    disabled: bool = False,
    style: Optional[Style] = None,
) -> Optional[str]:
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
    key: Optional[str] = None,
    accept: Optional[List[str]] = None,
    multiple: bool = False,
    disabled: bool = False,
    style: Optional[Style] = None,
) -> Optional[Any]:
    """
    Create a file uploader.

    Args:
        label: Uploader label
        key: State key
        accept: Accepted file types (e.g., ['.pdf', '.docx'])
        multiple: Allow multiple files
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
        "disabled": disabled,
        "stateKey": state_key,
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("fileuploader", props=props, style=style_dict)

    return current_value


def color_picker(
    label: str = "",
    *,
    key: Optional[str] = None,
    value: str = "#6366f1",
    disabled: bool = False,
    style: Optional[Style] = None,
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
    columns: Optional[List[str]] = None,
    height: Optional[str] = None,
    style: Optional[Style] = None,
) -> None:
    """
    Display a dataframe or table data.

    Args:
        data: Data to display (list of dicts, pandas DataFrame, etc.)
        columns: Column names (inferred from data if not provided)
        height: Max height with scrolling
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
    }
    style_dict = style.to_dict() if style else None
    ctx.create_component("dataframe", props=props, style=style_dict)


def table(
    data: Any,
    *,
    columns: Optional[List[str]] = None,
    style: Optional[Style] = None,
) -> None:
    """Alias for dataframe."""
    dataframe(data, columns=columns, style=style)


def metric(
    label: str,
    value: Any,
    *,
    delta: Optional[float] = None,
    delta_label: str = "",
    style: Optional[Style] = None,
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
    label: Optional[str] = None,
    style: Optional[Style] = None,
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
    width: Optional[str] = None,
    height: Optional[str] = None,
    caption: Optional[str] = None,
    style: Optional[Style] = None,
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
    width: Optional[str] = None,
    height: Optional[str] = None,
    style: Optional[Style] = None,
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
    style: Optional[Style] = None,
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
    avatar: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


def chat_message(
    content: str,
    *,
    role: str = "assistant",
    avatar: Optional[str] = None,
    name: Optional[str] = None,
    timestamp: Optional[str] = None,
    is_streaming: bool = False,
    style: Optional[Style] = None,
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
    key: Optional[str] = None,
    disabled: bool = False,
    max_length: Optional[int] = None,
    style: Optional[Style] = None,
) -> Optional[str]:
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
    key: Optional[str] = None,
    style: Optional[Style] = None,
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
    messages: List[Dict[str, Any]],
    *,
    key: Optional[str] = None,
    height: str = "500px",
    show_input: bool = True,
    input_placeholder: str = "Type a message...",
    on_submit: Optional[Callable[[str], None]] = None,
    user_avatar: Optional[str] = None,
    assistant_avatar: Optional[str] = None,
    style: Optional[Style] = None,
) -> Optional[str]:
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
    style: Optional[Style] = None,
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
    href: Optional[str] = None,
    icon: Optional[str] = None,
    active: bool = False,
    key: Optional[str] = None,
    style: Optional[Style] = None,
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
    was_clicked = state.get(f"{state_key}_clicked", False)
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
    items: List[Dict[str, str]],
    *,
    separator: str = "/",
    style: Optional[Style] = None,
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
    key: Optional[str] = None,
    style: Optional[Style] = None,
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
    key: Optional[str] = None,
    icon: Optional[str] = None,
    style: Optional[Style] = None,
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
    items: List[str],
    *,
    allow_multiple: bool = False,
    key: Optional[str] = None,
    style: Optional[Style] = None,
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
    open_items = state.setdefault(state_key, [])

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
    key: Optional[str] = None,
    size: str = "md",
    close_on_overlay: bool = True,
    style: Optional[Style] = None,
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
    key: Optional[str] = None,
    style: Optional[Style] = None,
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
    style: Optional[Style] = None,
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
    key: Optional[str] = None,
    value: float = 0,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    step: float = 1,
    disabled: bool = False,
    style: Optional[Style] = None,
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
    key: Optional[str] = None,
    value: str = "",
    debounce: int = 300,
    style: Optional[Style] = None,
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
    key: Optional[str] = None,
    value: int = 0,
    max_value: int = 5,
    disabled: bool = False,
    style: Optional[Style] = None,
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
    key: Optional[str] = None,
    value: Optional[List[str]] = None,
    placeholder: str = "Add tag...",
    max_tags: Optional[int] = None,
    suggestions: Optional[List[str]] = None,
    style: Optional[Style] = None,
) -> List[str]:
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
    style: Optional[Style] = None,
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
    src: Optional[str] = None,
    *,
    name: Optional[str] = None,
    size: str = "md",
    style: Optional[Style] = None,
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
    avatars: List[Dict[str, str]],
    *,
    max_display: int = 4,
    size: str = "md",
    style: Optional[Style] = None,
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
    description: Optional[str] = None,
    icon: Optional[str] = None,
    trend: Optional[float] = None,
    trend_label: Optional[str] = None,
    style: Optional[Style] = None,
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
    description: Optional[str] = None,
    icon: Optional[str] = None,
    action_label: Optional[str] = None,
    key: Optional[str] = None,
    style: Optional[Style] = None,
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
    was_clicked = state.get(f"{state_key}_clicked", False)
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
    height: Optional[str] = None,
    style: Optional[Style] = None,
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
    items: List[Dict[str, Any]],
    *,
    style: Optional[Style] = None,
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
    items: List[str],
    *,
    current: int = 0,
    key: Optional[str] = None,
    clickable: bool = False,
    style: Optional[Style] = None,
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
    data: List[Dict[str, Any]],
    *,
    x: str,
    y: Union[str, List[str]],
    title: Optional[str] = None,
    height: str = "300px",
    colors: Optional[List[str]] = None,
    style: Optional[Style] = None,
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
    data: List[Dict[str, Any]],
    *,
    x: str,
    y: Union[str, List[str]],
    title: Optional[str] = None,
    height: str = "300px",
    colors: Optional[List[str]] = None,
    horizontal: bool = False,
    stacked: bool = False,
    style: Optional[Style] = None,
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
    data: List[Dict[str, Any]],
    *,
    x: str,
    y: Union[str, List[str]],
    title: Optional[str] = None,
    height: str = "300px",
    colors: Optional[List[str]] = None,
    stacked: bool = False,
    style: Optional[Style] = None,
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
    data: List[Dict[str, Any]],
    *,
    label: str,
    value: str,
    title: Optional[str] = None,
    height: str = "300px",
    colors: Optional[List[str]] = None,
    donut: bool = False,
    style: Optional[Style] = None,
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
    style: Optional[Style] = None,
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
    style: Optional[Style] = None,
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
    style: Optional[Style] = None,
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
    style: Optional[Style] = None,
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
