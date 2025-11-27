"""
Test data display, media, and additional UI components.
"""

import umara as um

um.set_theme('ocean')
um.header('Data & UI Components Test')

# =============================================================================
# TEST 1: Progress Bar
# =============================================================================
um.subheader('Test 1: Progress Bar')

with um.card():
    progress_val = um.slider('Set progress', 0, 100, 65, key='progress_slider')
    um.progress(progress_val, label=f'{int(progress_val)}% Complete')

um.divider()

# =============================================================================
# TEST 2: Spinner
# =============================================================================
um.subheader('Test 2: Spinner')

with um.card():
    um.text('Spinner component:')
    with um.spinner('Loading data...'):
        um.text('This content appears while loading')

um.divider()

# =============================================================================
# TEST 3: Badge
# =============================================================================
um.subheader('Test 3: Badge')

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
# TEST 4: Avatar
# =============================================================================
um.subheader('Test 4: Avatar')

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
# TEST 5: Dataframe / Table
# =============================================================================
um.subheader('Test 5: Dataframe / Table')

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
# TEST 6: Breadcrumbs
# =============================================================================
um.subheader('Test 6: Breadcrumbs')

with um.card():
    um.breadcrumbs([
        {'label': 'Home', 'href': '#'},
        {'label': 'Products', 'href': '#'},
        {'label': 'Electronics', 'href': '#'},
        {'label': 'Laptops'},
    ])

um.divider()

# =============================================================================
# TEST 7: Steps Indicator
# =============================================================================
um.subheader('Test 7: Steps Indicator')

with um.card():
    current_step = um.slider('Current step', 0, 3, 1, key='step_slider')
    um.steps(['Account', 'Profile', 'Review', 'Complete'], current=int(current_step))

um.divider()

# =============================================================================
# TEST 8: JSON Viewer
# =============================================================================
um.subheader('Test 8: JSON Viewer')

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
# TEST 9: Stat Card
# =============================================================================
um.subheader('Test 9: Stat Card')

with um.card():
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
# TEST 10: Pagination
# =============================================================================
um.subheader('Test 10: Pagination')

with um.card():
    page = um.pagination(total_pages=10, current_page=1, key='pagination_test')
    um.text(f'Current page: {page}')

um.divider()

# =============================================================================
# TEST 11: Empty State
# =============================================================================
um.subheader('Test 11: Empty State')

with um.card():
    um.empty_state(
        title='No results found',
        description='Try adjusting your search or filters to find what you\'re looking for.',
        icon='search'
    )

um.divider()

# =============================================================================
# TEST 12: Copy Button
# =============================================================================
um.subheader('Test 12: Copy Button')

with um.card():
    um.text('Click to copy the text below:')
    um.copy_button('npm install umara', label='Copy install command')

um.divider()

# =============================================================================
# TEST 13: Download Button
# =============================================================================
um.subheader('Test 13: Download Button')

with um.card():
    um.download_button(
        label='Download Sample Data',
        data='Name,Age,City\nAlice,28,NYC\nBob,34,LA',
        file_name='sample.csv',
        mime='text/csv'
    )

um.divider()

# =============================================================================
# TEST 14: HTML Embed
# =============================================================================
um.subheader('Test 14: HTML Embed')

with um.card():
    um.html('''
        <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white; text-align: center;">
            <h3 style="margin: 0 0 10px 0;">Custom HTML Content</h3>
            <p style="margin: 0;">This is embedded HTML with custom styling!</p>
        </div>
    ''')

um.divider()

# =============================================================================
# Debug: Show session state
# =============================================================================
um.subheader('Debug: Current Session State')
um.code(str(um.session_state.to_dict()), language='python')
