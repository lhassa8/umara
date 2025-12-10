# Umara LLM Reference Guide

Concise API reference for LLM agents using Umara v0.5.1. All signatures verified against source code.

## Quick Start

```python
import umara as um

um.set_page_config(page_title="My App", layout="wide")
um.title("Hello World")
um.text("Welcome to Umara!")

if um.button("Click me"):
    um.success("Button clicked!")
```

---

## Typography Components

### text()
```python
um.text(content: str, *, color: str = None, size: str = None, style: Style = None) -> None
```
Display text. Use `color` for text color, `size` for font size (e.g., "1.5em").

### header()
```python
um.header(content: str, *, level: int = 1, style: Style = None) -> None
```
Display header. `level` is 1-6 (h1-h6).

### subheader()
```python
um.subheader(content: str, *, style: Style = None) -> None
```
Display h3 subheader.

### title()
```python
um.title(content: str, *, anchor: str = None, style: Style = None) -> None
```
Display largest heading (title level).

### caption()
```python
um.caption(content: str, *, unsafe_allow_html: bool = False, style: Style = None) -> None
```
Display small caption text.

### markdown()
```python
um.markdown(content: str, *, style: Style = None) -> None
```
Render markdown content.

### code()
```python
um.code(content: str, *, language: str = "python", line_numbers: bool = True, style: Style = None) -> None
```
Display syntax-highlighted code.

### latex()
```python
um.latex(content: str, *, style: Style = None) -> None
```
Display LaTeX math. Example: `um.latex(r"E = mc^2")`

---

## Feedback Components

### success() / error() / warning() / info()
```python
um.success(message: str, *, style: Style = None) -> None
um.error(message: str, *, style: Style = None) -> None
um.warning(message: str, *, style: Style = None) -> None
um.info(message: str, *, style: Style = None) -> None
```
Display colored alert messages.

### toast()
```python
um.toast(message: str, *, icon: str = None, duration: int = 4000) -> None
```
Show popup notification. `icon` is emoji or icon name, `duration` in ms.

### exception()
```python
um.exception(e: Exception) -> None
```
Display exception with traceback.

---

## Input Widgets

### button()
```python
um.button(label: str, *, key: str = None, variant: str = "primary", disabled: bool = False,
          loading: bool = False, full_width: bool = False, icon: str = None, style: Style = None) -> bool
```
**Returns**: `True` if clicked this render.
**Variants**: "primary", "secondary", "outline", "ghost", "danger"

### input()
```python
um.input(label: str = "", *, key: str = None, value: str = "", placeholder: str = "",
         type: str = "text", disabled: bool = False, label_position: str = "top",
         label_width: str = "120px", style: Style = None) -> str
```
**Returns**: Current input value.
**Types**: "text", "password", "email", "number"

### text_area()
```python
um.text_area(label: str = "", *, key: str = None, value: str = "", placeholder: str = "",
             rows: int = 4, disabled: bool = False, label_position: str = "top",
             label_width: str = "120px", style: Style = None) -> str
```
**Returns**: Current text area value.

### number_input()
```python
um.number_input(label: str = "", *, key: str = None, value: float = 0, min_value: float = None,
                max_value: float = None, step: float = 1, disabled: bool = False, style: Style = None) -> float
```
**Returns**: Current numeric value.

### slider()
```python
um.slider(label: str = "", min_value: float = 0, max_value: float = 100, value: float = None,
          *, key: str = None, step: float = 1, disabled: bool = False, style: Style = None) -> float
```
**Returns**: Current slider value.

### select()
```python
um.select(label: str = "", options: list[str | dict] = None, *, key: str = None, default: str = None,
          placeholder: str = "Select an option...", disabled: bool = False,
          label_position: str = "top", label_width: str = "120px", style: Style = None) -> str | None
```
**Returns**: Selected value or None.

### multiselect()
```python
um.multiselect(label: str = "", options: list = None, *, key: str = None, default: list = None,
               placeholder: str = "Select options...", disabled: bool = False, style: Style = None) -> list[str]
```
**Returns**: List of selected values.

### checkbox()
```python
um.checkbox(label: str, *, key: str = None, value: bool = False, disabled: bool = False, style: Style = None) -> bool
```
**Returns**: Current checked state.

### toggle()
```python
um.toggle(label: str, *, key: str = None, value: bool = False, disabled: bool = False, style: Style = None) -> bool
```
**Returns**: Current toggle state.

### radio()
```python
um.radio(label: str, options: list[str], *, key: str = None, default: str = None,
         horizontal: bool = False, disabled: bool = False, style: Style = None) -> str | None
```
**Returns**: Selected option or None.

### date_input()
```python
um.date_input(label: str = "", *, key: str = None, value: str = None, min_date: str = None,
              max_date: str = None, disabled: bool = False, style: Style = None) -> str | None
```
**Returns**: Date string "YYYY-MM-DD" or None.

### time_input()
```python
um.time_input(label: str = "", *, key: str = None, value: str = None, disabled: bool = False,
              style: Style = None) -> str | None
```
**Returns**: Time string "HH:MM" or None.

### file_uploader()
```python
um.file_uploader(label: str = "", *, key: str = None, accept: list[str] = None, multiple: bool = False,
                 max_file_size: int = None, disabled: bool = False, style: Style = None) -> Any | None
```
**Returns**: Uploaded file(s) or None.

### color_picker()
```python
um.color_picker(label: str = "", *, key: str = None, value: str = "#6366f1", disabled: bool = False,
                style: Style = None) -> str
```
**Returns**: Hex color string.

### rating()
```python
um.rating(label: str = "", *, key: str = None, value: int = 0, max_value: int = 5,
          disabled: bool = False, style: Style = None) -> int
```
**Returns**: Current rating (0 to max_value).

### search_input()
```python
um.search_input(placeholder: str = "Search...", *, key: str = None, value: str = "",
                debounce: int = 300, style: Style = None) -> str
```
**Returns**: Current search value.

### tag_input()
```python
um.tag_input(label: str = "", *, key: str = None, value: list[str] = None, placeholder: str = "Add tag...",
             max_tags: int = None, suggestions: list[str] = None, style: Style = None) -> list[str]
```
**Returns**: List of tags.

### pills()
```python
um.pills(label: str, options: list[str], *, selection_mode: str = "single", default: str | list = None,
         key: str = None, disabled: bool = False, style: Style = None) -> str | list[str] | None
```
**Returns**: Selected option(s).
**Modes**: "single" or "multi"

### select_slider()
```python
um.select_slider(label: str, options: list, *, value: Any = None, key: str = None,
                 disabled: bool = False, label_visibility: str = "visible", style: Style = None) -> Any
```
**Returns**: Selected option.

### segmented_control()
```python
um.segmented_control(label: str, options: list[str], *, default: str = None, key: str = None,
                     disabled: bool = False, style: Style = None) -> str | None
```
**Returns**: Selected option.

### feedback()
```python
um.feedback(sentiment_mapping: dict[int, str] = None, *, key: str = None, disabled: bool = False,
            style: Style = None) -> int | None
```
**Returns**: Selected score or None.
**Default mapping**: `{0: "Thumbs down", 1: "Thumbs up"}`

### camera_input() [Experimental]
```python
um.camera_input(label: str, *, key: str = None, disabled: bool = False,
                label_visibility: str = "visible", style: Style = None) -> bytes | None
```
**Returns**: Image bytes or None.

### audio_input() [Experimental]
```python
um.audio_input(label: str, *, key: str = None, disabled: bool = False, style: Style = None) -> bytes | None
```
**Returns**: Audio bytes or None.

---

## Layout Components

### container()
```python
with um.container(*, padding: str = None, margin: str = None, align: str = None,
                  justify: str = None, gap: str = None, style: Style = None):
    # child components
```
Context manager for grouping components.

### columns()
```python
with um.columns(count: int = 2, *, gap: str = "16px", vertical_align: str = None, style: Style = None):
    with um.column():
        # column 1 content
    with um.column():
        # column 2 content
```
Create multi-column layout.

### column()
```python
with um.column(*, align: str = None, justify: str = None, gap: str = None, style: Style = None):
    # column content
```
Single column within columns layout.

### grid()
```python
with um.grid(columns: int | str = 3, *, gap: str = "16px", row_gap: str = None,
             align: str = None, justify: str = None, style: Style = None):
    # grid items
```
CSS grid layout.

### card()
```python
with um.card(*, title: str = None, subtitle: str = None, padding: str = "24px",
             shadow: str = "md", align: str = None, justify: str = None, gap: str = None, style: Style = None):
    # card content
```
**Shadow sizes**: "sm", "md", "lg", "xl"

### sidebar()
```python
with um.sidebar(*, width: str = "280px", collapsed: bool = False, style: Style = None):
    # sidebar content
```
Navigation sidebar panel.

### divider()
```python
um.divider(*, style: Style = None) -> None
```
Horizontal divider line.

### spacer()
```python
um.spacer(height: str = "24px") -> None
```
Vertical space.

---

## Container Components

### tabs()
```python
with um.tabs(tab_names: list[str], *, default: int = 0, key: str = None, style: Style = None) as active_tab:
    with um.tab(0):
        # Tab 1 content
    with um.tab(1):
        # Tab 2 content
```
**Returns**: Active tab index (0-indexed).

### expander()
```python
with um.expander(title: str, *, expanded: bool = False, key: str = None, icon: str = None, style: Style = None):
    # expandable content
```
Collapsible section.

### accordion()
```python
with um.accordion(items: list[str], *, allow_multiple: bool = False, key: str = None, style: Style = None):
    # accordion content
```
Multiple collapsible sections.

### modal()
```python
with um.modal(title: str, *, is_open: bool = False, key: str = None, size: str = "md",
              close_on_overlay: bool = True, style: Style = None):
    # modal content
```
**Sizes**: "sm", "md", "lg", "xl", "full"
Use `um.open_modal(key)` and `um.close_modal(key)` to control.

### dialog()
```python
with um.dialog(title: str, *, width: str = "medium", style: Style = None):
    # dialog content
```
**Widths**: "small", "medium", "large"

### popover()
```python
with um.popover(trigger_label: str, *, position: str = "bottom", key: str = None, style: Style = None):
    # popover content
```
**Positions**: "top", "bottom", "left", "right"

### tooltip()
```python
um.tooltip(content: str, *, text: str, position: str = "top", style: Style = None) -> None
```
Display text with hover tooltip.

### status()
```python
with um.status(label: str, *, expanded: bool = True, state: str = "running", style: Style = None) as s:
    # status content
    s.update(label="Done!", state="complete")
```
**States**: "running", "complete", "error"

### spinner()
```python
with um.spinner(text: str = "Loading..."):
    # code to execute while showing spinner
```

---

## Data Display

### metric()
```python
um.metric(label: str, value: Any, *, delta: float = None, delta_label: str = "", style: Style = None) -> None
```
Display metric with optional delta change indicator.

### progress()
```python
um.progress(value: float, *, label: str = None, style: Style = None) -> None
```
Progress bar. `value` is 0-100.

### dataframe() / table()
```python
um.dataframe(data: Any, *, columns: list[str] = None, height: str = None,
             sortable: bool = False, style: Style = None) -> None
um.table(data: Any, *, columns: list[str] = None, style: Style = None) -> None
```
Display tabular data. Accepts list of dicts or pandas DataFrame.

### data_editor()
```python
um.data_editor(data: list[dict] | DataFrame, *, num_rows: str = "fixed", disabled: bool | list[str] = False,
               column_config: dict = None, hide_index: bool = True, key: str = None,
               height: str = None, style: Style = None) -> list[dict] | DataFrame
```
**Returns**: Edited data in same format as input.
**num_rows**: "fixed" or "dynamic"

### json_viewer()
```python
um.json_viewer(data: Any, *, expanded: bool = True, max_depth: int = 3, style: Style = None) -> None
```
Collapsible JSON tree view.

### stat_card()
```python
um.stat_card(title: str, value: str, *, description: str = None, icon: str = None,
             trend: float | str = None, trend_label: str = None,
             delta: str = None, delta_type: str = None, style: Style = None) -> None
```
Statistic card with icon and trend. `delta` is a Streamlit-compatible alias for `trend`. `delta_type`: 'positive', 'negative', 'neutral'.

### badge()
```python
um.badge(text: str, *, variant: str = "default", size: str = "md", style: Style = None) -> None
```
**Variants**: "default", "success", "warning", "error", "info"
**Sizes**: "sm", "md", "lg"

### avatar()
```python
um.avatar(src: str = None, *, name: str = None, size: str = "md", style: Style = None) -> None
```
**Sizes**: "sm", "md", "lg", "xl"
Use `name` for initials fallback when no image.

### avatar_group()
```python
um.avatar_group(avatars: list[dict], *, max_display: int = 4, size: str = "md", style: Style = None) -> None
```
Overlapping avatar display.

### empty_state()
```python
um.empty_state(title: str, *, description: str = None, icon: str = None,
               action_label: str = None, key: str = None, style: Style = None) -> bool
```
**Returns**: True if action button clicked.

### loading_skeleton()
```python
um.loading_skeleton(*, variant: str = "text", lines: int = 3, height: str = None, style: Style = None) -> None
```
**Variants**: "text", "card", "avatar", "image"

### timeline()
```python
um.timeline(items: list[dict], *, style: Style = None) -> None
```
Items should have: title, description, date, icon.

### copy_button()
```python
um.copy_button(text: str, *, label: str = "Copy", success_label: str = "Copied!", style: Style = None) -> None
```
Button that copies text to clipboard.

---

## Media Components

### image()
```python
um.image(src: str, *, alt: str = "", width: str = None, height: str = None,
         caption: str = None, style: Style = None) -> None
```

### video()
```python
um.video(src: str, *, autoplay: bool = False, controls: bool = True, loop: bool = False,
         muted: bool = False, width: str = None, height: str = None, style: Style = None) -> None
```

### audio()
```python
um.audio(src: str, *, autoplay: bool = False, controls: bool = True, loop: bool = False,
         style: Style = None) -> None
```

---

## Chart Components

### line_chart()
```python
um.line_chart(data: list[dict], *, x: str, y: str | list[str], title: str = None,
              height: str = "300px", colors: list[str] = None, style: Style = None) -> None
```

### bar_chart()
```python
um.bar_chart(data: list[dict], *, x: str, y: str | list[str], title: str = None,
             height: str = "300px", colors: list[str] = None, horizontal: bool = False,
             stacked: bool = False, style: Style = None) -> None
```

### area_chart()
```python
um.area_chart(data: list[dict], *, x: str, y: str | list[str], title: str = None,
              height: str = "300px", colors: list[str] = None, stacked: bool = False, style: Style = None) -> None
```

### pie_chart()
```python
um.pie_chart(data: list[dict], *, label: str, value: str, title: str = None,
             height: str = "300px", colors: list[str] = None, donut: bool = False, style: Style = None) -> None
```

### scatter_chart()
```python
um.scatter_chart(data: list[dict], *, x: str = None, y: str = None, color: str = None,
                 size: str = None, title: str = None, height: str = "300px", style: Style = None) -> None
```

### map()
```python
um.map(data: list[dict] = None, *, latitude: str = "lat", longitude: str = "lon",
       zoom: int = 10, height: str = "400px", style: Style = None) -> None
```

### plotly_chart()
```python
um.plotly_chart(figure: Any, *, use_container_width: bool = True, theme: str = None,
                key: str = None, style: Style = None) -> None
```
Render any Plotly figure (go.Figure or plotly.express).

---

## Navigation Components

### breadcrumbs()
```python
um.breadcrumbs(items: list[dict], *, separator: str = "/", style: Style = None) -> None
```
Items: `[{"label": "Home", "href": "/"}, {"label": "Current"}]`

### steps()
```python
um.steps(items: list[str], *, current: int = 0, key: str = None, clickable: bool = False,
         style: Style = None) -> int
```
**Returns**: Current step index.

### pagination()
```python
um.pagination(total_pages: int, *, current_page: int = 1, key: str = None, style: Style = None) -> int
```
**Returns**: Current page number (1-indexed).

### nav_link()
```python
um.nav_link(label: str, *, href: str = None, icon: str = None, active: bool = False,
            key: str = None, style: Style = None) -> bool
```
**Returns**: True if clicked.

---

## Chat Components

### chat_message()
```python
um.chat_message(content: str, *, role: str = "assistant", avatar: str = None, name: str = None,
                timestamp: str = None, is_streaming: bool = False, style: Style = None) -> None
```
**Roles**: "user", "assistant", "system"

### chat_input()
```python
um.chat_input(placeholder: str = "Type a message...", *, key: str = None, disabled: bool = False,
              max_length: int = None, style: Style = None) -> str | None
```
**Returns**: Submitted message or None.

### chat_container()
```python
with um.chat_container(*, height: str = "500px", key: str = None, style: Style = None):
    # chat messages
```
Scrollable container for messages.

### chat()
```python
um.chat(messages: list[dict], *, key: str = None, height: str = "500px", show_input: bool = True,
        input_placeholder: str = "Type a message...", user_avatar: str = None,
        assistant_avatar: str = None, style: Style = None) -> str | None
```
**Returns**: Submitted user message or None.
Messages format: `[{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello!"}]`

---

## Form Components

### form()
```python
with um.form(key: str, *, clear_on_submit: bool = False, border: bool = True, style: Style = None):
    name = um.input("Name")
    if um.form_submit_button("Submit"):
        um.success(f"Hello {name}")
```
Batches inputs together.

### form_submit_button()
```python
um.form_submit_button(label: str = "Submit", *, disabled: bool = False, variant: str = "primary",
                      style: Style = None) -> bool
```
**Returns**: True if form submitted.

---

## Button Variants

### download_button()
```python
um.download_button(label: str, data: str | bytes | Callable, *, file_name: str = "download.txt",
                   mime: str = None, key: str = None, disabled: bool = False, variant: str = "secondary",
                   on_click: Callable = None, style: Style = None) -> bool
```
**Returns**: True if clicked.

### link_button()
```python
um.link_button(label: str, url: str, *, disabled: bool = False, variant: str = "secondary",
               style: Style = None) -> None
```
Button that opens URL.

---

## Utility Functions

### write()
```python
um.write(*args, **kwargs) -> None
```
Smart output - handles strings, numbers, dicts, lists, DataFrames automatically.

### write_stream()
```python
um.write_stream(stream: Any, *, key: str = None, style: Style = None) -> str
```
**Returns**: Complete concatenated response.
Works with OpenAI/Anthropic streams.

### echo()
```python
with um.echo(code_location: str = "above"):
    # Code shown and executed
```

### html()
```python
um.html(content: str, *, style: Style = None) -> None
```
**Warning**: Use only with trusted content.

### iframe()
```python
um.iframe(src: str, *, height: str = "400px", width: str = "100%", title: str = "Embedded content",
          style: Style = None) -> None
```

### logo()
```python
um.logo(image: str, *, link: str = None, icon_image: str = None, style: Style = None) -> None
```
Display app logo in sidebar.

---

## Page Configuration

### set_page_config()
```python
um.set_page_config(page_title: str = None, page_icon: str = None, layout: str = "centered",
                   initial_sidebar_state: str = "auto", menu_items: dict = None) -> None
```
**Must be called first!**
**Layouts**: "centered", "wide"
**Sidebar states**: "auto", "expanded", "collapsed"

---

## Control Flow

### rerun()
```python
um.rerun() -> None
```
Rerun the app from top. Raises RerunException.

### stop()
```python
um.stop() -> None
```
Stop app execution at this point. Raises StopException.

### open_modal() / close_modal()
```python
um.open_modal(key: str) -> None
um.close_modal(key: str) -> None
```
Control modal visibility by key.

---

## Form Validation

Umara includes a built-in validation system with 17+ validators. Import from `umara.validation`.

### validate()
```python
from umara.validation import validate, required, email, min_length

errors = validate({
    "email": (email_input, [required(), email()]),
    "password": (password, [required(), min_length(8)]),
})
# Returns: dict[str, list[str]] - empty dict if valid
```

### validate_field()
```python
from umara.validation import validate_field, required, email

errors = validate_field(email_input, [required(), email()])
# Returns: list[str] - list of error messages
```

### is_valid()
```python
from umara.validation import is_valid, required, min_length

if is_valid(password, [required(), min_length(8)]):
    um.success("Password is valid!")
```

### Available Validators
```python
required(message="...")           # Not empty/None
min_length(n, message="...")      # Minimum string/list length
max_length(n, message="...")      # Maximum string/list length
email(message="...")              # Valid email format
url(message="...")                # Valid URL format
pattern(regex, message="...")     # Regex match
min_value(n, message="...")       # Minimum numeric value
max_value(n, message="...")       # Maximum numeric value
in_range(min, max, message="...")  # Numeric range
one_of(options, message="...")    # Value in list
matches(other, name, message="...") # Matches another value
numeric(message="...")            # Is numeric
integer(message="...")            # Is whole number
alpha(message="...")              # Letters only
alphanumeric(message="...")       # Letters and numbers only
no_whitespace(message="...")      # No spaces/tabs/newlines
custom(fn, message="...")         # Custom validation function
```

### FormValidator Class
```python
from umara.validation import FormValidator, required, email

validator = FormValidator()
validator.add("name", name_input, [required()])
validator.add("email", email_input, [required(), email()])

if um.form_submit_button("Submit"):
    if validator.is_valid():
        um.success("Form valid!")
    else:
        validator.show_errors()  # Displays um.error() for each
```

---

## AI Streaming Helpers

Advanced AI/LLM integration helpers in `umara.ai`.

### stream_with_metrics()
```python
from umara.ai import stream_with_metrics

response, metrics = stream_with_metrics(openai_stream)
print(f"Tokens: {metrics.tokens_generated}, Speed: {metrics.tokens_per_second:.0f} tok/s")
```

### write_stream_with_stats()
```python
from umara.ai import write_stream_with_stats

result = um.ai.write_stream_with_stats(stream, show_stats=True)
# Displays streaming content + "Generated ~150 tokens in 2.3s (65 tok/s)"
```

### chat_stream()
```python
from umara.ai import chat_stream

# Streams inside a chat message container
response = um.ai.chat_stream(stream, role="assistant", avatar="🤖")
```

### simulate_stream()
```python
from umara.ai import simulate_stream

# Test streaming without API calls
stream = um.ai.simulate_stream("Hello! How can I help?", chunk_size=10, delay=0.02)
um.write_stream(stream)
```

### typewriter()
```python
from umara.ai import typewriter

um.ai.typewriter("Hello! How can I help you today?", speed=0.03)
```

### show_thinking()
```python
from umara.ai import show_thinking

um.ai.show_thinking("Let me break this down:\n1. First...", collapsed=True)
```

### estimate_cost()
```python
from umara.ai import estimate_cost

cost = um.ai.estimate_cost(input_tokens=500, output_tokens=1000, model="gpt-4")
print(f"Estimated: ${cost:.4f}")
```

### Provider Adapters
```python
from umara.ai import create_openai_stream_adapter, create_anthropic_stream_adapter

# Convert provider streams to plain string iterators
um.write_stream(create_openai_stream_adapter(openai_stream))
um.write_stream(create_anthropic_stream_adapter(anthropic_stream))
```

### AIMessage
```python
from umara.ai import AIMessage

messages = [
    AIMessage.system("You are helpful"),
    AIMessage.user("Hello!"),
    AIMessage.assistant("Hi there!"),
]
# Convert: msg.to_openai() or msg.to_anthropic()
```

---

## Common Patterns

### Basic Chat App
```python
import umara as um

if "messages" not in um.state:
    um.state.messages = []

um.title("Chat")

for msg in um.state.messages:
    um.chat_message(msg["content"], role=msg["role"])

if prompt := um.chat_input():
    um.state.messages.append({"role": "user", "content": prompt})
    # Add AI response
    response = "Echo: " + prompt
    um.state.messages.append({"role": "assistant", "content": response})
    um.rerun()
```

### Dashboard Layout
```python
import umara as um

um.set_page_config(layout="wide")

with um.sidebar():
    um.title("Dashboard")
    page = um.radio("Page", ["Overview", "Analytics", "Settings"])

if page == "Overview":
    with um.columns(3):
        with um.column():
            um.metric("Users", "1,234", delta=12)
        with um.column():
            um.metric("Revenue", "$5,678", delta=-3)
        with um.column():
            um.metric("Growth", "23%", delta=5)
```

### Form Handling
```python
import umara as um

with um.form("user_form"):
    name = um.input("Name")
    email = um.input("Email", type="email")
    agreed = um.checkbox("I agree to terms")

    if um.form_submit_button("Register"):
        if name and email and agreed:
            um.success(f"Welcome, {name}!")
        else:
            um.error("Please fill all fields")
```

---

## State Management

Access session state via `um.state`:
```python
# Set value
um.state.counter = 0

# Get value
count = um.state.counter

# Check existence
if "key" not in um.state:
    um.state.key = "default"
```

---

## Common Errors to Avoid

1. **Don't use `type` parameter for toast()** - Use `icon` instead:
   ```python
   um.toast("Message", icon="success")  # Correct
   um.toast("Message", type="success")  # WRONG
   ```

2. **Modal must have unique key**:
   ```python
   with um.modal("Title", key="my_modal", is_open=show):
       # content
   ```

3. **set_page_config must be first**:
   ```python
   um.set_page_config(page_title="App")  # Must be first!
   um.title("Hello")
   ```

4. **Form widgets need form_submit_button**:
   ```python
   with um.form("my_form"):
       um.input("Name")
       um.form_submit_button("Submit")  # Required inside form
   ```

---

*Umara v0.5.1 - 79 components + Form Validation + AI Streaming Helpers*
