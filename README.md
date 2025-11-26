<div align="center">

# Umara

### Beautiful Python UIs — Without the Complexity

[![PyPI version](https://badge.fury.io/py/umara.svg)](https://pypi.org/project/umara/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

[Getting Started](#getting-started) • [Documentation](#documentation) • [Examples](#examples) • [Contributing](#contributing)

</div>

---

## What is Umara?

**Umara** is a modern Python framework for building beautiful web applications with pure Python. No HTML, CSS, or JavaScript required.

```python
import umara as um

um.header('Hello, Umara!')
name = um.input('Your name')

if um.button('Greet'):
    um.success(f'Welcome, {name}!')
```

**Why Umara?**

- **Beautiful by Default** — Components look polished out of the box with modern design
- **Fast & Reactive** — WebSocket-based architecture for instant UI updates
- **12 Built-in Themes** — Professional themes including dark mode, ocean, forest, and more
- **Flexible Layouts** — Columns, grids, cards, tabs, sidebars with precise control
- **Hot Reload** — See changes instantly during development
- **Smart State** — Efficient updates without full page re-runs

---

## Getting Started

### 1. Install Umara

```bash
pip install umara
```

### 2. Create Your App

Create a file called `app.py`:

```python
import umara as um

um.set_theme('ocean')

um.header('My First App')
um.text('Building beautiful UIs is easy!')

with um.card():
    name = um.input('Enter your name', placeholder='John Doe')

    if um.button('Say Hello', variant='primary'):
        um.success(f'Hello, {name}!')
```

### 3. Run Your App

```bash
umara run app.py
```

### 4. Open in Browser

Navigate to **http://localhost:8501** in your browser.

That's it! Your app is running with hot reload enabled — any changes to `app.py` will automatically refresh in the browser.

---

## Core Concepts

### Components

Umara provides 100+ components for building UIs:

```python
# Typography
um.title('Page Title')
um.header('Section Header')
um.text('Regular text')

# Inputs
name = um.input('Name', placeholder='Enter name...')
age = um.slider('Age', 0, 100, 25)
color = um.select('Color', ['Red', 'Green', 'Blue'])
agreed = um.checkbox('I agree')

# Feedback
um.success('Operation completed!')
um.error('Something went wrong')
um.warning('Please check your input')
um.info('Helpful tip here')

# Data Display
um.metric('Users', '12,543', delta=12.5)
um.progress(75, label='Completion')
um.dataframe(data)  # Works with pandas DataFrames
```

### Layouts

Organize content with flexible layout components:

```python
# Columns
with um.columns(3):
    with um.column():
        um.metric('Users', '1,234')
    with um.column():
        um.metric('Revenue', '$5,678')
    with um.column():
        um.metric('Growth', '12.5%')

# Cards
with um.card(title='Dashboard'):
    um.text('Card content here')

# Tabs
with um.tabs(['Overview', 'Data', 'Settings']) as t:
    with t.tab(0):
        um.text('Overview content')
    with t.tab(1):
        um.dataframe(data)
    with t.tab(2):
        um.toggle('Enable feature')

# Grid
with um.grid(columns=4, gap='16px'):
    for i in range(8):
        with um.card():
            um.text(f'Item {i + 1}')
```

### Themes

Switch between 12 professional themes:

```python
um.set_theme('light')     # Clean, minimal
um.set_theme('dark')      # Modern dark mode
um.set_theme('ocean')     # Calming blues
um.set_theme('forest')    # Earthy greens
um.set_theme('slate')     # Corporate gray
um.set_theme('nord')      # Arctic, Scandinavian
um.set_theme('midnight')  # Deep purple dark
um.set_theme('rose')      # Warm pink
um.set_theme('copper')    # Premium bronze
um.set_theme('lavender')  # Soft purple
um.set_theme('sunset')    # Warm orange
um.set_theme('mint')      # Fresh teal
```

Themes persist in localStorage and respect system dark/light mode preferences.

### State Management

Use `session_state` to persist data across interactions:

```python
# Initialize state
um.session_state.setdefault('counter', 0)

# Display current value
um.text(f'Count: {um.session_state.counter}')

# Update state
if um.button('Increment'):
    um.session_state.counter += 1
```

### Keys and Forms

**Standalone inputs require a `key` parameter** to persist values across reruns:

```python
# Without key - value resets on every rerun (not recommended)
name = um.input('Name')

# With key - value persists across reruns (recommended)
name = um.input('Name', key='user_name')
email = um.input('Email', key='user_email')
```

**Use forms when you want to batch multiple inputs** and only trigger an action on submit:

```python
# Form - values are batched, action triggers on submit
with um.form('contact'):
    name = um.input('Name', key='name')
    email = um.input('Email', key='email')

    if um.form_submit_button('Submit'):
        # All values available here
        um.success(f'Submitted: {name}, {email}')
```

**When to use which:**

| Scenario | Use |
|----------|-----|
| Single input that triggers immediate action | Standalone with `key` |
| Multiple related fields submitted together | `um.form()` |
| Real-time filtering/search | Standalone with `key` |
| Data entry that should be validated together | `um.form()` |

---

## Documentation

### Full API Reference

See [docs/UMARA_COMPLETE_REFERENCE.md](docs/UMARA_COMPLETE_REFERENCE.md) for complete documentation including:

- All 100+ components with parameters and examples
- State management and caching
- Theming and custom styles
- Database and API connections
- Fragments for partial reruns
- Best practices

### Quick Reference

#### Input Components

| Component | Description | Returns |
|-----------|-------------|---------|
| `um.input(label, key=...)` | Text input field | `str` |
| `um.text_area(label, key=...)` | Multi-line text | `str` |
| `um.number_input(label, key=...)` | Numeric input | `float` |
| `um.slider(label, min, max, value, key=...)` | Range slider | `float` |
| `um.select(label, options, key=...)` | Dropdown select | `str` |
| `um.multiselect(label, options, key=...)` | Multi-select | `list[str]` |
| `um.checkbox(label, key=...)` | Checkbox | `bool` |
| `um.toggle(label, key=...)` | Toggle switch | `bool` |
| `um.radio(label, options, key=...)` | Radio buttons | `str` |
| `um.date_input(label, key=...)` | Date picker | `str` |
| `um.time_input(label, key=...)` | Time picker | `str` |
| `um.color_picker(label, key=...)` | Color picker | `str` |
| `um.file_uploader(label, key=...)` | File upload | `file \| None` |
| `um.button(label, key=...)` | Click button | `bool` |

**Important:** Use `key` parameter for inputs outside forms to persist values across reruns.

#### Display Components

| Component | Description |
|-----------|-------------|
| `um.title(text)` | Large page title |
| `um.header(text)` | Section header |
| `um.subheader(text)` | Subsection header |
| `um.text(text)` | Regular text |
| `um.markdown(text)` | Markdown content |
| `um.code(code, language)` | Syntax-highlighted code |
| `um.metric(label, value, delta)` | Metric with trend |
| `um.progress(value, label)` | Progress bar |
| `um.dataframe(data)` | Data table (sortable) |
| `um.json_viewer(data)` | JSON tree view |

#### Feedback Components

| Component | Description |
|-----------|-------------|
| `um.success(message)` | Green success alert |
| `um.error(message)` | Red error alert |
| `um.warning(message)` | Yellow warning alert |
| `um.info(message)` | Blue info alert |
| `um.toast(message)` | Temporary notification |
| `um.spinner(text)` | Loading spinner |

#### Layout Components

| Component | Description |
|-----------|-------------|
| `um.columns(count)` | Multi-column layout |
| `um.grid(columns)` | CSS grid layout |
| `um.card(title)` | Card container |
| `um.tabs(names)` | Tabbed interface |
| `um.expander(title)` | Collapsible section |
| `um.sidebar()` | Side navigation |
| `um.modal(title, key)` | Modal dialog |
| `um.form(key)` | Form container |

#### Charts

| Component | Description |
|-----------|-------------|
| `um.line_chart(data, x, y)` | Line chart |
| `um.bar_chart(data, x, y)` | Bar chart |
| `um.area_chart(data, x, y)` | Area chart |
| `um.pie_chart(data, label, value)` | Pie chart |
| `um.scatter_chart(data, x, y)` | Scatter plot |
| `um.plotly_chart(figure)` | Plotly figure |

---

## Examples

### Dashboard

```python
import umara as um

um.set_theme('dark')
um.header('Analytics Dashboard')

# Metrics row
with um.columns(4):
    for label, value, delta in [
        ('Users', '12,543', 12.5),
        ('Revenue', '$48.2K', 8.2),
        ('Sessions', '1,892', -2.4),
        ('Conversion', '3.24%', 0.5),
    ]:
        with um.column():
            with um.card():
                um.metric(label, value, delta=delta)

# Chart
um.subheader('Revenue Trend')
um.line_chart(data, x='month', y='revenue')

# Data table
um.subheader('Recent Orders')
um.dataframe(orders, sortable=True)
```

### Form

```python
import umara as um

um.header('Contact Form')

with um.card():
    with um.form('contact'):
        name = um.input('Name', key='name')
        email = um.input('Email', type='email', key='email')
        message = um.text_area('Message', key='message')

        if um.form_submit_button('Send'):
            if name and email and message:
                um.success('Message sent!')
            else:
                um.error('Please fill all fields')
```

### Chat Interface

```python
import umara as um

um.set_theme('dark')
um.header('AI Chat')

# Initialize messages
um.session_state.setdefault('messages', [])

# Display chat
with um.chat_container(height='400px'):
    for msg in um.session_state.messages:
        um.chat_message(msg['content'], role=msg['role'])

# Input
user_input = um.chat_input('Type a message...')

if user_input:
    um.session_state.messages.append({'role': 'user', 'content': user_input})
    # Add your AI response logic here
    response = "This is a response"
    um.session_state.messages.append({'role': 'assistant', 'content': response})
```

### File Upload with Size Limit

```python
import umara as um

# Max 5MB file size
uploaded = um.file_uploader(
    'Upload Document',
    accept=['.pdf', '.docx'],
    max_file_size=5 * 1024 * 1024  # 5MB in bytes
)

if uploaded:
    um.success(f'Uploaded: {uploaded["name"]}')
```

---

## CLI Commands

```bash
# Run an app
umara run app.py

# Run with custom host/port
umara run app.py --host 0.0.0.0 --port 8080

# Create new project
umara init my_project

# List available themes
umara themes
```

---

## Project Structure

```
umara/
├── umara/                 # Python package
│   ├── core.py           # App lifecycle & component tree
│   ├── components.py     # 100+ UI components
│   ├── server.py         # WebSocket server
│   ├── frontend.py       # Frontend HTML/CSS/JS
│   ├── state.py          # State management
│   ├── themes.py         # 12 built-in themes
│   └── cli.py            # CLI commands
├── examples/             # Example applications
└── docs/                 # Documentation
```

---

## Contributing

Contributions are welcome! Here's how to set up for development:

```bash
# Clone the repository
git clone https://github.com/lhassa8/umara.git
cd umara

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run the demo app
umara run examples/demo_app.py
# Open http://localhost:8501 in your browser
```

---

## Roadmap

- [x] 100+ UI components
- [x] 12 built-in themes
- [x] Charts & data visualization
- [x] Chat/conversation components
- [x] Forms with batched submission
- [x] File uploads with size limits
- [x] Sortable data tables
- [x] ARIA accessibility labels
- [x] System theme detection
- [x] Theme persistence (localStorage)
- [ ] Authentication helpers
- [ ] Multi-page app support
- [ ] Component marketplace
- [ ] VS Code extension

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with Python**

[GitHub](https://github.com/lhassa8/umara) • [PyPI](https://pypi.org/project/umara/)

</div>
