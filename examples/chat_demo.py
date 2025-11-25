"""
Umara Chat Demo - AI Chatbot Interface

Demonstrates the chat components for building AI chatbot interfaces.
"""

import umara as um

um.set_theme('dark')

# ============================================================================
# Header Section
# ============================================================================
um.header('AI Chat Assistant')
um.text('A beautiful chat interface built with Umara', color='#64748b')

um.divider()

# ============================================================================
# Simple Chat Interface
# ============================================================================
um.subheader('Simple Chat')

# Initialize chat messages in state
if 'messages' not in um.session_state:
    um.session_state['messages'] = [
        {'role': 'assistant', 'content': 'Hello! I\'m your AI assistant. How can I help you today?'},
    ]

# Display the chat widget
message = um.chat(
    um.session_state['messages'],
    key='main_chat',
    height='400px',
    input_placeholder='Ask me anything...',
)

# Handle new messages
if message:
    # Add user message
    um.session_state['messages'].append({'role': 'user', 'content': message})

    # Simulate AI response (in real app, call your AI API here)
    responses = [
        "That's a great question! Let me think about that...",
        "I understand. Here's what I can tell you...",
        "Interesting! Based on what you've said...",
        "Thanks for sharing. Here are my thoughts...",
    ]
    import random
    ai_response = random.choice(responses)
    um.session_state['messages'].append({'role': 'assistant', 'content': ai_response})

um.divider()

# ============================================================================
# Manual Chat Building
# ============================================================================
um.subheader('Custom Chat Layout')
um.text('Build your own chat layout with individual components', color='#64748b')

with um.chat_container(height='300px', key='custom_chat'):
    um.chat_message('user', 'How do I create a dashboard?')
    um.chat_message('assistant', 'Creating dashboards with Umara is easy! Use the `columns` and `metric` components.')
    um.chat_message('user', 'Can you show me an example?')
    um.chat_message('assistant', 'Sure! Here\'s a quick example:\n\n```python\nwith um.columns(3):\n    um.metric("Users", "1,234")\n    um.metric("Revenue", "$48K")\n```')

um.chat_input('Type your message...', key='custom_input')

um.divider()

# ============================================================================
# Chat with Context
# ============================================================================
um.subheader('Chat with System Context')

with um.card():
    um.text('System Prompt:', color='#64748b', size='14px')
    system_prompt = um.text_area(
        '',
        placeholder='You are a helpful assistant...',
        rows=3,
        key='system_prompt'
    )

    um.spacer(height='12px')

    with um.columns(2):
        with um.column():
            model = um.select(
                'Model',
                options=['GPT-4', 'GPT-3.5', 'Claude', 'Llama'],
                key='model_select'
            )
        with um.column():
            temp = um.slider('Temperature', 0.0, 2.0, 0.7, key='temp_slider')

    if um.button('Start New Chat', variant='primary', key='new_chat_btn'):
        um.success('New chat started with your configuration!')

um.divider()

# ============================================================================
# Footer
# ============================================================================
um.text('Chat Demo - Umara v0.2.0', color='#64748b', size='12px')
