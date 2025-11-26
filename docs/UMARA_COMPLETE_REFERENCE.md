# Umara Complete API Reference

> **A beautiful, modern Python framework for creating web UIs without HTML, CSS, or JavaScript.**

Version: 0.4.5

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Concepts](#core-concepts)
3. [Typography Components](#typography-components)
4. [Feedback Components](#feedback-components)
5. [Input Widgets](#input-widgets)
6. [Layout Components](#layout-components)
7. [Data Display](#data-display)
8. [Charts & Visualization](#charts--visualization)
9. [Media Components](#media-components)
10. [Navigation Components](#navigation-components)
11. [Chat Components](#chat-components)
12. [State Management](#state-management)
13. [Caching](#caching)
14. [Fragments (Partial Reruns)](#fragments-partial-reruns)
15. [Connections (Database & API)](#connections-database--api)
16. [Theming](#theming)
17. [Styling](#styling)
18. [Page Configuration](#page-configuration)
19. [CLI Commands](#cli-commands)
20. [Accessibility](#accessibility)
21. [Complete Examples](#complete-examples)

---

## Quick Start

### Installation

```bash
pip install umara
```

### Your First App

Create `app.py`:

```python
import umara as um

um.set_page_config(page_title="My First App", layout="wide")
um.set_theme("ocean")

um.title("Welcome to Umara!")
um.text("Build beautiful web apps with pure Python.")

name = um.input("What's your name?", placeholder="Enter your name")

if um.button("Say Hello"):
    um.success(f"Hello, {name}! Welcome to Umara!")
```

### Run Your App

```bash
umara run app.py
```

Open **http://localhost:8501** in your browser. Hot reload is enabled by default.

---

## Core Concepts

### How Umara Works

1. **Declarative UI**: Write Python code that describes your UI
2. **Reactive State**: When state changes, the UI automatically updates
3. **Component-Based**: Build UIs from reusable components
4. **WebSocket-Powered**: Real-time updates without page refreshes

### Import Convention

```python
import umara as um
```

### Basic Pattern

```python
import umara as um

# Configure page
um.set_page_config(page_title="My App")

# Set theme
um.set_theme("ocean")

# Display content
um.header("My App")
um.text("Welcome!")

# Get user input (returns current value)
name = um.input("Name", key="user_name")

# Handle interactions
if um.button("Submit"):
    um.success(f"Hello {name}!")
```

### Keys

**Keys are required for standalone inputs** (outside forms) to persist values across reruns:

```python
# WITHOUT key - value resets on every rerun (NOT recommended)
name = um.input("Name")  # Will lose value when app reruns!

# WITH key - value persists across reruns (RECOMMENDED)
name = um.input("Name", key="user_name")
email = um.input("Email", key="user_email")
```

**Why keys matter:**
- Without a key, input values reset to defaults on every script rerun
- Keys create a stable identity for the widget across reruns
- The widget's value is stored in session state using the key

**When to use keys vs forms:**

| Use Case | Solution |
|----------|----------|
| Input + button action | `um.form()` (recommended) |
| Real-time search/filtering | Standalone input with `key` |
| Toggle/checkbox immediate effect | Standalone with `key` |
| Multi-field data entry | `um.form()` with inputs |

**Important:** Standalone inputs have a 50ms debounce. If a user clicks a button immediately after typing, the input value may not be synced yet. For reliable input + button patterns, always use `um.form()`.

See [Forms](#form) for batched input handling.

---

## Typography Components

### text()

Display text content.

```python
um.text(
    content: str,
    *,
    style: Style | None = None,
    color: str | None = None,
    size: str | None = None
) -> None
```

**Parameters:**
- `content`: The text to display
- `style`: Custom style object
- `color`: Text color (CSS color value)
- `size`: Font size (e.g., "16px", "1.2rem")

**Examples:**

```python
um.text("Hello, world!")
um.text("Colored text", color="#6366f1")
um.text("Large text", size="24px")
um.text("Styled text", color="red", size="18px")
```

### title()

Display a page title (large h1).

```python
um.title(content: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.title("Welcome to My App")
```

### header()

Display a section header (h2).

```python
um.header(content: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.header("Section Title")
```

### subheader()

Display a subsection header (h3).

```python
um.subheader(content: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.subheader("Subsection")
```

### caption()

Display small caption text.

```python
um.caption(content: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.caption("Figure 1: Sample data visualization")
```

### markdown()

Display markdown content with full markdown support.

```python
um.markdown(content: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.markdown("""
### Features
- **Bold** and *italic* text
- `inline code`
- [Links](https://example.com)

> Blockquotes work too!
""")
```

### code()

Display code with syntax highlighting.

```python
um.code(
    content: str,
    *,
    language: str = "python",
    style: Style | None = None
) -> None
```

**Parameters:**
- `content`: The code to display
- `language`: Programming language for syntax highlighting

**Example:**

```python
um.code("""
def hello(name):
    return f"Hello, {name}!"

print(hello("World"))
""", language="python")
```

### latex()

Display LaTeX mathematical expressions.

```python
um.latex(content: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.latex(r"E = mc^2")
um.latex(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")
```

### divider()

Display a horizontal divider line.

```python
um.divider(*, style: Style | None = None) -> None
```

**Example:**

```python
um.text("Section 1")
um.divider()
um.text("Section 2")
```

### spacer()

Add vertical space.

```python
um.spacer(height: str = "24px") -> None
```

**Parameters:**
- `height`: Space height (CSS value)

**Example:**

```python
um.text("Above")
um.spacer("48px")
um.text("Below (with 48px gap)")
```

---

## Feedback Components

### success()

Display a success message (green).

```python
um.success(message: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.success("Operation completed successfully!")
```

### error()

Display an error message (red).

```python
um.error(message: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.error("Something went wrong. Please try again.")
```

### warning()

Display a warning message (amber/yellow).

```python
um.warning(message: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.warning("This action cannot be undone.")
```

### info()

Display an info message (blue).

```python
um.info(message: str, *, style: Style | None = None) -> None
```

**Example:**

```python
um.info("Tip: You can use keyboard shortcuts!")
```

### toast()

Display a temporary toast notification.

```python
um.toast(
    message: str,
    *,
    type: str = "info",  # "info", "success", "warning", "error"
    duration: int = 3000  # milliseconds
) -> None
```

**Parameters:**
- `message`: The notification text
- `type`: Toast style variant
- `duration`: How long to show (milliseconds)

**Example:**

```python
if um.button("Save"):
    # ... save logic ...
    um.toast("Saved successfully!", type="success")
```

### exception()

Display an exception with formatted traceback.

```python
um.exception(e: Exception) -> None
```

**Example:**

```python
try:
    result = risky_operation()
except Exception as e:
    um.exception(e)
```

### spinner()

Display a loading spinner (context manager).

```python
um.spinner(text: str = "Loading...") -> ContextManager
```

**Example:**

```python
with um.spinner("Processing..."):
    import time
    time.sleep(2)
```

---

## Input Widgets

### button()

Create a clickable button.

```python
um.button(
    label: str,
    *,
    key: str | None = None,
    variant: str = "primary",  # "primary", "secondary", "outline", "ghost", "danger"
    disabled: bool = False,
    loading: bool = False,
    icon: str | None = None,
    style: Style | None = None
) -> bool  # Returns True when clicked
```

**Parameters:**
- `label`: Button text
- `key`: Unique identifier
- `variant`: Visual style ("primary", "secondary", "outline", "ghost", "danger")
- `disabled`: Whether button is disabled
- `loading`: Show loading spinner
- `icon`: Icon name

**Examples:**

```python
# Basic button
if um.button("Click Me"):
    um.success("Button clicked!")

# Different variants
um.button("Primary", variant="primary")
um.button("Secondary", variant="secondary")
um.button("Outline", variant="outline")
um.button("Ghost", variant="ghost")
um.button("Delete", variant="danger")

# Loading state
um.button("Processing...", loading=True)

# Disabled button
um.button("Disabled", disabled=True)
```

### input()

Create a text input field.

```python
um.input(
    label: str = "",
    *,
    key: str | None = None,
    value: str = "",
    placeholder: str = "",
    type: str = "text",  # "text", "password", "email", "number"
    disabled: bool = False,
    label_position: str = "top",  # "top", "left"
    style: Style | None = None
) -> str  # Returns current value
```

**Parameters:**
- `label`: Input label text
- `key`: Unique identifier
- `value`: Default value
- `placeholder`: Placeholder text
- `type`: Input type
- `disabled`: Whether input is disabled
- `label_position`: Label placement ("top" or "left")

**Examples:**

```python
# Basic input
name = um.input("Name", placeholder="Enter your name")

# Password input
password = um.input("Password", type="password")

# Email input
email = um.input("Email", type="email", placeholder="you@example.com")

# Horizontal label
city = um.input("City", value="New York", label_position="left")

# Disabled
um.input("Read Only", value="Cannot edit", disabled=True)
```

### text_area()

Create a multi-line text input.

```python
um.text_area(
    label: str = "",
    *,
    key: str | None = None,
    value: str = "",
    placeholder: str = "",
    rows: int = 4,
    disabled: bool = False,
    style: Style | None = None
) -> str
```

**Parameters:**
- `label`: Label text
- `key`: Unique identifier
- `value`: Default value
- `placeholder`: Placeholder text
- `rows`: Number of visible rows
- `disabled`: Whether disabled

**Example:**

```python
bio = um.text_area(
    "Bio",
    placeholder="Tell us about yourself...",
    rows=5,
    key="user_bio"
)
```

### number_input()

Create a numeric input.

```python
um.number_input(
    label: str = "",
    *,
    key: str | None = None,
    value: float = 0,
    min_value: float | None = None,
    max_value: float | None = None,
    step: float = 1,
    disabled: bool = False,
    style: Style | None = None
) -> float
```

**Parameters:**
- `label`: Label text
- `key`: Unique identifier
- `value`: Default value
- `min_value`: Minimum allowed value
- `max_value`: Maximum allowed value
- `step`: Increment step

**Examples:**

```python
# Basic
age = um.number_input("Age", min_value=0, max_value=120, value=25)

# With step
price = um.number_input("Price", min_value=0, step=0.01, value=9.99)

# Integer only
quantity = um.number_input("Quantity", min_value=1, max_value=100, step=1)
```

### slider()

Create a range slider.

```python
um.slider(
    label: str = "",
    min_value: float = 0,
    max_value: float = 100,
    value: float | None = None,
    *,
    key: str | None = None,
    step: float = 1,
    disabled: bool = False,
    style: Style | None = None
) -> float
```

**Parameters:**
- `label`: Label text
- `min_value`: Minimum value
- `max_value`: Maximum value
- `value`: Default value (defaults to min_value)
- `key`: Unique identifier
- `step`: Increment step

**Examples:**

```python
# Basic slider
volume = um.slider("Volume", 0, 100, 50)

# Float slider
temperature = um.slider("Temperature", 0.0, 1.0, 0.5, step=0.1)

# Custom range
year = um.slider("Year", 1900, 2024, 2000, step=1)
```

### select()

Create a dropdown select.

```python
um.select(
    label: str = "",
    options: list[str] | list[dict] | None = None,
    *,
    key: str | None = None,
    default: str | None = None,
    placeholder: str = "Select an option...",
    disabled: bool = False,
    style: Style | None = None
) -> str | None
```

**Parameters:**
- `label`: Label text
- `options`: List of options (strings or dicts with "value" and "label" keys)
- `key`: Unique identifier
- `default`: Default selected value
- `placeholder`: Placeholder text

**Examples:**

```python
# Basic select
color = um.select("Favorite Color", ["Red", "Green", "Blue"])

# With default
size = um.select(
    "Size",
    options=["Small", "Medium", "Large"],
    default="Medium"
)

# With value/label objects
framework = um.select(
    "Framework",
    options=[
        {"value": "umara", "label": "Umara (Best!)"},
        {"value": "streamlit", "label": "Streamlit"},
        {"value": "gradio", "label": "Gradio"},
    ],
    default="umara"
)
```

### multiselect()

Create a multi-select dropdown.

```python
um.multiselect(
    label: str = "",
    options: list[str] | None = None,
    *,
    key: str | None = None,
    default: list[str] | None = None,
    placeholder: str = "Select options...",
    disabled: bool = False,
    style: Style | None = None
) -> list[str]
```

**Example:**

```python
skills = um.multiselect(
    "Skills",
    options=["Python", "JavaScript", "Rust", "Go", "TypeScript"],
    default=["Python"]
)
um.text(f"Selected: {', '.join(skills)}")
```

### checkbox()

Create a checkbox.

```python
um.checkbox(
    label: str,
    *,
    key: str | None = None,
    value: bool = False,
    disabled: bool = False,
    style: Style | None = None
) -> bool
```

**Examples:**

```python
# Basic checkbox
agreed = um.checkbox("I agree to the terms")

if agreed:
    um.success("Thank you for agreeing!")

# Default checked
newsletter = um.checkbox("Subscribe to newsletter", value=True)
```

### toggle()

Create a toggle switch.

```python
um.toggle(
    label: str,
    *,
    key: str | None = None,
    value: bool = False,
    disabled: bool = False,
    style: Style | None = None
) -> bool
```

**Example:**

```python
dark_mode = um.toggle("Dark Mode", key="dark_mode_toggle")

if dark_mode:
    um.set_theme("dark")
else:
    um.set_theme("light")
```

### radio()

Create radio button group.

```python
um.radio(
    label: str,
    options: list[str],
    *,
    key: str | None = None,
    default: str | None = None,
    horizontal: bool = False,
    disabled: bool = False,
    style: Style | None = None
) -> str | None
```

**Parameters:**
- `label`: Group label
- `options`: List of option strings
- `horizontal`: Display horizontally instead of vertically

**Examples:**

```python
# Vertical radio (default)
size = um.radio("Size", ["Small", "Medium", "Large"], default="Medium")

# Horizontal radio
priority = um.radio(
    "Priority",
    ["Low", "Medium", "High"],
    horizontal=True,
    default="Medium"
)
```

### date_input()

Create a date picker.

```python
um.date_input(
    label: str = "",
    *,
    key: str | None = None,
    value: str | None = None,  # "YYYY-MM-DD"
    min_date: str | None = None,
    max_date: str | None = None,
    disabled: bool = False,
    style: Style | None = None
) -> str | None  # Returns "YYYY-MM-DD"
```

**Example:**

```python
birthday = um.date_input(
    "Birthday",
    min_date="1900-01-01",
    max_date="2024-12-31"
)

if birthday:
    um.text(f"You selected: {birthday}")
```

### time_input()

Create a time picker.

```python
um.time_input(
    label: str = "",
    *,
    key: str | None = None,
    value: str | None = None,  # "HH:MM"
    disabled: bool = False,
    style: Style | None = None
) -> str | None  # Returns "HH:MM"
```

**Example:**

```python
meeting_time = um.time_input("Meeting Time", value="09:00")
```

### color_picker()

Create a color picker.

```python
um.color_picker(
    label: str = "",
    *,
    key: str | None = None,
    value: str = "#6366f1",
    disabled: bool = False,
    style: Style | None = None
) -> str  # Returns hex color
```

**Example:**

```python
bg_color = um.color_picker("Background Color", value="#ffffff")
um.html(f'<div style="background: {bg_color}; padding: 20px;">Preview</div>')
```

### rating()

Create a star rating input.

```python
um.rating(
    label: str = "",
    *,
    key: str | None = None,
    value: int = 0,
    max_value: int = 5,
    disabled: bool = False,
    style: Style | None = None
) -> int
```

**Example:**

```python
rating = um.rating("Rate this product", value=3, max_value=5)
um.text(f"You rated: {rating} stars")
```

### file_uploader()

Create a file upload widget.

```python
um.file_uploader(
    label: str = "",
    *,
    key: str | None = None,
    accept: list[str] | None = None,  # e.g., [".csv", ".xlsx"] or ["image/*"]
    multiple: bool = False,
    max_file_size: int | None = None,  # Maximum file size in bytes
    disabled: bool = False,
    style: Style | None = None
) -> dict | list[dict] | None
```

**Parameters:**
- `label`: Upload label
- `key`: Unique identifier
- `accept`: List of accepted file extensions or MIME types
- `multiple`: Allow multiple file selection
- `max_file_size`: Maximum file size in bytes (new in v0.4.4)
- `disabled`: Whether disabled

**Returns:** File object with keys: `name`, `size`, `type`, `content` (base64)

**Examples:**

```python
# Single file
uploaded = um.file_uploader("Upload CSV", accept=[".csv"])

if uploaded:
    um.success(f"Uploaded: {uploaded['name']} ({uploaded['size']} bytes)")

# Multiple files
files = um.file_uploader("Upload Images", accept=["image/*"], multiple=True)

if files:
    um.info(f"Uploaded {len(files)} file(s)")

# With size limit (5MB)
doc = um.file_uploader(
    "Upload Document",
    accept=[".pdf", ".docx"],
    max_file_size=5 * 1024 * 1024  # 5MB in bytes
)
```

### download_button()

Create a download button.

```python
um.download_button(
    label: str,
    data: str | bytes | Callable[[], str | bytes],
    *,
    file_name: str = "download.txt",
    mime: str | None = None,
    key: str | None = None,
    disabled: bool = False,
    on_click: Callable[[], None] | None = None,
    style: Style | None = None
) -> bool
```

**Parameters:**
- `label`: Button text
- `data`: File content (string, bytes, or callable that returns content)
- `file_name`: Downloaded file name
- `mime`: MIME type (auto-detected from file_name if not provided)
- `on_click`: Callback function

**Examples:**

```python
# Static text
um.download_button(
    "Download Text",
    "Hello, World!",
    file_name="hello.txt"
)

# Binary data
um.download_button(
    "Download Image",
    image_bytes,
    file_name="image.png"
)

# Dynamic generation (callable)
def generate_csv():
    return df.to_csv(index=False)

um.download_button(
    "Export CSV",
    generate_csv,
    file_name="data.csv"
)
```

---

## Layout Components

### container()

Create a container for grouping elements.

```python
with um.container(*, style: Style | None = None):
    # Children go here
```

**Example:**

```python
with um.container():
    um.header("Grouped Content")
    um.text("This content is grouped together")
```

### columns()

Create a multi-column layout.

```python
with um.columns(
    count: int = 2,
    *,
    gap: str = "16px",
    style: Style | None = None
):
    with um.column():
        # Column content
```

**Parameters:**
- `count`: Number of columns
- `gap`: Gap between columns (CSS value)

**Examples:**

```python
# Two equal columns
with um.columns(2):
    with um.column():
        um.text("Left column")
    with um.column():
        um.text("Right column")

# Three columns with custom gap
with um.columns(3, gap="24px"):
    with um.column():
        um.metric("Users", "1,234")
    with um.column():
        um.metric("Revenue", "$5,678")
    with um.column():
        um.metric("Orders", "890")
```

### grid()

Create a CSS grid layout.

```python
with um.grid(
    columns: int | str = 3,
    *,
    gap: str = "16px",
    row_gap: str | None = None,
    style: Style | None = None
):
    # Grid items go here
```

**Parameters:**
- `columns`: Number of columns or CSS grid-template-columns value
- `gap`: Gap between items
- `row_gap`: Row gap (uses `gap` if not specified)

**Example:**

```python
with um.grid(columns=4, gap="16px"):
    for i in range(8):
        with um.card():
            um.text(f"Item {i + 1}")
```

### card()

Create a styled card container.

```python
with um.card(
    *,
    title: str | None = None,
    subtitle: str | None = None,
    padding: str = "24px",
    shadow: str = "md",  # "sm", "md", "lg", "xl"
    style: Style | None = None
):
    # Card content goes here
```

**Parameters:**
- `title`: Card title
- `subtitle`: Card subtitle
- `padding`: Internal padding
- `shadow`: Shadow size

**Examples:**

```python
# Basic card
with um.card():
    um.text("Card content")

# Card with title
with um.card(title="User Profile", subtitle="Account settings"):
    um.text("Name: John Doe")
    um.text("Email: john@example.com")

# Styled card
with um.card(shadow="lg", padding="32px"):
    um.header("Premium Feature")
    um.text("Exclusive content here")
```

### tabs()

Create a tabbed interface.

```python
with um.tabs(
    tab_names: list[str],
    *,
    default: int = 0,
    key: str | None = None,
    style: Style | None = None
) as t:
    with t.tab(index):
        # Tab content
```

**Example:**

```python
with um.tabs(["Overview", "Data", "Settings"]) as t:
    with t.tab(0):
        um.header("Overview")
        um.text("Welcome to the dashboard")

    with t.tab(1):
        um.header("Data")
        um.dataframe(df)

    with t.tab(2):
        um.header("Settings")
        um.toggle("Enable notifications")
```

### expander()

Create a collapsible section.

```python
with um.expander(
    title: str,
    *,
    expanded: bool = False,
    key: str | None = None,
    style: Style | None = None
):
    # Expandable content
```

**Example:**

```python
with um.expander("Click to see more", expanded=False):
    um.text("Hidden content revealed!")
    um.code("print('Hello!')")
```

### sidebar()

Create a sidebar layout.

```python
with um.sidebar(
    *,
    width: str = "240px",
    style: Style | None = None
):
    # Sidebar content
```

**Example:**

```python
with um.sidebar():
    um.header("Navigation")
    um.nav_link("Home", href="/")
    um.nav_link("About", href="/about")
    um.nav_link("Contact", href="/contact")

# Main content (outside sidebar)
um.title("Main Content Area")
```

### modal()

Create a modal dialog.

```python
with um.modal(
    title: str,
    *,
    key: str,  # Required for open/close
    size: str = "md",  # "sm", "md", "lg"
    style: Style | None = None
):
    # Modal content
```

**Example:**

```python
if um.button("Open Modal"):
    um.open_modal("my_modal")

with um.modal("Confirm Action", key="my_modal"):
    um.text("Are you sure you want to proceed?")

    with um.columns(2):
        with um.column():
            if um.button("Cancel", variant="outline"):
                um.close_modal("my_modal")
        with um.column():
            if um.button("Confirm", variant="danger"):
                # Do action
                um.close_modal("my_modal")
```

### form()

Create a form container with batched submission.

```python
with um.form(
    key: str,
    *,
    border: bool = False,
    style: Style | None = None
):
    # Form fields
    if um.form_submit_button("Submit"):
        # Handle submission
```

**Example:**

```python
with um.form("contact_form", border=True):
    name = um.input("Name", key="form_name")
    email = um.input("Email", type="email", key="form_email")
    message = um.text_area("Message", key="form_message")

    if um.form_submit_button("Send Message"):
        if name and email and message:
            send_email(name, email, message)
            um.success("Message sent!")
        else:
            um.error("Please fill all fields")
```

---

## Data Display

### metric()

Display a metric with optional delta indicator.

```python
um.metric(
    label: str,
    value: str | int | float,
    *,
    delta: float | None = None,
    delta_label: str | None = None,
    delta_color: str = "auto",  # "auto", "green", "red"
    style: Style | None = None
) -> None
```

**Parameters:**
- `label`: Metric label
- `value`: Metric value
- `delta`: Change indicator (positive/negative number)
- `delta_label`: Additional context for delta
- `delta_color`: Color for delta ("auto" uses green for positive, red for negative)

**Examples:**

```python
# Basic metric
um.metric("Total Users", "12,543")

# With positive delta
um.metric("Revenue", "$48.2K", delta=12.5, delta_label="vs last month")

# With negative delta
um.metric("Churn Rate", "2.4%", delta=-0.5)

# Custom delta color
um.metric("Errors", "23", delta=5, delta_color="red")
```

### progress()

Display a progress bar.

```python
um.progress(
    value: float,
    *,
    label: str | None = None,
    max_value: float = 100,
    style: Style | None = None
) -> None
```

**Parameters:**
- `value`: Current progress value
- `label`: Progress label
- `max_value`: Maximum value (default 100)

**Examples:**

```python
um.progress(75, label="Project Progress")
um.progress(45, label="Upload Progress")

# Custom max
um.progress(150, label="Downloads", max_value=200)
```

### dataframe()

Display tabular data with optional sorting.

```python
um.dataframe(
    data: list[dict] | DataFrame,
    *,
    columns: list[str] | None = None,
    height: str | None = None,
    sortable: bool = False,  # Enable column sorting (new in v0.4.4)
    style: Style | None = None
) -> None
```

**Parameters:**
- `data`: Data as list of dicts or pandas DataFrame
- `columns`: Column names to display (default: all)
- `height`: Fixed height with scroll
- `sortable`: Enable click-to-sort on column headers (new in v0.4.4)

**Examples:**

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Carol"],
    "Age": [25, 30, 35],
    "City": ["NYC", "LA", "Chicago"]
})

# Basic table
um.dataframe(df)

# Sortable table (click headers to sort)
um.dataframe(df, sortable=True)

# With list of dicts
data = [
    {"Name": "Alice", "Score": 95},
    {"Name": "Bob", "Score": 87},
]
um.dataframe(data, sortable=True)
```

### table()

Display a simple HTML table (non-interactive).

```python
um.table(
    data: list[dict] | DataFrame,
    *,
    style: Style | None = None
) -> None
```

### json_viewer()

Display JSON in a formatted, syntax-highlighted view.

```python
um.json_viewer(
    data: dict | list,
    *,
    expanded: bool = False,
    style: Style | None = None
) -> None
```

**Example:**

```python
data = {
    "name": "Umara",
    "version": "0.4.4",
    "features": ["themes", "components", "state"]
}

um.json_viewer(data, expanded=True)
```

### stat_card()

Display a statistics card with trend indicator.

```python
um.stat_card(
    title: str,
    value: str,
    *,
    trend: float | None = None,
    icon: str | None = None,
    style: Style | None = None
) -> None
```

**Example:**

```python
um.stat_card("Total Sales", "$12,450", trend=15.2, icon="TrendingUp")
```

### badge()

Display a small badge/tag.

```python
um.badge(
    text: str,
    *,
    variant: str = "default",  # "default", "primary", "success", "warning", "error", "info"
    style: Style | None = None
) -> None
```

**Example:**

```python
um.badge("New", variant="success")
um.badge("Beta", variant="warning")
um.badge("Deprecated", variant="error")
```

### avatar()

Display a user avatar.

```python
um.avatar(
    *,
    name: str = "",  # Generates initials
    src: str | None = None,  # Image URL
    size: str = "md",  # "sm", "md", "lg", "xl"
    style: Style | None = None
) -> None
```

**Examples:**

```python
# With initials
um.avatar(name="John Doe")  # Shows "JD"

# With image
um.avatar(src="https://example.com/avatar.jpg", size="lg")
```

### timeline()

Display a timeline of events.

```python
um.timeline(
    items: list[dict],  # {"title": str, "description": str, "date": str}
    *,
    style: Style | None = None
) -> None
```

**Example:**

```python
events = [
    {"title": "Project Started", "description": "Initial setup", "date": "2024-01-15"},
    {"title": "First Release", "description": "v0.1.0", "date": "2024-02-20"},
    {"title": "Major Update", "description": "Added new features", "date": "2024-03-10"},
]

um.timeline(events)
```

---

## Charts & Visualization

### line_chart()

Display a line chart.

```python
um.line_chart(
    data: list[dict],
    *,
    x: str,  # Column name for x-axis
    y: str | list[str],  # Column name(s) for y-axis
    title: str | None = None,
    height: str = "300px",
    colors: list[str] | None = None,
    style: Style | None = None
) -> None
```

**Example:**

```python
data = [
    {"month": "Jan", "revenue": 4000, "profit": 2400},
    {"month": "Feb", "revenue": 3000, "profit": 1398},
    {"month": "Mar", "revenue": 2000, "profit": 9800},
]

um.line_chart(data, x="month", y=["revenue", "profit"], title="Monthly Revenue")
```

### bar_chart()

Display a bar chart.

```python
um.bar_chart(
    data: list[dict],
    *,
    x: str,
    y: str | list[str],
    title: str | None = None,
    height: str = "300px",
    horizontal: bool = False,
    stacked: bool = False,
    colors: list[str] | None = None,
    style: Style | None = None
) -> None
```

**Example:**

```python
um.bar_chart(data, x="month", y="revenue", title="Monthly Revenue")
```

### area_chart()

Display an area chart.

```python
um.area_chart(
    data: list[dict],
    *,
    x: str,
    y: str | list[str],
    title: str | None = None,
    height: str = "300px",
    colors: list[str] | None = None,
    style: Style | None = None
) -> None
```

### pie_chart()

Display a pie chart.

```python
um.pie_chart(
    data: list[dict],
    *,
    label: str,  # Column for slice labels
    value: str,  # Column for slice values
    title: str | None = None,
    height: str = "300px",
    donut: bool = False,
    style: Style | None = None
) -> None
```

**Example:**

```python
data = [
    {"name": "Desktop", "value": 400},
    {"name": "Mobile", "value": 300},
    {"name": "Tablet", "value": 100},
]

um.pie_chart(data, label="name", value="value", title="Traffic Sources")
```

### scatter_chart()

Display a scatter plot.

```python
um.scatter_chart(
    data: list[dict],
    *,
    x: str,
    y: str,
    color: str | None = None,
    size: str | None = None,
    title: str | None = None,
    height: str = "300px",
    style: Style | None = None
) -> None
```

### plotly_chart()

Display a Plotly figure (full Plotly.js support).

```python
um.plotly_chart(
    figure: Any,  # Plotly figure object
    *,
    use_container_width: bool = True,
    theme: str | None = None,
    key: str | None = None,
    style: Style | None = None
) -> None
```

**Example:**

```python
import plotly.express as px

# Create Plotly figure
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")

# Display in Umara
um.plotly_chart(fig)
```

### map()

Display an interactive map.

```python
um.map(
    data: list[dict] | None = None,
    *,
    latitude: str = "lat",
    longitude: str = "lon",
    zoom: int = 10,
    height: str = "400px",
    style: Style | None = None
) -> None
```

**Example:**

```python
locations = [
    {"lat": 40.7128, "lon": -74.0060, "name": "NYC"},
    {"lat": 34.0522, "lon": -118.2437, "name": "LA"},
]

um.map(locations, zoom=4)
```

---

## Media Components

### image()

Display an image.

```python
um.image(
    src: str,  # URL or file path
    *,
    caption: str | None = None,
    width: str | None = None,
    use_container_width: bool = False,
    style: Style | None = None
) -> None
```

**Examples:**

```python
um.image("https://example.com/photo.jpg", caption="Beautiful sunset")
um.image("./local_image.png", width="300px")
um.image(uploaded_file, use_container_width=True)
```

### video()

Display a video player.

```python
um.video(
    src: str,
    *,
    start_time: int = 0,
    style: Style | None = None
) -> None
```

### audio()

Display an audio player.

```python
um.audio(
    src: str,
    *,
    start_time: int = 0,
    style: Style | None = None
) -> None
```

---

## Navigation Components

### breadcrumbs()

Display breadcrumb navigation.

```python
um.breadcrumbs(
    items: list[dict],  # [{"label": str, "href": str}, ...]
    *,
    style: Style | None = None
) -> None
```

**Example:**

```python
um.breadcrumbs([
    {"label": "Home", "href": "/"},
    {"label": "Products", "href": "/products"},
    {"label": "Detail", "href": "#"},
])
```

### steps()

Display progress steps.

```python
um.steps(
    steps: list[str],
    *,
    current: int = 0,
    key: str | None = None,
    style: Style | None = None
) -> int  # Returns current step
```

**Example:**

```python
current = um.steps(["Cart", "Shipping", "Payment", "Confirm"], current=1)
um.text(f"Current step: {current + 1}")
```

### pagination()

Display pagination controls.

```python
um.pagination(
    total_pages: int,
    *,
    current_page: int = 1,
    key: str | None = None,
    style: Style | None = None
) -> int  # Returns current page
```

**Example:**

```python
page = um.pagination(10, current_page=1, key="data_pagination")

# Display data for current page
start = (page - 1) * 10
um.dataframe(all_data[start:start + 10])
```

---

## Chat Components

### chat_container()

Create a container for chat messages.

```python
with um.chat_container(
    *,
    height: str = "400px",
    style: Style | None = None
):
    # Chat messages go here
```

### chat_message()

Display a single chat message.

```python
um.chat_message(
    content: str,
    *,
    role: str = "assistant",  # "user", "assistant", "system"
    avatar: str | None = None,
    name: str | None = None,
    style: Style | None = None
) -> None
```

### chat_input()

Create a chat input box.

```python
um.chat_input(
    placeholder: str = "Type your message...",
    *,
    key: str | None = None,
    style: Style | None = None
) -> str | None  # Returns message when submitted
```

**Complete Chat Example:**

```python
import umara as um

# Initialize message history
um.session_state.setdefault("messages", [])

# Display chat container with messages
with um.chat_container(height="400px"):
    for msg in um.session_state.messages:
        um.chat_message(msg["content"], role=msg["role"])

# Chat input
user_message = um.chat_input("Type your message...")

if user_message:
    # Add user message
    um.session_state.messages.append({"role": "user", "content": user_message})

    # Generate response (example)
    response = generate_response(user_message)
    um.session_state.messages.append({"role": "assistant", "content": response})

    um.rerun()
```

### chat()

Simplified chat widget that handles messages automatically.

```python
um.chat(
    messages: list[dict],  # [{"role": str, "content": str}, ...]
    *,
    key: str | None = None,
    height: str = "400px",
    style: Style | None = None
) -> str | None  # Returns new message when submitted
```

**Example:**

```python
messages = [
    {"role": "assistant", "content": "Hello! How can I help?"},
]

new_message = um.chat(messages, key="my_chat")

if new_message:
    # Handle new message
    messages.append({"role": "user", "content": new_message})
    # Add AI response...
```

---

## State Management

### session_state

Global session state that persists across reruns.

```python
# Set values
um.session_state.user_name = "Alice"
um.session_state.count = 0

# Get values
name = um.session_state.user_name
count = um.session_state.count

# Check existence
if "user_name" in um.session_state:
    um.text(f"Hello, {um.session_state.user_name}")

# Get with default
value = um.session_state.get("missing_key", "default_value")

# Set default if not exists
um.session_state.setdefault("counter", 0)

# Update multiple
um.session_state.update(name="Bob", age=30)

# Clear all
um.session_state.clear()

# Iterate
for key, value in um.session_state.items():
    um.text(f"{key}: {value}")
```

**Complete State Example:**

```python
import umara as um

# Initialize state
um.session_state.setdefault("counter", 0)

um.header("Counter App")
um.text(f"Count: {um.session_state.counter}")

with um.columns(3):
    with um.column():
        if um.button("Decrement", key="dec"):
            um.session_state.counter -= 1
    with um.column():
        if um.button("Reset", key="reset"):
            um.session_state.counter = 0
    with um.column():
        if um.button("Increment", key="inc"):
            um.session_state.counter += 1

um.metric("Counter Value", um.session_state.counter)
```

---

## Caching

### @cache_data

Cache function results based on inputs. Use for data operations.

```python
@um.cache_data(
    ttl: int | None = None,  # Time-to-live in seconds
    show_spinner: bool = True,
    max_entries: int | None = None  # LRU cache limit
)
def function():
    ...
```

**Examples:**

```python
# Cache forever
@um.cache_data
def load_data():
    return pd.read_csv("large_file.csv")

# Cache for 1 hour
@um.cache_data(ttl=3600)
def fetch_api_data(endpoint):
    return requests.get(endpoint).json()

# With max entries (LRU eviction)
@um.cache_data(max_entries=100)
def compute_expensive(x, y):
    return complex_calculation(x, y)

# Clear specific function's cache
load_data.clear()
```

### @cache_resource

Cache global resources (connections, models). Shared across all users.

```python
@um.cache_resource(ttl: int | None = None)
def get_resource():
    ...
```

**Examples:**

```python
# Database connection
@um.cache_resource
def get_database():
    return sqlite3.connect("app.db")

# ML model
@um.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))

# With TTL
@um.cache_resource(ttl=3600)
def get_api_client():
    return APIClient(api_key=os.environ["API_KEY"])
```

---

## Fragments (Partial Reruns)

### @fragment

Create sections that can rerun independently.

```python
@um.fragment(run_every: int | float | None = None)
def section():
    ...
```

**Parameters:**
- `run_every`: Auto-refresh interval in seconds

**Examples:**

```python
# Basic fragment - only reruns when its inputs change
@um.fragment
def chart_section():
    data_points = um.slider("Data points", 10, 100, 50, key="points")
    um.line_chart(generate_data(data_points))

# Auto-refreshing fragment (every 5 seconds)
@um.fragment(run_every=5)
def live_metrics():
    data = fetch_live_data()
    um.metric("Active Users", data["users"])
    um.metric("Requests/sec", data["rps"])

# Use fragments in your app
um.title("Dashboard")

chart_section()  # This is a fragment

um.divider()

live_metrics()  # This auto-refreshes
```

---

## Connections (Database & API)

### SQL Connections

```python
conn = um.connection.sql(
    connection_name: str,
    *,
    url: str,  # "sqlite:///app.db", "postgresql://user:pass@host/db"
    **kwargs
) -> SQLConnection
```

**Methods:**

```python
# Query (returns DataFrame or list of dicts)
df = conn.query("SELECT * FROM users WHERE age > ?", params=(18,))

# Execute (INSERT, UPDATE, DELETE)
conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", params=("Alice", 25))
```

**Example:**

```python
# Connect to SQLite
conn = um.connection.sql("mydb", url="sqlite:///data.db")

# Query data
users = conn.query("SELECT * FROM users LIMIT 10")
um.dataframe(users)

# Insert data
if um.button("Add User"):
    conn.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        params=(name, email)
    )
    um.success("User added!")
```

### HTTP/REST Connections

```python
api = um.connection.http(
    connection_name: str,
    *,
    base_url: str = "",
    headers: dict | None = None,
    timeout: int = 30,
    **kwargs
) -> HTTPConnection
```

**Methods:**

```python
api.get(endpoint, params=None, **kwargs) -> dict
api.post(endpoint, data=None, json=None, **kwargs) -> dict
api.put(endpoint, data=None, json=None, **kwargs) -> dict
api.delete(endpoint, **kwargs) -> dict | None
```

**Example:**

```python
# Connect to API
api = um.connection.http(
    "github",
    base_url="https://api.github.com",
    headers={"Authorization": f"token {token}"}
)

# Make requests
repos = api.get("/users/octocat/repos")

for repo in repos:
    um.text(f"- {repo['name']}: {repo['stargazers_count']} stars")
```

---

## Theming

### Built-in Themes

Umara includes 12 professional themes:

```python
um.set_theme("light")     # Clean, minimal (default)
um.set_theme("dark")      # Modern dark mode
um.set_theme("ocean")     # Calming blues
um.set_theme("forest")    # Earthy greens
um.set_theme("slate")     # Corporate gray
um.set_theme("nord")      # Arctic, Scandinavian
um.set_theme("midnight")  # Deep purple dark
um.set_theme("rose")      # Warm pink, fintech
um.set_theme("copper")    # Premium bronze
um.set_theme("lavender")  # Soft purple, calming
um.set_theme("sunset")    # Warm orange
um.set_theme("mint")      # Fresh teal
```

### Theme Persistence (v0.4.4)

Themes automatically:
- **Persist to localStorage**: User's theme choice is saved and restored on reload
- **Detect system preference**: Respects `prefers-color-scheme` for dark/light mode
- **Listen for changes**: Updates when user changes system dark mode

### Custom Themes

```python
# Create custom theme
my_theme = um.create_theme(
    "my_theme",
    base="light",  # Inherit from light theme
    colors={
        "primary": "#ff6b6b",
        "secondary": "#4ecdc4",
        "accent": "#ffe66d",
        "background": "#f7f7f7",
    }
)

um.set_theme(my_theme)

# Or directly
um.set_theme(um.create_theme("dark_blue", base="dark", colors={"primary": "#3b82f6"}))
```

### Theme Colors

Available color properties:

- `primary`, `primary_light`, `primary_hover`, `primary_active`
- `secondary`, `secondary_light`, `secondary_hover`
- `accent`
- `success`, `warning`, `error`, `info`
- `background`, `background_secondary`
- `surface`
- `border`, `border_light`
- `text`, `text_secondary`, `text_muted`
- `overlay`

---

## Styling

### Inline Styles

```python
my_style = um.style(
    color="#ff0000",
    fontSize="18px",
    fontWeight="bold",
    padding="16px",
    backgroundColor="#f0f0f0",
    borderRadius="8px"
)

um.text("Styled text", style=my_style)
um.card(style=um.style(boxShadow="0 4px 6px rgba(0,0,0,0.1)"))
```

### CSS Properties

Use camelCase for CSS properties:

```python
um.style(
    # Typography
    fontSize="16px",
    fontWeight="bold",
    lineHeight="1.5",
    textAlign="center",

    # Colors
    color="#333",
    backgroundColor="#fff",

    # Spacing
    padding="16px",
    margin="8px",

    # Layout
    display="flex",
    flexDirection="column",
    alignItems="center",
    justifyContent="center",

    # Borders
    border="1px solid #ccc",
    borderRadius="8px",

    # Effects
    boxShadow="0 2px 4px rgba(0,0,0,0.1)",
    opacity="0.9",

    # Sizing
    width="100%",
    maxWidth="600px",
    height="auto"
)
```

---

## Page Configuration

```python
um.set_page_config(
    page_title: str = "Umara App",
    page_icon: str | None = None,  # Emoji or URL
    layout: str = "centered",  # "centered" or "wide"
    initial_sidebar_state: str = "auto"  # "auto", "expanded", "collapsed"
) -> None
```

**Example:**

```python
um.set_page_config(
    page_title="My Dashboard",
    page_icon="📊",
    layout="wide"
)
```

---

## CLI Commands

### Run an App

```bash
umara run app.py [OPTIONS]
```

Options:
- `--host, -h`: Host to bind (default: 127.0.0.1)
- `--port, -p`: Port (default: 8501)
- `--reload/--no-reload`: Hot reload (default: enabled)
- `--debug/--no-debug`: Debug mode

Examples:

```bash
umara run app.py
umara run app.py --port 8000
umara run app.py --host 0.0.0.0 --port 80
umara run app.py --no-reload
```

### Create New Project

```bash
umara init [project_name]
```

Creates:
- `app.py` - Main application file
- `requirements.txt` - Dependencies
- `README.md` - Documentation

### Other Commands

```bash
umara themes    # List available themes
umara docs      # Open documentation
umara --version # Show version
umara --help    # Show help
```

---

## Accessibility

### ARIA Labels (v0.4.4)

Umara automatically adds ARIA attributes to interactive components for screen reader support:

- **Buttons**: `role="button"`, `aria-label`
- **Inputs**: `aria-label`, associated `<label>` elements
- **Sliders**: `role="slider"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`
- **Toggles**: `role="switch"`, `aria-checked`
- **Progress bars**: `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`

### Keyboard Navigation

- **Toggle switches**: Support Space and Enter keys
- **Modals**: Focus trap keeps keyboard navigation within modal
- **Forms**: Proper tab order and label associations

---

## Complete Examples

### Dashboard App

```python
import umara as um
import pandas as pd

um.set_page_config(page_title="Sales Dashboard", layout="wide")
um.set_theme("ocean")

# Sidebar
with um.sidebar():
    um.header("Filters")
    date_range = um.select("Period", ["Last 7 days", "Last 30 days", "Last 90 days"])
    region = um.multiselect("Region", ["North", "South", "East", "West"], default=["North"])

# Header
um.title("Sales Dashboard")
um.caption(f"Showing data for: {date_range}")

# Metrics
with um.columns(4):
    with um.column():
        um.metric("Total Revenue", "$124,500", delta=12.5)
    with um.column():
        um.metric("Orders", "1,234", delta=8.2)
    with um.column():
        um.metric("Customers", "892", delta=15.3)
    with um.column():
        um.metric("Avg Order Value", "$101", delta=-2.1)

um.divider()

# Charts
with um.columns(2):
    with um.column():
        with um.card(title="Revenue Trend"):
            um.line_chart(revenue_data, x="date", y="revenue")

    with um.column():
        with um.card(title="Sales by Category"):
            um.pie_chart(category_data, label="category", value="sales")

# Data table
um.header("Recent Orders")
um.dataframe(orders_df, sortable=True)
```

### Chat Application

```python
import umara as um

um.set_page_config(page_title="AI Chat")
um.set_theme("dark")

um.title("AI Assistant")

# Initialize messages
um.session_state.setdefault("messages", [
    {"role": "assistant", "content": "Hello! How can I help you today?"}
])

# Display messages
with um.chat_container(height="500px"):
    for msg in um.session_state.messages:
        um.chat_message(msg["content"], role=msg["role"])

# Input
user_input = um.chat_input("Type your message...")

if user_input:
    # Add user message
    um.session_state.messages.append({"role": "user", "content": user_input})

    # Generate AI response
    with um.spinner("Thinking..."):
        response = call_ai_api(user_input)

    um.session_state.messages.append({"role": "assistant", "content": response})
    um.rerun()
```

### Data Entry Form

```python
import umara as um

um.set_page_config(page_title="Registration")
um.set_theme("light")

with um.container():
    um.title("Create Account")

    with um.card():
        with um.form("registration"):
            um.subheader("Personal Information")

            with um.columns(2):
                with um.column():
                    first_name = um.input("First Name", key="first_name")
                with um.column():
                    last_name = um.input("Last Name", key="last_name")

            email = um.input("Email", type="email", key="email")
            password = um.input("Password", type="password", key="password")

            um.subheader("Preferences")

            plan = um.radio("Plan", ["Free", "Pro", "Enterprise"], default="Free")

            newsletter = um.checkbox("Subscribe to newsletter")
            terms = um.checkbox("I agree to the terms and conditions")

            um.spacer()

            if um.form_submit_button("Create Account"):
                if not all([first_name, last_name, email, password]):
                    um.error("Please fill in all required fields")
                elif not terms:
                    um.error("You must agree to the terms")
                else:
                    um.success(f"Account created for {email}!")
```

### Real-time Dashboard

```python
import umara as um
import random

um.set_page_config(page_title="Live Metrics", layout="wide")
um.set_theme("dark")

um.title("System Monitor")

# Auto-refreshing metrics
@um.fragment(run_every=2)
def live_metrics():
    with um.columns(4):
        with um.column():
            um.metric("CPU Usage", f"{random.randint(20, 80)}%")
        with um.column():
            um.metric("Memory", f"{random.randint(40, 90)}%")
        with um.column():
            um.metric("Network", f"{random.randint(100, 500)} Mbps")
        with um.column():
            um.metric("Requests", f"{random.randint(1000, 5000)}/s")

live_metrics()

um.divider()

# Static content
um.header("System Status")
um.success("All systems operational")
```

### File Upload with Validation

```python
import umara as um

um.set_page_config(page_title="File Upload")
um.header("Document Upload")

with um.card():
    um.text("Upload your documents (max 10MB per file)")

    uploaded = um.file_uploader(
        "Select files",
        accept=[".pdf", ".docx", ".xlsx"],
        multiple=True,
        max_file_size=10 * 1024 * 1024  # 10MB
    )

    if uploaded:
        um.success(f"Uploaded {len(uploaded)} file(s)")

        um.dataframe([
            {"Name": f["name"], "Size": f"{f['size'] / 1024:.1f} KB", "Type": f["type"]}
            for f in uploaded
        ], sortable=True)
```

---

## Best Practices

### 1. Use Keys for Stateful Widgets

```python
# Good - unique key
name = um.input("Name", key="user_name_input")

# Bad - no key, may cause state issues
name = um.input("Name")
```

### 2. Initialize State with setdefault

```python
# Good
um.session_state.setdefault("counter", 0)

# Avoid
if "counter" not in um.session_state:
    um.session_state.counter = 0
```

### 3. Cache Expensive Operations

```python
# Good - cached
@um.cache_data
def load_large_dataset():
    return pd.read_csv("huge_file.csv")

# Bad - reloads every rerun
df = pd.read_csv("huge_file.csv")
```

### 4. Use Fragments for Independent Sections

```python
# Good - only this section reruns
@um.fragment
def chart_section():
    ...

# Bad - whole app reruns on any change
def chart_section():
    ...
```

### 5. Organize with Layout Components

```python
# Good - clear structure
with um.columns(2):
    with um.column():
        with um.card(title="Section 1"):
            ...
    with um.column():
        with um.card(title="Section 2"):
            ...

# Bad - flat structure, harder to maintain
um.text("Section 1")
um.text("Content...")
um.text("Section 2")
um.text("More content...")
```

---

## Version History

- **0.4.5** - Fixed SessionState bracket notation support, updated documentation
- **0.4.4** - Added max_file_size for file_uploader, sortable dataframes, ARIA accessibility labels, system theme detection, localStorage theme persistence
- **0.4.3** - Added button loading states, modal focus trap, chat auto-scroll
- **0.4.2** - Added horizontal input labels, right-aligned numbers in tables
- **0.4.0** - Added Plotly charts, cache decorators, streaming support, connections
- **0.3.0** - Added fragments, improved download_button
- **0.2.0** - Added themes, state management, WebSocket communication
- **0.1.0** - Initial release with core components

---

*Documentation generated for Umara v0.4.5*
