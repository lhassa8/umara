<div align="center">

# Umara

### Beautiful Python UIs — Without the Complexity

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Getting Started](#quick-start) • [Documentation](#documentation) • [Examples](#examples) • [Contributing](#contributing)

</div>

---

## Why Umara?

**Umara** is a modern Python framework for building web applications with pure Python. No HTML, CSS, or JavaScript required.

Think of it as a more polished alternative to Streamlit — with better styling, smarter state management, and more layout control.

```python
import umara as um

um.set_theme('ocean')

um.header('Welcome to Umara')

name = um.input('Your name')
if um.button('Say Hello'):
    um.success(f'Hello, {name}!')
```

### Key Differentiators

| Feature | Umara | Streamlit |
|---------|-------|-----------|
| **Default Styling** | Modern, polished design | Basic styling |
| **Theming** | 12 built-in themes + custom | Limited |
| **Layout Control** | Flexbox, Grid, precise positioning | Column-based only |
| **State Management** | Component-level, efficient | Full script re-runs |
| **Animations** | Smooth transitions built-in | None |
| **Performance** | Smart re-rendering | Re-runs entire script |

## Features

- **Beautiful by Default** — Components look polished out of the box
- **Fast & Reactive** — WebSocket-based for instant UI updates
- **Flexible Theming** — 12 professional themes + custom themes
- **Powerful Layouts** — Columns, grids, cards, tabs with precise control
- **Hot Reload** — See changes instantly during development
- **Smart State** — Efficient updates without full re-runs

## Quick Start

### Installation

```bash
pip install umara
```

### Create Your First App

Create `app.py`:

```python
import umara as um

um.set_theme('light')

um.header('My First Umara App')
um.text('Building beautiful UIs is easy!')

with um.card():
    name = um.input('Enter your name', placeholder='John Doe')
    age = um.slider('Select your age', 0, 100, 25)

    if um.button('Submit', variant='primary'):
        um.success(f'Hello {name}, you are {age} years old!')

with um.columns(3):
    with um.column():
        um.metric('Users', '12.5K', delta=12.3)
    with um.column():
        um.metric('Revenue', '$48K', delta=8.1)
    with um.column():
        um.metric('Growth', '23%', delta=-2.4)
```

### Run Your App

Start the development server:

```bash
umara run app.py
```

Then open your browser to **http://localhost:8501** to see your app.

The server runs with hot reload enabled by default, so any changes you make to `app.py` will automatically refresh in the browser.

## Documentation

### Themes

```python
# 12 built-in professional themes
um.set_theme('light')     # Clean, minimal
um.set_theme('dark')      # Modern dark mode
um.set_theme('ocean')     # Calming blues
um.set_theme('forest')    # Earthy greens
um.set_theme('slate')     # Corporate gray
um.set_theme('nord')      # Arctic, Scandinavian
um.set_theme('midnight')  # Deep purple dark
um.set_theme('rose')      # Warm pink, fintech
um.set_theme('copper')    # Premium bronze
um.set_theme('lavender')  # Soft purple, calming
um.set_theme('sunset')    # Warm orange
um.set_theme('mint')      # Fresh teal

# Create custom themes
um.create_theme(
    'my-brand',
    base='dark',
    colors={
        'primary': '#ff6b6b',
        'accent': '#4ecdc4'
    }
)
```

### Layout Components

<details>
<summary><b>Columns</b></summary>

```python
with um.columns(3):
    with um.column():
        um.text('Column 1')
    with um.column():
        um.text('Column 2')
    with um.column():
        um.text('Column 3')
```
</details>

<details>
<summary><b>Grid</b></summary>

```python
with um.grid(columns=4, gap='16px'):
    for i in range(8):
        with um.card():
            um.text(f'Card {i+1}')
```
</details>

<details>
<summary><b>Cards</b></summary>

```python
with um.card(title='Dashboard', subtitle='Real-time metrics'):
    um.metric('Active Users', '1,234')
    um.progress(75, label='Server Load')
```
</details>

<details>
<summary><b>Tabs</b></summary>

```python
with um.tabs(['Overview', 'Analytics', 'Settings']) as t:
    with t.tab(0):
        um.text('Overview content')
    with t.tab(1):
        um.text('Analytics content')
    with t.tab(2):
        um.text('Settings content')
```
</details>

### Input Widgets

```python
# Text inputs
name = um.input('Name', placeholder='Enter name...')
bio = um.text_area('Bio', rows=4)

# Selection
option = um.select('Choose', options=['A', 'B', 'C'])
value = um.slider('Value', 0, 100, 50)

# Toggles
agreed = um.checkbox('I agree to terms')
enabled = um.toggle('Enable feature')

# Buttons with variants
um.button('Primary', variant='primary')
um.button('Secondary', variant='secondary')
um.button('Outline', variant='outline')
um.button('Danger', variant='danger')
```

### Data Display

```python
# Metrics with deltas
um.metric('Revenue', '$48,234', delta=12.5, delta_label='vs last month')

# Progress bars
um.progress(75, label='Completion')

# Tables (works with pandas)
data = [
    {'Name': 'Alice', 'Role': 'Engineer'},
    {'Name': 'Bob', 'Role': 'Designer'},
]
um.dataframe(data)

# Stat cards with trends
um.stat_card('Total Users', '12,543', trend=12.5, icon='Users')
```

### Charts

```python
# Line chart
data = [
    {'month': 'Jan', 'revenue': 10000, 'profit': 2000},
    {'month': 'Feb', 'revenue': 25000, 'profit': 5000},
]
um.line_chart(data, x='month', y=['revenue', 'profit'], title='Revenue & Profit')

# Bar chart
um.bar_chart(data, x='category', y='sales', title='Sales by Category')

# Area chart
um.area_chart(data, x='month', y='revenue', title='Revenue Trend')

# Pie chart
um.pie_chart(data, label='name', value='share', title='Market Share')
```

### Smart Write

```python
# Automatically handles any data type
um.write('Hello, world!')           # Text
um.write(42)                        # Numbers
um.write({'a': 1, 'b': 2})          # Dicts as JSON
um.write(df)                        # DataFrames as tables
um.write(my_chart)                  # Charts
```

### Forms

```python
with um.form('my_form'):
    name = um.input('Name')
    email = um.input('Email')

    if um.form_submit_button('Submit'):
        um.success(f'Thanks {name}!')
```

### Feedback Messages

```python
um.success('Operation completed!')
um.error('Something went wrong.')
um.warning('Please review your input.')
um.info('Pro tip: Try the dark theme!')
um.toast('Quick notification!')     # Toast notification
```

### Custom Styling

```python
from umara import style

um.text(
    'Styled text',
    style=style(
        color='#6366f1',
        font_size='24px',
        font_weight='bold'
    )
)
```

## CLI Commands

```bash
# Run an app
umara run app.py

# Run with options
umara run app.py --host 0.0.0.0 --port 8080

# Create new project
umara init my_project

# List themes
umara themes
```

## Examples

### Dashboard

```python
import umara as um

um.set_theme('dark')
um.header('Analytics Dashboard')

with um.columns(4):
    for label, value, trend in [
        ('Users', '12,543', 12.5),
        ('Revenue', '$48.2K', 8.2),
        ('Sessions', '1,892', -2.4),
        ('Conversion', '3.24%', 0.5),
    ]:
        with um.column():
            um.stat_card(label, value, trend=trend)

um.subheader('Recent Activity')
um.dataframe(activity_data)
```

### Form

```python
import umara as um

um.header('Contact Form')

with um.card():
    name = um.input('Name', key='name')
    email = um.input('Email', key='email')
    message = um.text_area('Message', key='message')

    if um.button('Send Message', variant='primary'):
        if name and email and message:
            um.success('Message sent successfully!')
        else:
            um.error('Please fill in all fields.')
```

## Chat Interface

Build AI chatbot interfaces:

```python
import umara as um

# Simple chat widget
messages = [
    {'role': 'assistant', 'content': 'Hello! How can I help?'},
    {'role': 'user', 'content': 'What is Umara?'},
]

message = um.chat(messages, key='my_chat')

if message:
    # Handle new message (call your AI API here)
    messages.append({'role': 'user', 'content': message})
```

Or build custom chat layouts:

```python
with um.chat_container(height='400px'):
    um.chat_message('user', 'Hello!')
    um.chat_message('assistant', 'Hi there!')

um.chat_input('Type a message...', key='input')
```

## All Components

### Layout
`container`, `columns`, `grid`, `card`, `tabs`, `divider`, `spacer`, `sidebar`

### Typography
`title`, `header`, `subheader`, `text`, `caption`, `markdown`, `code`, `latex`

### Inputs
`button`, `download_button`, `link_button`, `input`, `text_area`, `number_input`, `slider`, `select_slider`, `select`, `multiselect`, `checkbox`, `toggle`, `radio`, `date_input`, `time_input`, `color_picker`, `rating`, `file_uploader`, `camera_input`, `audio_input`, `pills`, `segmented_control`, `feedback`

### Forms
`form`, `form_submit_button`

### Data Display
`write`, `dataframe`, `data_editor`, `table`, `metric`, `stat_card`, `progress`, `badge`, `avatar`, `avatar_group`

### Feedback
`success`, `error`, `warning`, `info`, `toast`, `spinner`, `status`, `loading_skeleton`, `empty_state`, `exception`

### Navigation
`breadcrumbs`, `pagination`, `steps`, `nav_link`

### Container
`expander`, `accordion`, `modal`, `dialog`, `popover`, `tooltip`

### Chat
`chat`, `chat_message`, `chat_input`, `chat_container`

### Charts
`line_chart`, `bar_chart`, `area_chart`, `pie_chart`, `scatter_chart`, `map`

### Media
`image`, `video`, `audio`, `logo`, `iframe`

### Utility
`timeline`, `json_viewer`, `html`, `copy_button`, `tag_input`, `search_input`

### Page Config
`set_page_config`, `rerun`, `stop`

## Architecture

```
umara/
├── umara/                 # Python package
│   ├── core.py           # App lifecycle & component tree
│   ├── components.py     # UI components
│   ├── server.py         # WebSocket server
│   ├── frontend.py       # Frontend HTML/CSS/JS
│   ├── state.py          # State management
│   ├── themes.py         # Theming system
│   └── cli.py            # CLI commands
└── examples/             # Example apps
```

## Contributing

Contributions are welcome. Here's how to get started:

```bash
# Clone the repo
git clone https://github.com/lhassa8/umara.git
cd umara

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in dev mode with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run the demo app
umara run examples/demo_app.py
# Then open http://localhost:8501 in your browser
```

## Roadmap

- [x] Charts & data visualization
- [x] Chat/conversation components
- [x] Additional input types
- [x] Modern frontend with animations
- [x] Streamlit parity (112 components)
- [x] Forms with batched submission
- [x] Page configuration
- [ ] Authentication helpers
- [ ] Multi-page app support
- [ ] Component marketplace
- [ ] VS Code extension

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built for the Python community**

[Back to top](#umara)

</div>
