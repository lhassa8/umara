"""
Umara Demo Application

This example showcases the key features of the Umara framework,
demonstrating beautiful UI components with minimal code.
"""

import umara as um

# Set the theme - try 'light', 'dark', 'ocean', or 'forest'
um.set_theme('light')

# ============================================================================
# Header Section
# ============================================================================

um.header('Welcome to Umara')
um.text(
    'Build beautiful, modern web UIs with pure Python. '
    'No HTML, CSS, or JavaScript required.'
)

um.divider()

# ============================================================================
# Interactive Demo Section
# ============================================================================

with um.card():
    um.subheader('Interactive Demo')
    um.text('Try out these interactive widgets:', color='#64748b')

    # Two-column layout for form inputs
    with um.columns(2):
        with um.column():
            name = um.input(
                'Your Name',
                placeholder='Enter your name...',
                key='demo_name'
            )
            age = um.slider('Age', 0, 100, 25, key='demo_age')

        with um.column():
            color = um.select(
                'Favorite Color',
                options=['Red', 'Green', 'Blue', 'Purple', 'Orange'],
                default='Blue',
                key='demo_color'
            )
            framework = um.select(
                'Preferred Framework',
                options=[
                    {'value': 'umara', 'label': 'Umara (Best!)'},
                    {'value': 'streamlit', 'label': 'Streamlit'},
                    {'value': 'gradio', 'label': 'Gradio'},
                    {'value': 'panel', 'label': 'Panel'},
                ],
                default='umara',
                key='demo_framework'
            )

    # Checkboxes
    subscribe = um.checkbox('Subscribe to newsletter', key='demo_subscribe')
    notifications = um.toggle('Enable notifications', key='demo_notifications')

    um.spacer('16px')

    # Button with action
    if um.button('Say Hello!', variant='primary'):
        if name:
            um.success(f'Hello, {name}! You are {age} years old and love {color}.')
            if subscribe:
                um.info('Thanks for subscribing to our newsletter!')
        else:
            um.warning('Please enter your name first!')

# ============================================================================
# Metrics Dashboard
# ============================================================================

um.subheader('Dashboard Metrics')
um.text('Real-time metrics displayed beautifully.', color='#64748b')

with um.columns(4):
    with um.column():
        with um.card():
            um.metric('Total Users', '12,543', delta=12.5, delta_label='vs last month')

    with um.column():
        with um.card():
            um.metric('Revenue', '$48.2K', delta=8.2, delta_label='vs last month')

    with um.column():
        with um.card():
            um.metric('Active Sessions', '1,892', delta=-2.4, delta_label='vs yesterday')

    with um.column():
        with um.card():
            um.metric('Conversion Rate', '3.24%', delta=0.5, delta_label='vs last week')

# ============================================================================
# Data Table
# ============================================================================

um.subheader('Data Display')

# Sample data
sample_data = [
    {'Name': 'Alice Johnson', 'Role': 'Engineer', 'Department': 'Engineering', 'Status': 'Active'},
    {'Name': 'Bob Smith', 'Role': 'Designer', 'Department': 'Design', 'Status': 'Active'},
    {'Name': 'Carol Williams', 'Role': 'Manager', 'Department': 'Operations', 'Status': 'Active'},
    {'Name': 'David Brown', 'Role': 'Analyst', 'Department': 'Finance', 'Status': 'On Leave'},
    {'Name': 'Eva Martinez', 'Role': 'Developer', 'Department': 'Engineering', 'Status': 'Active'},
]

um.dataframe(sample_data)

# ============================================================================
# Progress Indicators
# ============================================================================

um.subheader('Progress Indicators')

with um.columns(2):
    with um.column():
        um.progress(75, label='Project Completion')
        um.progress(45, label='Budget Used')
        um.progress(90, label='Customer Satisfaction')

    with um.column():
        with um.card():
            um.text('Progress bars adapt to your theme colors automatically.')
            um.text(
                'They animate smoothly when values change.',
                color='#64748b',
                size='14px'
            )

# ============================================================================
# Theme Showcase
# ============================================================================

um.subheader('Theme System')
um.text('Umara comes with beautiful built-in themes. Switch themes instantly!')

theme = um.select(
    'Select Theme',
    options=['light', 'dark', 'ocean', 'forest'],
    default='light',
    key='theme_select'
)

# Apply selected theme
um.set_theme(theme)

with um.card():
    um.text(f'Currently using the "{theme}" theme.')
    um.text(
        'Themes include coordinated colors, shadows, and typography. '
        'All components automatically adapt to the selected theme.',
        color='#64748b',
        size='14px'
    )

# ============================================================================
# Alert Messages
# ============================================================================

um.subheader('Feedback Components')

with um.columns(2):
    with um.column():
        um.success('Operation completed successfully!')
        um.info('Here is some helpful information.')

    with um.column():
        um.warning('Please review before continuing.')
        um.error('An error occurred. Please try again.')

# ============================================================================
# Button Variants
# ============================================================================

um.subheader('Button Variants')

with um.container():
    um.text('Buttons come in multiple variants for different contexts:', color='#64748b')

    um.spacer('12px')

    # Show all button variants in a row
    with um.columns(5):
        with um.column():
            um.button('Primary', variant='primary', key='btn_primary')
        with um.column():
            um.button('Secondary', variant='secondary', key='btn_secondary')
        with um.column():
            um.button('Outline', variant='outline', key='btn_outline')
        with um.column():
            um.button('Ghost', variant='ghost', key='btn_ghost')
        with um.column():
            um.button('Danger', variant='danger', key='btn_danger')

# ============================================================================
# Footer
# ============================================================================

um.divider()

um.text(
    'Built with Umara - Beautiful Python UIs',
    color='#94a3b8',
    size='14px'
)
um.text(
    'Star us on GitHub: github.com/umara-framework/umara',
    color='#94a3b8',
    size='12px'
)
