"""
UI Components for Umara.

All components are designed to be beautiful by default with
polished styling out of the box.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union
from contextlib import contextmanager

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
