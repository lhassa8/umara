"""
Interactive test to verify actual data flow in Umara.
Tests: form submission, state management, button clicks, input persistence.
"""

import umara as um

um.set_theme('ocean')
um.header('Interactive Data Flow Test')

# =============================================================================
# TEST 1: Form Submission - verify data is captured
# =============================================================================
um.subheader('Test 1: Form Submission')

with um.card(title='Contact Form'):
    with um.form('contact_form'):
        name = um.input('Your Name', placeholder='Enter name...')
        email = um.input('Email', placeholder='email@example.com', type='email')
        message = um.text_area('Message', placeholder='Type message...')

        if um.form_submit_button('Submit'):
            # Log to console for verification
            print(f"[FORM SUBMITTED] name={name!r}, email={email!r}, message={message!r}")

            if name and email:
                um.success(f'Form received! Name: {name}, Email: {email}')
                # Store in session state to verify persistence
                um.session_state['last_submission'] = {
                    'name': name,
                    'email': email,
                    'message': message
                }
            else:
                um.error('Please fill in name and email')

# Show last submission if exists
if um.session_state.get('last_submission'):
    um.info(f"Last submission stored: {um.session_state['last_submission']}")

um.divider()

# =============================================================================
# TEST 2: State Management - counter
# =============================================================================
um.subheader('Test 2: State Management (Counter)')

um.session_state.setdefault('counter', 0)

with um.card():
    # Handle button clicks FIRST (immediate-mode pattern)
    with um.columns(3):
        with um.column():
            inc_clicked = um.button('Increment (+1)', key='inc')
        with um.column():
            dec_clicked = um.button('Decrement (-1)', variant='secondary', key='dec')
        with um.column():
            reset_clicked = um.button('Reset', variant='outline', key='reset')

    # Process state changes
    if inc_clicked:
        um.session_state.counter += 1
        print(f"[COUNTER] Incremented to {um.session_state.counter}")
    if dec_clicked:
        um.session_state.counter -= 1
        print(f"[COUNTER] Decremented to {um.session_state.counter}")
    if reset_clicked:
        um.session_state.counter = 0
        print(f"[COUNTER] Reset to 0")

    # Display AFTER state changes for accurate value
    um.text(f'Counter value: **{um.session_state.counter}**')

um.divider()

# =============================================================================
# TEST 3: Real-time Input Updates
# =============================================================================
um.subheader('Test 3: Real-time Input (with key)')

with um.card():
    search_term = um.input('Type something (updates live)', key='live_search')
    um.text(f'You typed: "{search_term}"')
    um.text(f'Length: {len(search_term)} characters')

um.divider()

# =============================================================================
# TEST 4: Select and Radio persistence
# =============================================================================
um.subheader('Test 4: Select/Radio State')

with um.card():
    with um.columns(2):
        with um.column():
            color = um.select('Favorite Color',
                            options=['Red', 'Green', 'Blue', 'Yellow'],
                            key='fav_color')
            um.text(f'Selected color: {color}')

        with um.column():
            size = um.radio('Size',
                          options=['S', 'M', 'L', 'XL'],
                          key='size_choice',
                          horizontal=True)
            um.text(f'Selected size: {size}')

um.divider()

# =============================================================================
# TEST 5: Toggle/Checkbox state
# =============================================================================
um.subheader('Test 5: Toggle/Checkbox State')

with um.card():
    with um.columns(2):
        with um.column():
            dark_mode = um.toggle('Dark Mode', key='dark_toggle')
            um.text(f'Dark mode: {"ON" if dark_mode else "OFF"}')

        with um.column():
            agree = um.checkbox('I agree to terms', key='agree_check')
            um.text(f'Agreed: {"Yes" if agree else "No"}')

um.divider()

# =============================================================================
# TEST 6: Slider state
# =============================================================================
um.subheader('Test 6: Slider State')

with um.card():
    volume = um.slider('Volume', min_value=0, max_value=100, value=50, key='volume_slider')
    um.progress(volume, label=f'Volume: {volume}%')

um.divider()

# =============================================================================
# Debug: Show all session state
# =============================================================================
um.subheader('Debug: Current Session State')
um.code(str(um.session_state.to_dict()), language='python')
