"""
Umara - A beautiful, modern Python framework for creating web UIs.

Build stunning web applications with pure Python. No web development
knowledge required.

Example:
    import umara as um

    um.set_theme('ocean')
    um.header('Welcome to Umara')

    name = um.input('Your name')
    if um.button('Submit'):
        um.success(f'Hello {name}!')
"""

from umara.core import (
    UmaraApp,
    get_app,
    run,
)
from umara.components import (
    # Typography
    text,
    header,
    subheader,
    markdown,
    code,
    # Feedback
    success,
    error,
    warning,
    info,
    # Layout
    container,
    columns,
    column,
    grid,
    card,
    tabs,
    tab,
    divider,
    spacer,
    # Widgets
    button,
    input,
    text_area,
    slider,
    select,
    multiselect,
    checkbox,
    toggle,
    radio,
    date_input,
    time_input,
    file_uploader,
    color_picker,
    # Data Display
    dataframe,
    table,
    metric,
    progress,
    spinner,
    # Media
    image,
    video,
    audio,
)
from umara.themes import (
    set_theme,
    get_theme,
    create_theme,
    Theme,
)
from umara.state import (
    state,
    session_state,
    cache,
)
from umara.style import style

__version__ = "0.1.0"
__all__ = [
    # Core
    "UmaraApp",
    "get_app",
    "run",
    # Typography
    "text",
    "header",
    "subheader",
    "markdown",
    "code",
    # Feedback
    "success",
    "error",
    "warning",
    "info",
    # Layout
    "container",
    "columns",
    "column",
    "grid",
    "card",
    "tabs",
    "tab",
    "divider",
    "spacer",
    # Widgets
    "button",
    "input",
    "text_area",
    "slider",
    "select",
    "multiselect",
    "checkbox",
    "toggle",
    "radio",
    "date_input",
    "time_input",
    "file_uploader",
    "color_picker",
    # Data Display
    "dataframe",
    "table",
    "metric",
    "progress",
    "spinner",
    # Media
    "image",
    "video",
    "audio",
    # Themes
    "set_theme",
    "get_theme",
    "create_theme",
    "Theme",
    # State
    "state",
    "session_state",
    "cache",
    # Styling
    "style",
]
