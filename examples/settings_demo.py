"""
Umara Settings Demo - Application Settings Page

A comprehensive settings page example demonstrating tabs, forms,
and various input components organized into logical sections.
"""

import umara as um

um.set_theme('light')

# ============================================================================
# Header
# ============================================================================
um.header('Settings')
um.text('Manage your account settings and preferences.', color='#64748b')

um.spacer(height='24px')

# ============================================================================
# Settings Tabs
# ============================================================================
with um.tabs(['Profile', 'Notifications', 'Security', 'Appearance'], key='settings_tabs'):

    # ========================================================================
    # Profile Tab
    # ========================================================================
    with um.tab(0):
        with um.card():
            um.subheader('Personal Information')
            um.text('Update your personal details here.', color='#64748b', size='14px')

            um.spacer(height='20px')

            with um.columns(2):
                with um.column():
                    um.input('First Name', value='John', key='first_name')
                with um.column():
                    um.input('Last Name', value='Doe', key='last_name')

            um.input('Email Address', value='john.doe@example.com', key='email')

            um.text_area(
                'Bio',
                placeholder='Tell us about yourself...',
                rows=3,
                key='bio'
            )

            um.spacer(height='16px')

            with um.columns(2):
                with um.column():
                    um.select(
                        'Country',
                        options=['United States', 'Canada', 'United Kingdom', 'Australia', 'Germany', 'France'],
                        default='United States',
                        key='country'
                    )
                with um.column():
                    um.select(
                        'Timezone',
                        options=['UTC-8 (Pacific)', 'UTC-5 (Eastern)', 'UTC+0 (GMT)', 'UTC+1 (CET)', 'UTC+9 (JST)'],
                        default='UTC-8 (Pacific)',
                        key='timezone'
                    )

        um.spacer(height='24px')

        with um.card():
            um.subheader('Profile Photo')
            um.text('Upload a profile picture.', color='#64748b', size='14px')

            um.spacer(height='16px')

            with um.columns([1, 3]):
                with um.column():
                    um.avatar(name='John Doe', size='80px')
                with um.column():
                    um.file_uploader(
                        'Choose Image',
                        accept=['.png', '.jpg', '.jpeg'],
                        key='avatar_upload'
                    )
                    um.text('PNG, JPG up to 5MB', color='#94a3b8', size='12px')

    # ========================================================================
    # Notifications Tab
    # ========================================================================
    with um.tab(1):
        with um.card():
            um.subheader('Email Notifications')
            um.text('Choose what emails you want to receive.', color='#64748b', size='14px')

            um.spacer(height='20px')

            um.toggle('Marketing emails', value=True, key='notif_marketing')
            um.text('Receive emails about new features and promotions.', color='#94a3b8', size='12px')

            um.spacer(height='16px')

            um.toggle('Product updates', value=True, key='notif_updates')
            um.text('Get notified when we release new features.', color='#94a3b8', size='12px')

            um.spacer(height='16px')

            um.toggle('Security alerts', value=True, key='notif_security')
            um.text('Receive alerts about your account security.', color='#94a3b8', size='12px')

            um.spacer(height='16px')

            um.toggle('Weekly digest', value=False, key='notif_digest')
            um.text('Get a weekly summary of your activity.', color='#94a3b8', size='12px')

        um.spacer(height='24px')

        with um.card():
            um.subheader('Push Notifications')
            um.text('Configure push notification preferences.', color='#64748b', size='14px')

            um.spacer(height='20px')

            um.toggle('Enable push notifications', value=True, key='push_enabled')

            um.spacer(height='16px')

            um.select(
                'Notification Sound',
                options=['Default', 'Chime', 'Bell', 'None'],
                default='Default',
                key='notif_sound'
            )

            um.spacer(height='12px')

            um.checkbox('Show preview in notifications', value=True, key='show_preview')
            um.checkbox('Group notifications', value=True, key='group_notif')

    # ========================================================================
    # Security Tab
    # ========================================================================
    with um.tab(2):
        with um.card():
            um.subheader('Change Password')
            um.text('Update your password regularly to keep your account secure.', color='#64748b', size='14px')

            um.spacer(height='20px')

            um.input('Current Password', placeholder='Enter current password', key='current_pass')
            um.input('New Password', placeholder='Enter new password', key='new_pass')
            um.input('Confirm New Password', placeholder='Confirm new password', key='confirm_pass')

            um.spacer(height='12px')

            um.progress(60, label='Password Strength: Medium')

            um.spacer(height='16px')

            if um.button('Update Password', variant='primary', key='update_pass'):
                um.success('Password updated successfully!')

        um.spacer(height='24px')

        with um.card():
            um.subheader('Two-Factor Authentication')
            um.text('Add an extra layer of security to your account.', color='#64748b', size='14px')

            um.spacer(height='20px')

            um.toggle('Enable 2FA', value=False, key='enable_2fa')

            um.spacer(height='16px')

            um.select(
                'Authentication Method',
                options=['Authenticator App', 'SMS', 'Email'],
                default='Authenticator App',
                key='auth_method'
            )

            um.spacer(height='16px')

            um.info('Two-factor authentication adds an extra layer of security by requiring a second form of verification.')

        um.spacer(height='24px')

        with um.card():
            um.subheader('Active Sessions')
            um.text('Manage your active login sessions.', color='#64748b', size='14px')

            um.spacer(height='20px')

            sessions = [
                {'Device': 'MacBook Pro', 'Location': 'San Francisco, CA', 'Last Active': 'Now', 'Status': 'Current'},
                {'Device': 'iPhone 15', 'Location': 'San Francisco, CA', 'Last Active': '2 hours ago', 'Status': 'Active'},
                {'Device': 'Windows PC', 'Location': 'New York, NY', 'Last Active': '3 days ago', 'Status': 'Active'},
            ]

            um.dataframe(sessions)

            um.spacer(height='12px')

            um.button('Sign Out All Other Sessions', variant='danger', key='signout_all')

    # ========================================================================
    # Appearance Tab
    # ========================================================================
    with um.tab(3):
        with um.card():
            um.subheader('Theme')
            um.text('Customize how the application looks.', color='#64748b', size='14px')

            um.spacer(height='20px')

            theme = um.select(
                'Color Theme',
                options=['light', 'dark', 'ocean', 'forest', 'slate', 'nord', 'midnight', 'rose'],
                default='light',
                key='theme_select'
            )

            # Apply the selected theme
            um.set_theme(theme)

            um.spacer(height='16px')

            um.toggle('Use system theme', value=False, key='system_theme')
            um.text('Automatically switch between light and dark themes based on your system settings.', color='#94a3b8', size='12px')

        um.spacer(height='24px')

        with um.card():
            um.subheader('Display')
            um.text('Adjust display settings.', color='#64748b', size='14px')

            um.spacer(height='20px')

            um.slider('Font Size', min_value=12, max_value=20, value=14, key='font_size')

            um.spacer(height='16px')

            um.select(
                'Density',
                options=[
                    {'value': 'compact', 'label': 'Compact'},
                    {'value': 'comfortable', 'label': 'Comfortable'},
                    {'value': 'spacious', 'label': 'Spacious'},
                ],
                default='comfortable',
                key='density'
            )

            um.spacer(height='16px')

            um.checkbox('Show sidebar by default', value=True, key='show_sidebar')
            um.checkbox('Enable animations', value=True, key='enable_animations')
            um.checkbox('Reduce motion', value=False, key='reduce_motion')

        um.spacer(height='24px')

        with um.card():
            um.subheader('Accessibility')
            um.text('Make the app easier to use.', color='#64748b', size='14px')

            um.spacer(height='20px')

            um.toggle('High contrast mode', value=False, key='high_contrast')
            um.spacer(height='12px')
            um.toggle('Larger click targets', value=False, key='large_targets')
            um.spacer(height='12px')
            um.toggle('Screen reader optimizations', value=False, key='screen_reader')

um.spacer(height='32px')

# ============================================================================
# Action Buttons
# ============================================================================
um.divider()
um.spacer(height='16px')

with um.columns([3, 1, 1]):
    with um.column():
        um.text('Changes are saved automatically.', color='#94a3b8', size='12px')
    with um.column():
        um.button('Cancel', variant='ghost', key='cancel')
    with um.column():
        if um.button('Save Changes', variant='primary', key='save'):
            um.success('Settings saved successfully!')

um.spacer(height='24px')

# ============================================================================
# Footer
# ============================================================================
um.text('Settings Demo - Umara v0.5.0', color='#94a3b8', size='12px')
