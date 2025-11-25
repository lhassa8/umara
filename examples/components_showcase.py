"""
Umara Components Showcase

Demonstrates all available components in the Umara framework.
"""

import umara as um

um.set_theme('light')

# ============================================================================
# Header
# ============================================================================
um.header('Umara Component Showcase')
um.text('Explore all available components in Umara v0.2.0')

um.breadcrumbs([
    {'label': 'Home', 'href': '/'},
    {'label': 'Components', 'href': '/components'},
    {'label': 'Showcase', 'href': '/showcase'},
])

um.divider()

# ============================================================================
# Navigation: Steps
# ============================================================================
um.subheader('Progress Steps')
um.steps(
    ['Select Plan', 'Account Info', 'Payment', 'Confirmation'],
    current_step=1,
    key='onboarding_steps'
)

um.divider()

# ============================================================================
# Stats & Metrics
# ============================================================================
um.subheader('Statistics Cards')

with um.columns(4):
    with um.column():
        um.stat_card('Total Users', '12,543', delta=12.5, icon='👥')
    with um.column():
        um.stat_card('Revenue', '$48.2K', delta=8.2, icon='💰')
    with um.column():
        um.stat_card('Active Sessions', '1,892', delta=-2.4, icon='📊')
    with um.column():
        um.stat_card('Conversion', '3.24%', delta=0.5, icon='📈')

um.divider()

# ============================================================================
# Badges & Avatars
# ============================================================================
um.subheader('Badges')

with um.columns(5):
    with um.column():
        um.badge('Default', variant='default')
    with um.column():
        um.badge('Primary', variant='primary')
    with um.column():
        um.badge('Success', variant='success')
    with um.column():
        um.badge('Warning', variant='warning')
    with um.column():
        um.badge('Error', variant='error')

um.spacer(height='16px')

um.subheader('Avatars')

with um.columns(4):
    with um.column():
        um.avatar(name='Alice Johnson', size='48px')
        um.text('Alice', size='12px')
    with um.column():
        um.avatar(name='Bob Smith', size='48px')
        um.text('Bob', size='12px')
    with um.column():
        um.avatar(name='Carol White', size='48px')
        um.text('Carol', size='12px')
    with um.column():
        um.avatar(name='David Brown', size='48px')
        um.text('David', size='12px')

um.divider()

# ============================================================================
# Input Components
# ============================================================================
um.subheader('Input Components')

with um.card():
    with um.columns(2):
        with um.column():
            um.number_input('Quantity', min=0, max=100, value=1, step=1, key='qty')
            um.date_input('Select Date', key='date')
            um.time_input('Select Time', key='time')
        with um.column():
            um.color_picker('Pick a Color', value='#6366f1', key='color')
            um.rating('Rate this', value=4, max=5, key='rating')

um.divider()

# ============================================================================
# Expandable Sections
# ============================================================================
um.subheader('Expandable Content')

with um.expander('Click to expand details', expanded=False, key='exp1'):
    um.text('This content is hidden by default and can be expanded.')
    um.text('Perfect for FAQs, details, or optional information.')

with um.expander('Another section', expanded=True, key='exp2'):
    um.text('This section starts expanded.')
    um.progress(75, label='Progress inside expander')

um.divider()

# ============================================================================
# Timeline
# ============================================================================
um.subheader('Timeline')

um.timeline([
    {'title': 'Project Started', 'description': 'Initial planning and setup', 'time': 'Jan 1, 2024'},
    {'title': 'Development Phase', 'description': 'Building core features', 'time': 'Feb 15, 2024'},
    {'title': 'Testing', 'description': 'QA and bug fixes', 'time': 'Mar 20, 2024'},
    {'title': 'Launch', 'description': 'Public release!', 'time': 'Apr 1, 2024'},
])

um.divider()

# ============================================================================
# Code Display
# ============================================================================
um.subheader('Code Display')

um.code('''import umara as um

um.set_theme('ocean')
um.header('Hello World')

name = um.input('Your name')
if um.button('Greet'):
    um.success(f'Hello, {name}!')
''', language='python')

um.divider()

# ============================================================================
# JSON Viewer
# ============================================================================
um.subheader('JSON Viewer')

um.json_viewer({
    'name': 'Umara',
    'version': '0.2.0',
    'features': ['chat', 'charts', 'themes'],
    'stats': {
        'components': 50,
        'themes': 4,
        'stars': 1000
    }
})

um.divider()

# ============================================================================
# Charts (Placeholder)
# ============================================================================
um.subheader('Charts')

with um.columns(2):
    with um.column():
        um.line_chart(
            title='Revenue Over Time',
            data=[10, 25, 45, 30, 55, 70],
            height='200px'
        )
    with um.column():
        um.bar_chart(
            title='Sales by Category',
            data=[30, 45, 20, 60],
            height='200px'
        )

with um.columns(2):
    with um.column():
        um.area_chart(
            title='User Growth',
            data=[100, 150, 200, 180, 250],
            height='200px'
        )
    with um.column():
        um.pie_chart(
            title='Market Share',
            data=[40, 30, 20, 10],
            height='200px'
        )

um.divider()

# ============================================================================
# Empty State
# ============================================================================
um.subheader('Empty State')

um.empty_state(
    title='No results found',
    description='Try adjusting your search or filter to find what you\'re looking for.',
    icon='🔍'
)

um.divider()

# ============================================================================
# Loading States
# ============================================================================
um.subheader('Loading Skeleton')

um.loading_skeleton(height='20px', width='60%')
um.loading_skeleton(height='16px', width='80%')
um.loading_skeleton(height='16px', width='40%')

um.divider()

# ============================================================================
# Pagination
# ============================================================================
um.subheader('Pagination')

um.pagination(total_pages=10, current_page=3, key='page')

um.divider()

# ============================================================================
# Theme Switcher
# ============================================================================
um.subheader('Try Different Themes')

theme = um.select(
    'Switch Theme',
    options=['light', 'dark', 'ocean', 'forest'],
    default='light',
    key='theme'
)
um.set_theme(theme)

um.divider()

# ============================================================================
# Footer
# ============================================================================
um.text('Umara v0.2.0 - Component Showcase', color='#64748b', size='12px')
um.text('50+ beautiful components for your Python apps', color='#94a3b8', size='12px')
