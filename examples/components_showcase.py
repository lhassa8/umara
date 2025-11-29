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
um.text('Explore all available components in Umara v0.5.0')

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
    current=1,
    key='onboarding_steps'
)

um.divider()

# ============================================================================
# Stats & Metrics
# ============================================================================
um.subheader('Statistics Cards')

with um.columns(4):
    with um.column():
        um.stat_card('Total Users', '12,543', trend=12.5, icon='👥')
    with um.column():
        um.stat_card('Revenue', '$48.2K', trend=8.2, icon='💰')
    with um.column():
        um.stat_card('Active Sessions', '1,892', trend=-2.4, icon='📊')
    with um.column():
        um.stat_card('Conversion', '3.24%', trend=0.5, icon='📈')

um.divider()

# ============================================================================
# Badges & Avatars
# ============================================================================
um.subheader('Badges')

with um.columns(5):
    with um.column():
        um.badge('Default', variant='default')
    with um.column():
        um.badge('Info', variant='info')
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
            um.number_input('Quantity', min_value=0, max_value=100, value=1, step=1, key='qty')
            um.date_input('Select Date', key='date')
            um.time_input('Select Time', key='time')
        with um.column():
            um.color_picker('Pick a Color', value='#6366f1', key='color')
            um.rating('Rate this', value=4, max_value=5, key='rating')

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
    'version': '0.5.0',
    'features': ['chat', 'charts', 'themes'],
    'stats': {
        'components': 50,
        'themes': 4,
        'stars': 1000
    }
})

um.divider()

# ============================================================================
# Charts
# ============================================================================
um.subheader('Charts')

# Sample data for charts
revenue_data = [
    {'month': 'Jan', 'revenue': 10000, 'profit': 2000},
    {'month': 'Feb', 'revenue': 25000, 'profit': 5000},
    {'month': 'Mar', 'revenue': 45000, 'profit': 12000},
    {'month': 'Apr', 'revenue': 30000, 'profit': 8000},
    {'month': 'May', 'revenue': 55000, 'profit': 15000},
    {'month': 'Jun', 'revenue': 70000, 'profit': 22000},
]

sales_data = [
    {'category': 'Electronics', 'sales': 30000},
    {'category': 'Clothing', 'sales': 45000},
    {'category': 'Food', 'sales': 20000},
    {'category': 'Books', 'sales': 15000},
]

market_data = [
    {'name': 'Product A', 'share': 40},
    {'name': 'Product B', 'share': 30},
    {'name': 'Product C', 'share': 20},
    {'name': 'Product D', 'share': 10},
]

with um.columns(2):
    with um.column():
        um.line_chart(
            revenue_data,
            x='month',
            y=['revenue', 'profit'],
            title='Revenue & Profit Over Time',
            height='250px'
        )
    with um.column():
        um.bar_chart(
            sales_data,
            x='category',
            y='sales',
            title='Sales by Category',
            height='250px'
        )

with um.columns(2):
    with um.column():
        um.area_chart(
            revenue_data,
            x='month',
            y='revenue',
            title='Revenue Trend',
            height='250px'
        )
    with um.column():
        um.pie_chart(
            market_data,
            label='name',
            value='share',
            title='Market Share',
            height='250px'
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

um.loading_skeleton(variant='text', lines=1, height='20px')
um.loading_skeleton(variant='text', lines=1, height='16px')
um.loading_skeleton(variant='text', lines=1, height='16px')

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
um.text('Umara v0.5.0 - Component Showcase', color='#64748b', size='12px')
um.text('50+ beautiful components for your Python apps', color='#94a3b8', size='12px')
