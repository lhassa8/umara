"""Simple test to verify button click handling works."""
import umara as um

um.header('Button Click Test')

um.session_state.setdefault('count', 0)

# Handle click FIRST (before display) for correct immediate-mode behavior
clicked = um.button('Click Me', key='test_btn')
if clicked:
    print(f"[BUTTON CLICKED] count was {um.session_state.count}")
    um.session_state.count += 1
    print(f"[BUTTON CLICKED] count is now {um.session_state.count}")

# Display AFTER button logic so it shows updated value
um.text(f'Counter: {um.session_state.count}')

if clicked:
    um.success(f'Button clicked! Count updated to {um.session_state.count}')

um.divider()

um.text('Form test:')
with um.form('test_form'):
    name = um.input('Name', placeholder='Enter your name')
    if um.form_submit_button('Submit'):
        print(f"[FORM SUBMITTED] name={name!r}")
        if name:
            um.success(f'Hello, {name}!')
        else:
            um.error('Please enter your name')

um.divider()
um.text('Debug: Current state:')
um.code(str(um.session_state.to_dict()), language='python')
