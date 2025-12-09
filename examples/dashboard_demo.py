"""
Umara Dashboard Demo - Analytics Dashboard

A realistic analytics dashboard example demonstrating sidebar navigation,
metrics, charts, and data tables.
"""

import umara as um

um.set_theme('light')

# ============================================================================
# Sidebar Navigation
# ============================================================================
with um.sidebar(width='260px'):
    um.subheader('Acme Analytics')
    um.spacer(height='8px')
    um.text('Dashboard', color='#64748b', size='12px')

    um.spacer(height='16px')

    um.nav_link('Overview', icon='📊', active=True, key='nav_overview')
    um.nav_link('Sales', icon='💰', key='nav_sales')
    um.nav_link('Customers', icon='👥', key='nav_customers')
    um.nav_link('Products', icon='📦', key='nav_products')
    um.nav_link('Reports', icon='📈', key='nav_reports')

    um.spacer(height='24px')
    um.divider()
    um.spacer(height='16px')

    um.text('Settings', color='#64748b', size='12px')
    um.spacer(height='12px')
    um.nav_link('Preferences', icon='⚙️', key='nav_prefs')
    um.nav_link('Team', icon='🏢', key='nav_team')
    um.nav_link('Billing', icon='💳', key='nav_billing')

# ============================================================================
# Main Content - Header
# ============================================================================
um.header('Dashboard Overview')
um.text('Welcome back! Here\'s what\'s happening with your business.', color='#64748b')

um.spacer(height='24px')

# ============================================================================
# Quick Stats
# ============================================================================
with um.columns(4):
    with um.column():
        um.stat_card('Total Revenue', '$124,500', trend=12.5, icon='💰')
    with um.column():
        um.stat_card('Active Users', '8,432', trend=8.2, icon='👥')
    with um.column():
        um.stat_card('Orders', '1,253', trend=-2.4, icon='📦')
    with um.column():
        um.stat_card('Conversion', '3.24%', trend=0.8, icon='📈')

um.spacer(height='32px')

# ============================================================================
# Charts Section
# ============================================================================
um.subheader('Performance Overview')

# Revenue data for charts
revenue_data = [
    {'month': 'Jan', 'revenue': 42000, 'orders': 320},
    {'month': 'Feb', 'revenue': 48000, 'orders': 380},
    {'month': 'Mar', 'revenue': 55000, 'orders': 420},
    {'month': 'Apr', 'revenue': 51000, 'orders': 390},
    {'month': 'May', 'revenue': 62000, 'orders': 480},
    {'month': 'Jun', 'revenue': 71000, 'orders': 520},
    {'month': 'Jul', 'revenue': 78000, 'orders': 580},
]

# Sales by category
category_data = [
    {'category': 'Electronics', 'sales': 45000},
    {'category': 'Clothing', 'sales': 32000},
    {'category': 'Home & Garden', 'sales': 28000},
    {'category': 'Sports', 'sales': 19500},
]

with um.columns(2):
    with um.column():
        with um.card():
            um.line_chart(
                revenue_data,
                x='month',
                y=['revenue', 'orders'],
                title='Revenue & Orders Trend',
                height='280px'
            )
    with um.column():
        with um.card():
            um.bar_chart(
                category_data,
                x='category',
                y='sales',
                title='Sales by Category',
                height='280px'
            )

um.spacer(height='32px')

# ============================================================================
# Recent Activity & Quick Actions
# ============================================================================
with um.columns([2, 1]):
    with um.column():
        um.subheader('Recent Orders')

        orders = [
            {'Order ID': '#ORD-7821', 'Customer': 'Alice Johnson', 'Product': 'Wireless Headphones', 'Amount': '$129.99', 'Status': 'Completed'},
            {'Order ID': '#ORD-7820', 'Customer': 'Bob Smith', 'Product': 'Smart Watch', 'Amount': '$299.00', 'Status': 'Processing'},
            {'Order ID': '#ORD-7819', 'Customer': 'Carol White', 'Product': 'Laptop Stand', 'Amount': '$49.99', 'Status': 'Completed'},
            {'Order ID': '#ORD-7818', 'Customer': 'David Lee', 'Product': 'USB-C Hub', 'Amount': '$79.99', 'Status': 'Shipped'},
            {'Order ID': '#ORD-7817', 'Customer': 'Eva Martinez', 'Product': 'Mechanical Keyboard', 'Amount': '$149.99', 'Status': 'Completed'},
        ]

        um.dataframe(orders)

        um.spacer(height='12px')

        with um.columns(3):
            with um.column():
                um.button('View All Orders', variant='outline', key='view_orders')
            with um.column():
                um.button('Export CSV', variant='ghost', key='export_csv')
            with um.column():
                pass

    with um.column():
        um.subheader('Quick Actions')

        with um.card():
            um.button('Create New Order', variant='primary', key='new_order')
            um.spacer(height='8px')
            um.button('Add Product', variant='secondary', key='add_product')
            um.spacer(height='8px')
            um.button('Generate Report', variant='outline', key='gen_report')
            um.spacer(height='8px')
            um.button('Send Notification', variant='ghost', key='send_notif')

        um.spacer(height='16px')

        um.subheader('System Status')
        with um.card():
            um.progress(92, label='Server Load')
            um.spacer(height='8px')
            um.progress(78, label='Memory Usage')
            um.spacer(height='8px')
            um.progress(45, label='Storage')

um.spacer(height='32px')

# ============================================================================
# Traffic Sources
# ============================================================================
um.subheader('Traffic Sources')

traffic_data = [
    {'name': 'Direct', 'share': 35},
    {'name': 'Organic Search', 'share': 30},
    {'name': 'Social Media', 'share': 20},
    {'name': 'Referral', 'share': 15},
]

with um.columns([1, 2]):
    with um.column():
        um.pie_chart(
            traffic_data,
            label='name',
            value='share',
            title='Traffic Distribution',
            height='250px'
        )
    with um.column():
        with um.card():
            um.subheader('Traffic Insights')
            um.spacer(height='12px')
            um.text('Direct traffic continues to be your strongest channel, indicating good brand recognition.', color='#64748b', size='14px')
            um.spacer(height='12px')
            um.text('Consider investing more in social media campaigns to grow that channel.', color='#64748b', size='14px')
            um.spacer(height='16px')

            with um.columns(2):
                with um.column():
                    um.metric('Avg. Session', '4m 32s', delta=12.3)
                with um.column():
                    um.metric('Bounce Rate', '42.1%', delta=-5.2)

um.spacer(height='32px')
um.divider()

# ============================================================================
# Footer
# ============================================================================
um.spacer(height='16px')
um.text('Dashboard Demo - Umara v0.5.1', color='#94a3b8', size='12px')
