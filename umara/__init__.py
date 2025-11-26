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

from umara.components import (
    ChatMessage,
    accordion,
    area_chart,
    audio,
    audio_input,
    avatar,
    avatar_group,
    # Display Components
    badge,
    bar_chart,
    breadcrumbs,
    # Widgets
    button,
    camera_input,
    caption,
    card,
    # Chat/Conversation
    chat,
    chat_container,
    chat_input,
    chat_message,
    checkbox,
    close_modal,
    code,
    color_picker,
    column,
    columns,
    # Layout
    container,
    # Utility Components
    copy_button,
    data_editor,
    # Data Display
    dataframe,
    date_input,
    dialog,
    divider,
    download_button,
    echo,
    empty_state,
    error,
    exception,
    # Container Components
    expander,
    feedback,
    file_uploader,
    # Forms
    form,
    form_submit_button,
    grid,
    header,
    html,
    iframe,
    # Media
    image,
    info,
    input,
    json_viewer,
    latex,
    # Charts
    line_chart,
    link_button,
    loading_skeleton,
    logo,
    map,
    markdown,
    metric,
    modal,
    multiselect,
    nav_link,
    # Additional Inputs
    number_input,
    open_modal,
    pagination,
    pie_chart,
    pills,
    popover,
    progress,
    radio,
    rating,
    # Execution Flow
    rerun,
    scatter_chart,
    search_input,
    segmented_control,
    select,
    select_slider,
    # Page Config
    set_page_config,
    # Navigation
    sidebar,
    slider,
    spacer,
    spinner,
    stat_card,
    status,
    steps,
    stop,
    subheader,
    # Feedback
    success,
    tab,
    table,
    tabs,
    tag_input,
    # Typography
    text,
    text_area,
    time_input,
    timeline,
    title,
    toast,
    toggle,
    tooltip,
    video,
    warning,
    # Smart Write (like st.write)
    write,
)
from umara.core import (
    UmaraApp,
    get_app,
    run,
)
from umara.state import (
    cache,
    session_state,
    state,
)
from umara.style import style
from umara.themes import (
    Theme,
    create_theme,
    get_theme,
    set_theme,
)

__version__ = "0.3.0"
__all__ = [
    # Core
    "UmaraApp",
    "get_app",
    "run",
    # Smart Write
    "write",
    # Typography
    "text",
    "title",
    "header",
    "subheader",
    "caption",
    "markdown",
    "code",
    "latex",
    "echo",
    # Feedback
    "success",
    "error",
    "warning",
    "info",
    "toast",
    "exception",
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
    "download_button",
    "link_button",
    "input",
    "text_area",
    "slider",
    "select_slider",
    "select",
    "multiselect",
    "checkbox",
    "toggle",
    "radio",
    "date_input",
    "time_input",
    "file_uploader",
    "color_picker",
    "pills",
    "feedback",
    "segmented_control",
    "camera_input",
    "audio_input",
    # Forms
    "form",
    "form_submit_button",
    # Data Display
    "dataframe",
    "data_editor",
    "table",
    "metric",
    "progress",
    "spinner",
    # Media
    "image",
    "video",
    "audio",
    "logo",
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
    "dialog",
    "open_modal",
    "close_modal",
    "popover",
    "tooltip",
    "status",
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
    "scatter_chart",
    "map",
    # Utility Components
    "copy_button",
    "json_viewer",
    "html",
    "iframe",
    # Execution Flow
    "rerun",
    "stop",
    # Page Config
    "set_page_config",
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
