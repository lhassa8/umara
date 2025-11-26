"""
Comprehensive test application for all Umara components.
This app tests every component to verify they render and function correctly.
"""

import umara as um

# Set theme
um.set_theme('ocean')

# =============================================================================
# SECTION 1: Typography
# =============================================================================
um.header('Component Test Suite', level=1)
um.text('This app tests all Umara components systematically.')
um.divider()

um.subheader('1. Typography Components')

with um.card(title='Typography'):
    um.header('Header Level 1', level=1)
    um.header('Header Level 2', level=2)
    um.header('Header Level 3', level=3)
    um.subheader('Subheader')
    um.text('Regular text content')
    um.text('Colored text', color='#6366f1')
    um.markdown('**Bold**, *italic*, and `code` in markdown')
    um.code('def hello():\n    print("Hello, World!")', language='python')

um.divider()

# =============================================================================
# SECTION 2: Feedback Components
# =============================================================================
um.subheader('2. Feedback Components')

with um.card(title='Alerts'):
    um.success('This is a success message')
    um.error('This is an error message')
    um.warning('This is a warning message')
    um.info('This is an info message')

um.divider()

# =============================================================================
# SECTION 3: Input Components (with forms)
# =============================================================================
um.subheader('3. Input Components')

with um.card(title='Form with All Inputs'):
    with um.form('test_form'):
        # Text input
        text_val = um.input('Text Input', placeholder='Enter text...')

        # Text area
        textarea_val = um.text_area('Text Area', placeholder='Enter multiple lines...')

        # Select
        select_val = um.select('Select', options=['Option A', 'Option B', 'Option C'], default='Option A')

        # Multi-select
        multiselect_val = um.multiselect('Multi-Select', options=['Red', 'Green', 'Blue'], default=['Red'])

        # Slider
        slider_val = um.slider('Slider', min_value=0, max_value=100, value=50)

        # Checkbox
        checkbox_val = um.checkbox('Checkbox')

        # Toggle
        toggle_val = um.toggle('Toggle Switch')

        # Radio
        radio_val = um.radio('Radio Buttons', options=['Small', 'Medium', 'Large'], default='Medium')

        if um.form_submit_button('Submit Form'):
            um.success(f'Form submitted! Text: {text_val}, Select: {select_val}')

um.divider()

# =============================================================================
# SECTION 4: Standalone Inputs (with keys)
# =============================================================================
um.subheader('4. Standalone Inputs (Real-time)')

with um.card(title='Real-time Inputs'):
    # These use keys for persistence
    search = um.input('Search (live)', key='search_input', placeholder='Type to search...')
    if search:
        um.text(f'You typed: {search}')

    um.spacer('16px')

    live_slider = um.slider('Live Slider', 0, 100, key='live_slider')
    um.text(f'Slider value: {live_slider}')

    um.spacer('16px')

    live_toggle = um.toggle('Live Toggle', key='live_toggle')
    um.text(f'Toggle is: {"ON" if live_toggle else "OFF"}')

um.divider()

# =============================================================================
# SECTION 5: Layout Components
# =============================================================================
um.subheader('5. Layout Components')

# Columns
um.text('**Columns Layout:**')
with um.columns(3):
    with um.column():
        with um.card():
            um.text('Column 1')
    with um.column():
        with um.card():
            um.text('Column 2')
    with um.column():
        with um.card():
            um.text('Column 3')

um.spacer()

# Grid
um.text('**Grid Layout:**')
with um.grid(columns=4, gap='12px'):
    for i in range(8):
        with um.card():
            um.text(f'Grid Item {i+1}')

um.divider()

# =============================================================================
# SECTION 6: Tabs
# =============================================================================
um.subheader('6. Tabs Component')

with um.tabs(['Tab One', 'Tab Two', 'Tab Three']) as t:
    with t.tab(0):
        um.text('Content for Tab One')
        um.info('This is the first tab')
    with t.tab(1):
        um.text('Content for Tab Two')
        um.warning('This is the second tab')
    with t.tab(2):
        um.text('Content for Tab Three')
        um.success('This is the third tab')

um.divider()

# =============================================================================
# SECTION 7: Data Display
# =============================================================================
um.subheader('7. Data Display Components')

with um.columns(3):
    with um.column():
        um.metric('Total Users', '12,543', delta=12.5, delta_label='from last week')
    with um.column():
        um.metric('Revenue', '$48,200', delta=-2.3)
    with um.column():
        um.metric('Conversion', '3.24%', delta=0.5)

um.spacer()

um.text('**Progress Bar:**')
um.progress(75, label='Task Progress')

um.spacer()

um.text('**Data Table:**')
sample_data = [
    {'Name': 'Alice', 'Age': 28, 'City': 'New York'},
    {'Name': 'Bob', 'Age': 34, 'City': 'San Francisco'},
    {'Name': 'Charlie', 'Age': 22, 'City': 'Chicago'},
    {'Name': 'Diana', 'Age': 31, 'City': 'Boston'},
]
um.dataframe(sample_data, sortable=True)

um.divider()

# =============================================================================
# SECTION 8: Buttons
# =============================================================================
um.subheader('8. Button Variants')

with um.columns(5):
    with um.column():
        if um.button('Primary', variant='primary', key='btn_primary'):
            um.session_state.setdefault('btn_clicks', 0)
            um.session_state.btn_clicks += 1
    with um.column():
        um.button('Secondary', variant='secondary', key='btn_secondary')
    with um.column():
        um.button('Outline', variant='outline', key='btn_outline')
    with um.column():
        um.button('Ghost', variant='ghost', key='btn_ghost')
    with um.column():
        um.button('Danger', variant='danger', key='btn_danger')

um.text(f"Primary button clicked: {um.session_state.get('btn_clicks', 0)} times")

um.divider()

# =============================================================================
# SECTION 9: Additional Components
# =============================================================================
um.subheader('9. Additional Components')

with um.card(title='Expander'):
    with um.expander('Click to expand', expanded=False):
        um.text('This content is hidden by default')
        um.info('You expanded the section!')

um.spacer()

# Horizontal radio
um.text('**Horizontal Radio:**')
h_radio = um.radio('Size Selection', options=['XS', 'S', 'M', 'L', 'XL'], horizontal=True, key='h_radio')
um.text(f'Selected: {h_radio}')

um.divider()

# =============================================================================
# SECTION 10: State Management
# =============================================================================
um.subheader('10. State Management')

um.session_state.setdefault('counter', 0)

with um.card(title='Counter Example'):
    um.text(f'Counter value: {um.session_state.counter}')

    with um.columns(2):
        with um.column():
            if um.button('Increment', key='inc'):
                um.session_state.counter += 1
        with um.column():
            if um.button('Reset', variant='outline', key='reset'):
                um.session_state.counter = 0

um.divider()

# =============================================================================
# SECTION 11: Complex Form Example
# =============================================================================
um.subheader('11. Contact Form (Real-world Example)')

with um.card(title='Contact Us'):
    with um.form('contact_form'):
        with um.columns(2):
            with um.column():
                first_name = um.input('First Name', placeholder='John')
            with um.column():
                last_name = um.input('Last Name', placeholder='Doe')

        email = um.input('Email', placeholder='john@example.com', type='email')
        subject = um.select('Subject', options=['General Inquiry', 'Support', 'Feedback', 'Other'])
        message = um.text_area('Message', placeholder='Your message here...', rows=5)

        agree = um.checkbox('I agree to the terms and conditions')

        if um.form_submit_button('Send Message'):
            if not first_name or not last_name or not email or not message:
                um.error('Please fill in all required fields')
            elif not agree:
                um.warning('Please agree to the terms and conditions')
            else:
                um.success(f'Thank you {first_name}! Your message has been sent.')

um.divider()
um.text('Test suite complete. Check console for any errors.', color='#888')
