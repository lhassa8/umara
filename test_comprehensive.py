"""
Comprehensive Component Test Suite for Umara
Tests every component to verify they render correctly.
"""

import umara as um

um.set_theme('ocean')
um.header('Comprehensive Component Test Suite')
um.text('Testing all Umara components systematically')

# =============================================================================
# SECTION 1: TYPOGRAPHY
# =============================================================================
um.subheader('1. Typography Components')

with um.card():
    um.header('Header Level 1', level=1)
    um.header('Header Level 2', level=2)
    um.header('Header Level 3', level=3)
    um.subheader('Subheader')
    um.text('Regular text')
    um.text('Colored text', color='#6366f1')
    um.markdown('**Bold**, *italic*, and `code`')
    um.code('print("Hello, World!")', language='python')
    um.caption('This is a caption')

um.divider()

# =============================================================================
# SECTION 2: FEEDBACK COMPONENTS
# =============================================================================
um.subheader('2. Feedback Components')

with um.card():
    um.success('Success message!')
    um.error('Error message!')
    um.warning('Warning message!')
    um.info('Info message!')

um.divider()

# =============================================================================
# SECTION 3: BUTTONS
# =============================================================================
um.subheader('3. Button Components')

with um.card():
    with um.columns(5):
        with um.column():
            if um.button('Primary', key='btn_primary', variant='primary'):
                um.success('Primary clicked!')
        with um.column():
            if um.button('Secondary', key='btn_secondary', variant='secondary'):
                um.success('Secondary clicked!')
        with um.column():
            if um.button('Outline', key='btn_outline', variant='outline'):
                um.success('Outline clicked!')
        with um.column():
            if um.button('Ghost', key='btn_ghost', variant='ghost'):
                um.success('Ghost clicked!')
        with um.column():
            if um.button('Danger', key='btn_danger', variant='danger'):
                um.success('Danger clicked!')

with um.card():
    um.text('Copy Button:')
    um.copy_button('npm install umara', label='Copy command')

    um.text('Download Button:')
    um.download_button(
        label='Download CSV',
        data='Name,Age,City\nAlice,28,NYC\nBob,34,LA',
        file_name='sample.csv',
        mime='text/csv'
    )

    um.text('Link Button:')
    um.link_button('Visit GitHub', url='https://github.com')

um.divider()

# =============================================================================
# SECTION 4: TEXT INPUTS
# =============================================================================
um.subheader('4. Text Input Components')

with um.card():
    text_val = um.input('Text Input', key='text_input', placeholder='Enter text...')
    um.text(f'Text value: {text_val}')

    password_val = um.input('Password Input', key='password_input', type='password')
    um.text(f'Password length: {len(password_val) if password_val else 0}')

    textarea_val = um.text_area('Text Area', key='textarea_input', placeholder='Enter longer text...', rows=3)
    um.text(f'Text area value: {textarea_val[:50] if textarea_val else ""}...')

    search_val = um.search_input('Search...', key='search_input')
    um.text(f'Search value: {search_val}')

um.divider()

# =============================================================================
# SECTION 5: NUMERIC INPUTS
# =============================================================================
um.subheader('5. Numeric Input Components')

with um.card():
    with um.columns(2):
        with um.column():
            slider_val = um.slider('Slider', min_value=0, max_value=100, value=50, key='slider_input')
            um.text(f'Slider value: {slider_val}')

        with um.column():
            number_val = um.number_input('Number Input', min_value=0, max_value=100, value=25, key='number_input')
            um.text(f'Number value: {number_val}')

um.divider()

# =============================================================================
# SECTION 6: SELECTION INPUTS
# =============================================================================
um.subheader('6. Selection Input Components')

with um.card():
    select_val = um.select('Select', options=['Option A', 'Option B', 'Option C'], key='select_input')
    um.text(f'Selected: {select_val}')

    multi_val = um.multiselect('Multiselect', options=['Apple', 'Banana', 'Cherry', 'Date'], default=['Apple'], key='multiselect_input')
    um.text(f'Multi-selected: {", ".join(multi_val) if multi_val else "None"}')

    radio_val = um.radio('Radio', options=['Small', 'Medium', 'Large'], key='radio_input')
    um.text(f'Radio value: {radio_val}')

    radio_h_val = um.radio('Horizontal Radio', options=['S', 'M', 'L', 'XL'], key='radio_h_input', horizontal=True)
    um.text(f'Horizontal radio: {radio_h_val}')

um.divider()

# =============================================================================
# SECTION 7: TOGGLE INPUTS
# =============================================================================
um.subheader('7. Toggle Input Components')

with um.card():
    with um.columns(2):
        with um.column():
            checkbox_val = um.checkbox('Checkbox', key='checkbox_input')
            um.text(f'Checkbox: {checkbox_val}')

        with um.column():
            toggle_val = um.toggle('Toggle Switch', key='toggle_input')
            um.text(f'Toggle: {toggle_val}')

um.divider()

# =============================================================================
# SECTION 8: DATE/TIME INPUTS
# =============================================================================
um.subheader('8. Date/Time Input Components')

with um.card():
    with um.columns(3):
        with um.column():
            date_val = um.date_input('Date Input', key='date_input')
            um.text(f'Date: {date_val}')

        with um.column():
            time_val = um.time_input('Time Input', key='time_input')
            um.text(f'Time: {time_val}')

        with um.column():
            color_val = um.color_picker('Color Picker', value='#3b82f6', key='color_input')
            um.text(f'Color: {color_val}')

um.divider()

# =============================================================================
# SECTION 9: SPECIAL INPUTS
# =============================================================================
um.subheader('9. Special Input Components')

with um.card():
    rating_val = um.rating('Rating', max_value=5, value=3, key='rating_input')
    um.text(f'Rating: {rating_val}/5 stars')

    pills_val = um.pills('Pills Filter', options=['All', 'Active', 'Completed', 'Archived'], key='pills_input')
    um.text(f'Selected pill: {pills_val}')

um.divider()

# =============================================================================
# SECTION 10: LAYOUT COMPONENTS
# =============================================================================
um.subheader('10. Layout Components')

with um.card():
    um.text('Columns Layout:')
    with um.columns(3):
        with um.column():
            um.text('Column 1')
        with um.column():
            um.text('Column 2')
        with um.column():
            um.text('Column 3')

with um.card():
    um.text('Grid Layout:')
    with um.grid(columns=4, gap='8px'):
        for i in range(8):
            with um.card():
                um.text(f'Grid {i+1}')

um.divider()

# =============================================================================
# SECTION 11: TABS
# =============================================================================
um.subheader('11. Tabs Component')

with um.card():
    with um.tabs(['Tab A', 'Tab B', 'Tab C'], key='test_tabs'):
        with um.tab(0):
            um.text('Content for Tab A')
            tab_a_input = um.input('Input in Tab A', key='tab_a_input')
            um.text(f'Tab A input: {tab_a_input}')

        with um.tab(1):
            um.text('Content for Tab B')
            if um.button('Button in Tab B', key='tab_b_btn'):
                um.success('Tab B button clicked!')

        with um.tab(2):
            um.text('Content for Tab C')

um.divider()

# =============================================================================
# SECTION 12: EXPANDER
# =============================================================================
um.subheader('12. Expander Component')

with um.card():
    with um.expander('Click to expand', expanded=False):
        um.text('This content is inside the expander')
        expand_input = um.input('Input inside expander', key='expand_input')
        um.text(f'You typed: {expand_input}')

um.divider()

# =============================================================================
# SECTION 13: MODAL
# =============================================================================
um.subheader('13. Modal Component')

with um.card():
    if um.button('Open Modal', key='open_modal_btn'):
        um.open_modal('test_modal')

    with um.modal('Test Modal', key='test_modal'):
        um.text('This is modal content!')
        modal_input = um.input('Input in modal', key='modal_input')
        um.text(f'Modal input: {modal_input}')

um.divider()

# =============================================================================
# SECTION 14: DATA DISPLAY - METRICS
# =============================================================================
um.subheader('14. Metric Components')

with um.card():
    with um.columns(4):
        with um.column():
            um.metric('Revenue', '$12,345', delta=5.2)
        with um.column():
            um.metric('Users', '1,234', delta=-2.1)
        with um.column():
            um.metric('Orders', '567', delta=0)
        with um.column():
            um.metric('Conversion', '3.24%')

with um.card():
    um.text('Stat Cards:')
    with um.columns(3):
        with um.column():
            um.stat_card(
                title='Total Revenue',
                value='$45,231',
                trend=12.5,
                trend_label='vs last month'
            )
        with um.column():
            um.stat_card(
                title='Active Users',
                value='2,345',
                trend=-3.2,
                trend_label='vs last week'
            )
        with um.column():
            um.stat_card(
                title='Orders',
                value='1,234',
                trend=8.1,
                trend_label='vs yesterday'
            )

um.divider()

# =============================================================================
# SECTION 15: PROGRESS & SPINNER
# =============================================================================
um.subheader('15. Progress & Spinner')

with um.card():
    progress_val = um.slider('Set progress', min_value=0, max_value=100, value=65, key='progress_slider')
    um.progress(progress_val, label=f'{int(progress_val)}% Complete')

with um.card():
    um.text('Spinner:')
    with um.spinner('Loading data...'):
        um.text('Content while loading')

um.divider()

# =============================================================================
# SECTION 16: DATA TABLE
# =============================================================================
um.subheader('16. Data Table / Dataframe')

with um.card():
    sample_data = [
        {'Name': 'Alice', 'Age': 28, 'City': 'New York', 'Score': 95},
        {'Name': 'Bob', 'Age': 34, 'City': 'Los Angeles', 'Score': 87},
        {'Name': 'Charlie', 'Age': 22, 'City': 'Chicago', 'Score': 92},
        {'Name': 'Diana', 'Age': 31, 'City': 'Houston', 'Score': 88},
        {'Name': 'Eve', 'Age': 27, 'City': 'Phoenix', 'Score': 91},
    ]
    um.dataframe(sample_data)

um.divider()

# =============================================================================
# SECTION 17: JSON VIEWER
# =============================================================================
um.subheader('17. JSON Viewer')

with um.card():
    sample_json = {
        'user': {
            'name': 'John Doe',
            'email': 'john@example.com',
            'preferences': {
                'theme': 'dark',
                'notifications': True
            }
        },
        'items': ['apple', 'banana', 'cherry'],
        'count': 42
    }
    um.json_viewer(sample_json)

um.divider()

# =============================================================================
# SECTION 18: BADGES
# =============================================================================
um.subheader('18. Badge Components')

with um.card():
    with um.columns(5):
        with um.column():
            um.badge('Default', variant='default')
        with um.column():
            um.badge('Success', variant='success')
        with um.column():
            um.badge('Warning', variant='warning')
        with um.column():
            um.badge('Error', variant='error')
        with um.column():
            um.badge('Info', variant='info')

um.divider()

# =============================================================================
# SECTION 19: AVATARS
# =============================================================================
um.subheader('19. Avatar Components')

with um.card():
    with um.columns(4):
        with um.column():
            um.avatar(name='John Doe', size='sm')
            um.text('Small')
        with um.column():
            um.avatar(name='Jane Smith', size='md')
            um.text('Medium')
        with um.column():
            um.avatar(name='Bob Wilson', size='lg')
            um.text('Large')
        with um.column():
            um.avatar(name='Alice Brown', size='xl')
            um.text('XL')

um.divider()

# =============================================================================
# SECTION 20: NAVIGATION - BREADCRUMBS
# =============================================================================
um.subheader('20. Breadcrumbs')

with um.card():
    um.breadcrumbs([
        {'label': 'Home', 'href': '#'},
        {'label': 'Products', 'href': '#'},
        {'label': 'Electronics', 'href': '#'},
        {'label': 'Laptops'},
    ])

um.divider()

# =============================================================================
# SECTION 21: NAVIGATION - STEPS
# =============================================================================
um.subheader('21. Steps Indicator')

with um.card():
    current_step = um.slider('Current step', min_value=0, max_value=3, value=1, key='step_slider')
    um.steps(['Account', 'Profile', 'Review', 'Complete'], current=int(current_step))

um.divider()

# =============================================================================
# SECTION 22: NAVIGATION - PAGINATION
# =============================================================================
um.subheader('22. Pagination')

with um.card():
    page = um.pagination(total_pages=10, current_page=1, key='pagination_test')
    um.text(f'Current page: {page}')

um.divider()

# =============================================================================
# SECTION 23: EMPTY STATE
# =============================================================================
um.subheader('23. Empty State')

with um.card():
    um.empty_state(
        title='No results found',
        description='Try adjusting your search or filters to find what you\'re looking for.',
        icon='search'
    )

um.divider()

# =============================================================================
# SECTION 24: HTML EMBED
# =============================================================================
um.subheader('24. HTML Embed')

with um.card():
    um.html('''
        <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white; text-align: center;">
            <h3 style="margin: 0 0 10px 0;">Custom HTML Content</h3>
            <p style="margin: 0;">This is embedded HTML with custom styling!</p>
        </div>
    ''')

um.divider()

# =============================================================================
# SECTION 25: FORMS
# =============================================================================
um.subheader('25. Form Component')

with um.card():
    with um.form('test_form'):
        form_name = um.input('Name')
        form_email = um.input('Email', type='email')
        form_message = um.text_area('Message', rows=3)

        if um.form_submit_button('Submit Form'):
            if form_name and form_email:
                um.success(f'Form submitted! Name: {form_name}, Email: {form_email}')
            else:
                um.error('Please fill in all fields')

um.divider()

# =============================================================================
# DEBUG: Session State
# =============================================================================
um.subheader('Debug: Current Session State')
um.code(str(um.session_state.to_dict()), language='python')
