"""
Test additional components not covered in test_interactive.py.
Tests: tabs, expander, modal, number_input, date_input, multiselect, rating, etc.
"""

import umara as um
from datetime import date, time

um.set_theme('ocean')
um.header('Additional Components Test')

# =============================================================================
# TEST 1: Tabs
# =============================================================================
um.subheader('Test 1: Tabs')

with um.tabs(['Tab A', 'Tab B', 'Tab C'], key='main_tabs'):
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
# TEST 2: Expander
# =============================================================================
um.subheader('Test 2: Expander')

with um.expander('Click to expand', expanded=False):
    um.text('This content is inside the expander')
    expand_input = um.input('Input inside expander', key='expand_input')
    um.text(f'You typed: {expand_input}')

um.divider()

# =============================================================================
# TEST 3: Number Input
# =============================================================================
um.subheader('Test 3: Number Input')

with um.card():
    num_val = um.number_input('Enter a number', min_value=0, max_value=100, value=50, key='num_input')
    um.text(f'Number value: {num_val}')
    um.text(f'Doubled: {num_val * 2}')

um.divider()

# =============================================================================
# TEST 4: Date and Time Input
# =============================================================================
um.subheader('Test 4: Date and Time Input')

with um.card():
    with um.columns(2):
        with um.column():
            selected_date = um.date_input('Select a date', key='date_pick')
            um.text(f'Selected date: {selected_date}')

        with um.column():
            selected_time = um.time_input('Select a time', key='time_pick')
            um.text(f'Selected time: {selected_time}')

um.divider()

# =============================================================================
# TEST 5: Multiselect
# =============================================================================
um.subheader('Test 5: Multiselect')

with um.card():
    selected_items = um.multiselect(
        'Select multiple items',
        options=['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
        default=['Apple'],
        key='multi_select'
    )
    um.text(f'Selected: {", ".join(selected_items) if selected_items else "None"}')

um.divider()

# =============================================================================
# TEST 6: Color Picker
# =============================================================================
um.subheader('Test 6: Color Picker')

with um.card():
    color = um.color_picker('Pick a color', value='#3b82f6', key='color_pick')
    um.text(f'Selected color: {color}')

um.divider()

# =============================================================================
# TEST 7: Rating
# =============================================================================
um.subheader('Test 7: Rating')

with um.card():
    rating_val = um.rating('Rate this', max_value=5, value=3, key='rating_input')
    um.text(f'Rating: {rating_val} / 5 stars')

um.divider()

# =============================================================================
# TEST 8: Modal
# =============================================================================
um.subheader('Test 8: Modal')

with um.card():
    if um.button('Open Modal', key='open_modal_btn'):
        um.open_modal('test_modal')

    with um.modal('Test Modal', key='test_modal'):
        um.text('This is modal content!')
        um.text('Click the X button or outside the modal to close.')
        modal_input = um.input('Input in modal', key='modal_input')
        um.text(f'Modal input: {modal_input}')

um.divider()

# =============================================================================
# TEST 9: Metric
# =============================================================================
um.subheader('Test 9: Metric Display')

with um.card():
    with um.columns(3):
        with um.column():
            um.metric('Revenue', '$12,345', delta=5.2)
        with um.column():
            um.metric('Users', '1,234', delta=-2.1)
        with um.column():
            um.metric('Orders', '567', delta=0)

um.divider()

# =============================================================================
# TEST 10: Pills / Segmented Control
# =============================================================================
um.subheader('Test 10: Pills & Segmented Control')

with um.card():
    pill_selection = um.pills(
        'Quick filters',
        options=['All', 'Active', 'Completed', 'Archived'],
        key='pills_select'
    )
    um.text(f'Selected pill: {pill_selection}')

um.divider()

# =============================================================================
# Debug: Show all session state
# =============================================================================
um.subheader('Debug: Current Session State')
um.code(str(um.session_state.to_dict()), language='python')
