"""
Advanced Component Test Suite for Umara
Tests components not covered in test_comprehensive.py
"""

import umara as um

um.set_theme('ocean')
um.header('Advanced Components Test Suite')
um.text('Testing additional Umara components')

# =============================================================================
# SECTION 1: CONTAINER & SPACER
# =============================================================================
um.subheader('1. Container & Spacer')

with um.card():
    um.text('Content before spacer')
    um.spacer(height='32px')
    um.text('Content after 32px spacer')

um.divider()

# =============================================================================
# SECTION 2: SIDEBAR
# =============================================================================
um.subheader('2. Sidebar')

with um.sidebar():
    um.header('Sidebar', level=3)
    um.text('This is sidebar content')
    sidebar_input = um.input('Sidebar Input', key='sidebar_input')
    um.text(f'You typed: {sidebar_input}')
    if um.button('Sidebar Button', key='sidebar_btn'):
        um.success('Sidebar button clicked!')

um.divider()

# =============================================================================
# SECTION 3: ACCORDION
# =============================================================================
um.subheader('3. Accordion')

with um.card():
    # Accordion takes a list of section titles
    with um.accordion(['Section 1', 'Section 2', 'Section 3'], key='test_accordion'):
        um.text('Accordion component with multiple sections')

um.divider()

# =============================================================================
# SECTION 4: TOOLTIP
# =============================================================================
um.subheader('4. Tooltip')

with um.card():
    um.tooltip('Hover over me', text='This is helpful tooltip text!')

um.divider()

# =============================================================================
# SECTION 5: TAG INPUT
# =============================================================================
um.subheader('5. Tag Input')

with um.card():
    tags = um.tag_input('Add tags', key='tags_input', placeholder='Type and press Enter')
    um.text(f'Tags: {", ".join(tags) if tags else "None"}')

um.divider()

# =============================================================================
# SECTION 6: AVATAR GROUP
# =============================================================================
um.subheader('6. Avatar Group')

with um.card():
    um.avatar_group([
        {'name': 'Alice Johnson'},
        {'name': 'Bob Smith'},
        {'name': 'Charlie Brown'},
        {'name': 'Diana Prince'},
        {'name': 'Eve Wilson'},
    ], max_display=3)

um.divider()

# =============================================================================
# SECTION 7: LOADING SKELETON
# =============================================================================
um.subheader('7. Loading Skeleton')

with um.card():
    um.text('Loading skeleton placeholders:')
    um.loading_skeleton(variant='text', lines=3)
    um.loading_skeleton(variant='card', height='100px')
    um.loading_skeleton(variant='avatar')

um.divider()

# =============================================================================
# SECTION 8: TIMELINE
# =============================================================================
um.subheader('8. Timeline')

with um.card():
    um.timeline([
        {'title': 'Project Started', 'description': 'Initial planning phase', 'date': '2024-01-01'},
        {'title': 'Development', 'description': 'Core features implemented', 'date': '2024-02-15'},
        {'title': 'Testing', 'description': 'QA and bug fixes', 'date': '2024-03-01'},
        {'title': 'Launch', 'description': 'Public release', 'date': '2024-04-01'},
    ])

um.divider()

# =============================================================================
# SECTION 9: CHARTS
# =============================================================================
um.subheader('9. Charts')

chart_data = [
    {'month': 'Jan', 'sales': 100, 'profit': 20},
    {'month': 'Feb', 'sales': 150, 'profit': 35},
    {'month': 'Mar', 'sales': 200, 'profit': 50},
    {'month': 'Apr', 'sales': 180, 'profit': 45},
    {'month': 'May', 'sales': 250, 'profit': 70},
]

with um.card():
    um.text('Line Chart:')
    um.line_chart(chart_data, x='month', y='sales')

with um.card():
    um.text('Bar Chart:')
    um.bar_chart(chart_data, x='month', y='sales')

with um.card():
    um.text('Area Chart:')
    um.area_chart(chart_data, x='month', y='sales')

pie_data = [
    {'category': 'Electronics', 'value': 400},
    {'category': 'Clothing', 'value': 300},
    {'category': 'Food', 'value': 200},
    {'category': 'Books', 'value': 100},
]

with um.card():
    um.text('Pie Chart:')
    um.pie_chart(pie_data, label='category', value='value')

um.divider()

# =============================================================================
# SECTION 10: SCATTER CHART
# =============================================================================
um.subheader('10. Scatter Chart')

scatter_data = [
    {'x': 1, 'y': 2, 'size': 10},
    {'x': 2, 'y': 4, 'size': 15},
    {'x': 3, 'y': 3, 'size': 20},
    {'x': 4, 'y': 7, 'size': 12},
    {'x': 5, 'y': 5, 'size': 25},
]

with um.card():
    um.scatter_chart(scatter_data, x='x', y='y')

um.divider()

# =============================================================================
# SECTION 11: TOAST NOTIFICATIONS
# =============================================================================
um.subheader('11. Toast Notifications')

with um.card():
    with um.columns(4):
        with um.column():
            if um.button('Success Toast', key='toast_success'):
                um.toast('Operation successful!', icon='check')
        with um.column():
            if um.button('Error Toast', key='toast_error'):
                um.toast('Something went wrong!', icon='x')
        with um.column():
            if um.button('Warning Toast', key='toast_warning'):
                um.toast('Please be careful!', icon='warning')
        with um.column():
            if um.button('Info Toast', key='toast_info'):
                um.toast('Here is some info', icon='info')

um.divider()

# =============================================================================
# SECTION 12: STATUS INDICATOR
# =============================================================================
um.subheader('12. Status Indicator')

with um.card():
    with um.status('Processing your request...', state='running') as status:
        um.text('Step 1: Initializing...')
        um.text('Step 2: Processing data...')
        um.text('Step 3: Finalizing...')

um.divider()

# =============================================================================
# SECTION 13: SELECT SLIDER
# =============================================================================
um.subheader('13. Select Slider')

with um.card():
    selected_option = um.select_slider(
        'Choose a size',
        options=['XS', 'S', 'M', 'L', 'XL', 'XXL'],
        value='M',
        key='size_slider'
    )
    um.text(f'Selected size: {selected_option}')

um.divider()

# =============================================================================
# SECTION 14: FEEDBACK COMPONENT
# =============================================================================
um.subheader('14. Feedback Component')

with um.card():
    feedback_val = um.feedback({0: 'Bad', 1: 'Okay', 2: 'Good'}, key='feedback_input')
    um.text(f'Feedback value: {feedback_val}')

um.divider()

# =============================================================================
# SECTION 15: SEGMENTED CONTROL
# =============================================================================
um.subheader('15. Segmented Control')

with um.card():
    segment_val = um.segmented_control(
        'View Mode',
        options=['List', 'Grid', 'Table'],
        key='segment_control'
    )
    um.text(f'Selected view: {segment_val}')

um.divider()

# =============================================================================
# SECTION 16: TITLE & CAPTION
# =============================================================================
um.subheader('16. Title & Caption')

with um.card():
    um.title('This is a Title Component')
    um.caption('This is a caption - smaller, muted text')
    um.text('Regular text for comparison')

um.divider()

# =============================================================================
# SECTION 17: WRITE FUNCTION
# =============================================================================
um.subheader('17. Write Function')

with um.card():
    um.write('The write() function can display various types:')
    um.write('A simple string')
    um.write(42)
    um.write(3.14159)
    um.write(['list', 'of', 'items'])
    um.write({'key': 'value', 'number': 123})

um.divider()

# =============================================================================
# SECTION 18: DIALOG (Using Modal)
# =============================================================================
um.subheader('18. Dialog Component')

with um.card():
    if um.button('Open Dialog', key='open_dialog_btn'):
        um.open_modal('test_dialog')

    with um.modal('Confirmation', key='test_dialog'):
        um.text('Are you sure you want to proceed?')
        um.text('This action cannot be undone.')
        if um.button('Close', key='close_dialog_btn'):
            um.close_modal('test_dialog')

um.divider()

# =============================================================================
# SECTION 19: NAV LINK
# =============================================================================
um.subheader('19. Nav Link')

with um.card():
    um.nav_link('Home', icon='home', href='#home')
    um.nav_link('Settings', icon='settings', href='#settings')
    um.nav_link('Profile', icon='user', href='#profile')

um.divider()

# =============================================================================
# SECTION 20: DATA EDITOR
# =============================================================================
um.subheader('20. Data Editor')

with um.card():
    editable_data = [
        {'Name': 'Alice', 'Age': 28, 'Active': True},
        {'Name': 'Bob', 'Age': 34, 'Active': False},
        {'Name': 'Charlie', 'Age': 22, 'Active': True},
    ]
    edited = um.data_editor(editable_data, key='data_editor')
    um.text('Edited data:')
    um.json_viewer(edited)

um.divider()

# =============================================================================
# SECTION 21: POPOVER
# =============================================================================
um.subheader('21. Popover')

with um.card():
    with um.popover('Click for more info'):
        um.text('This is popover content!')
        um.text('It can contain any components.')
        um.button('Button inside popover', key='popover_btn')

um.divider()

# =============================================================================
# SECTION 22: LOGO
# =============================================================================
um.subheader('22. Logo')

with um.card():
    um.text('Logo component (displays app logo):')
    um.logo('https://via.placeholder.com/150x50?text=Logo')

um.divider()

# =============================================================================
# DEBUG: Session State
# =============================================================================
um.subheader('Debug: Current Session State')
um.code(str(um.session_state.to_dict()), language='python')
