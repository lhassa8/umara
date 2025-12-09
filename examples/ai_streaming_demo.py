"""
Umara AI Streaming Demo - Token-by-Token Response Rendering

This is a showcase demo demonstrating Umara's AI-native capabilities:
- Real-time streaming responses (token by token)
- Beautiful chat interface
- Multiple AI model simulation
- System prompt customization

This demo uses simulated responses. For real AI, replace the simulate_stream
function with calls to OpenAI, Anthropic, or other providers.
"""

import time
import random
import umara as um

um.set_theme('dark')

# ============================================================================
# Simulated AI Response Generator
# ============================================================================

def simulate_stream(prompt: str, model: str = "GPT-4"):
    """
    Simulates an AI streaming response.

    In production, replace this with:
    - OpenAI: client.chat.completions.create(stream=True)
    - Anthropic: client.messages.stream()
    - Any other streaming API
    """
    # Sample responses based on common questions
    responses = {
        "hello": "Hello! I'm your AI assistant powered by Umara's streaming capabilities. I can help you with questions, creative writing, coding, analysis, and much more. What would you like to explore today?",

        "umara": """Umara is a beautiful, modern Python framework for creating web UIs. Here's what makes it special:

**Key Features:**
- Pure Python - no HTML/CSS/JS required
- Real-time streaming for AI applications
- 50+ beautiful pre-built components
- WebSocket-based reactive updates
- Multiple themes (light, dark, ocean, forest)

**Example:**
```python
import umara as um

um.header('My App')
name = um.input('Your name')
if um.button('Greet'):
    um.success(f'Hello, {name}!')
```

It's designed from the ground up for AI applications with first-class streaming support!""",

        "code": """Here's a Python function that demonstrates async streaming:

```python
async def stream_response(prompt: str):
    # Initialize the AI client
    client = AsyncAnthropic()

    # Create streaming message
    async with client.messages.stream(
        model="claude-3-5-sonnet",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    ) as stream:
        async for text in stream.text_stream:
            yield text
```

This pattern works beautifully with Umara's `write_stream()` function for real-time token rendering!""",

        "default": """That's a great question! Let me break this down for you.

When working with modern AI applications, there are several key considerations:

1. **Response Streaming** - Users expect real-time feedback, not waiting for complete responses
2. **State Management** - Maintaining conversation context across interactions
3. **UI/UX** - Clean interfaces that feel native and responsive

Umara addresses all of these with its AI-native architecture. The framework was built specifically to handle streaming responses elegantly, making it perfect for chatbots, copilots, and AI-powered tools.

Would you like me to elaborate on any of these points?"""
    }

    # Select appropriate response
    prompt_lower = prompt.lower()
    if "hello" in prompt_lower or "hi" in prompt_lower:
        response = responses["hello"]
    elif "umara" in prompt_lower or "framework" in prompt_lower:
        response = responses["umara"]
    elif "code" in prompt_lower or "python" in prompt_lower or "example" in prompt_lower:
        response = responses["code"]
    else:
        response = responses["default"]

    # Simulate token-by-token streaming
    # Vary speed based on "model"
    delay = 0.02 if model == "GPT-4 Turbo" else 0.03 if model == "GPT-4" else 0.015

    words = response.split(' ')
    for i, word in enumerate(words):
        # Add word with space
        yield word + (' ' if i < len(words) - 1 else '')
        # Simulate network latency with some variance
        time.sleep(delay + random.uniform(0, 0.01))


# ============================================================================
# Sidebar Configuration
# ============================================================================
with um.sidebar(width='280px'):
    um.header('AI Assistant')
    um.text('Powered by Umara Streaming', color='#64748b', size='12px')

    um.spacer(height='24px')
    um.divider()
    um.spacer(height='16px')

    # Model selection
    um.text('Model Configuration', color='#94a3b8', size='12px')
    um.spacer(height='8px')

    model = um.select(
        'Model',
        options=['GPT-4', 'GPT-4 Turbo', 'Claude 3.5', 'Llama 3.1'],
        default='GPT-4',
        key='model'
    )

    um.spacer(height='12px')

    temperature = um.slider(
        'Temperature',
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        key='temperature'
    )

    um.spacer(height='12px')

    max_tokens = um.number_input(
        'Max Tokens',
        min_value=100,
        max_value=4000,
        value=1024,
        step=100,
        key='max_tokens'
    )

    um.spacer(height='24px')
    um.divider()
    um.spacer(height='16px')

    # System prompt
    um.text('System Prompt', color='#94a3b8', size='12px')
    um.spacer(height='8px')

    system_prompt = um.text_area(
        '',
        value='You are a helpful AI assistant. Be concise, accurate, and friendly.',
        rows=4,
        key='system_prompt'
    )

    um.spacer(height='24px')
    um.divider()
    um.spacer(height='16px')

    # Clear chat button
    if um.button('Clear Conversation', variant='outline', key='clear_chat'):
        um.session_state['messages'] = []
        um.rerun()

    um.spacer(height='16px')

    # Stats
    with um.card():
        um.subheader('Session Stats')
        um.spacer(height='8px')
        msg_count = len(um.session_state.get('messages', []))
        um.text(f'Messages: {msg_count}', color='#64748b', size='12px')
        um.text(f'Model: {model}', color='#64748b', size='12px')


# ============================================================================
# Main Chat Area
# ============================================================================

# Header
with um.columns([3, 1]):
    with um.column():
        um.header('AI Chat with Streaming')
        um.text('Experience real-time token-by-token responses', color='#64748b')
    with um.column():
        um.badge('Streaming', variant='success')
        um.badge(model, variant='info')

um.spacer(height='16px')

# Initialize messages
if 'messages' not in um.session_state:
    um.session_state['messages'] = [
        {
            'role': 'assistant',
            'content': "Hello! I'm an AI assistant demonstrating Umara's streaming capabilities. Try asking me about:\n\n- **Umara framework** - What makes it special\n- **Code examples** - See streaming in action\n- **Any question** - I'll respond with simulated streaming\n\nWatch how the response appears token by token!"
        }
    ]

# Display chat messages
with um.chat_container(height='450px', key='chat_display'):
    for msg in um.session_state['messages']:
        um.chat_message(msg['content'], role=msg['role'])

um.spacer(height='16px')

# Chat input
user_input = um.chat_input(
    'Type your message and watch the streaming response...',
    key='user_input'
)

# Handle user input
if user_input:
    # Add user message
    um.session_state['messages'].append({
        'role': 'user',
        'content': user_input
    })

    # Generate streaming response
    um.spacer(height='8px')
    with um.card():
        um.avatar(name='AI', size='32px')
        um.spacer(height='8px')

        # Stream the response with write_stream
        full_response = um.write_stream(
            simulate_stream(user_input, model),
            key='ai_response'
        )

        # Save the complete response
        um.session_state['messages'].append({
            'role': 'assistant',
            'content': full_response
        })

um.spacer(height='24px')
um.divider()

# ============================================================================
# Feature Highlights
# ============================================================================
um.spacer(height='16px')
um.subheader('Streaming Features')

with um.columns(3):
    with um.column():
        with um.card():
            um.subheader('Real-time')
            um.text('Token-by-token rendering as the AI generates', color='#64748b', size='14px')
    with um.column():
        with um.card():
            um.subheader('AI-Native')
            um.text('Built-in support for OpenAI & Anthropic streams', color='#64748b', size='14px')
    with um.column():
        with um.card():
            um.subheader('Beautiful')
            um.text('Smooth animations and typing indicators', color='#64748b', size='14px')

um.spacer(height='16px')

# Code example
with um.expander('View Code Example', expanded=False, key='code_expander'):
    um.code('''# Using Umara with OpenAI streaming
import umara as um
from openai import OpenAI

client = OpenAI()

def get_stream(prompt):
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Display streaming response
prompt = um.chat_input("Ask anything...")
if prompt:
    um.write_stream(get_stream(prompt))
''', language='python')

um.spacer(height='24px')

# Footer
um.text('AI Streaming Demo - Umara v0.3.0', color='#64748b', size='12px')
