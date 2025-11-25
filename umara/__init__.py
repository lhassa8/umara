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
    # Chat/Conversation
    chat,
    chat_message,
    chat_input,
    chat_container,
    ChatMessage,
    # Navigation
    sidebar,
    nav_link,
    breadcrumbs,
    pagination,
    # Container Components
    expander,
    accordion,
    modal,
    open_modal,
    close_modal,
    popover,
    tooltip,
    # Additional Inputs
    number_input,
    search_input,
    rating,
    tag_input,
    # Display Components
    badge,
    avatar,
    avatar_group,
    stat_card,
    empty_state,
    loading_skeleton,
    timeline,
    steps,
    # Charts
    line_chart,
    bar_chart,
    area_chart,
    pie_chart,
    # Utility Components
    copy_button,
    json_viewer,
    html,
    iframe,
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

__version__ = "0.2.0"
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
    # Chat/Conversation
    "chat",
    "chat_message",
    "chat_input",
    "chat_container",
    "ChatMessage",
    # Navigation
    "sidebar",
    "nav_link",
    "breadcrumbs",
    "pagination",
    # Container Components
    "expander",
    "accordion",
    "modal",
    "open_modal",
    "close_modal",
    "popover",
    "tooltip",
    # Additional Inputs
    "number_input",
    "search_input",
    "rating",
    "tag_input",
    # Display Components
    "badge",
    "avatar",
    "avatar_group",
    "stat_card",
    "empty_state",
    "loading_skeleton",
    "timeline",
    "steps",
    # Charts
    "line_chart",
    "bar_chart",
    "area_chart",
    "pie_chart",
    # Utility Components
    "copy_button",
    "json_viewer",
    "html",
    "iframe",
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
