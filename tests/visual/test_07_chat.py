"""Comprehensive test for Chat components"""
import umara as um

um.set_page_config(page_title="Chat Test", layout="wide")

um.title("Chat Components Test")

# chat_message()
um.subheader("1. chat_message()")
um.chat_message("Hello! How can I help you today?", role="assistant", avatar="bot")
um.chat_message("I need help with Umara framework", role="user", avatar="user")
um.chat_message("Umara is a Python UI framework that lets you build web apps easily!", role="assistant")
um.chat_message("That sounds great! How do I get started?", role="user")

um.divider()

# chat_input()
um.subheader("2. chat_input()")
user_message = um.chat_input("Type your message...", key="chat_main")
if user_message:
    um.chat_message(user_message, role="user")
    um.chat_message("Thanks for your message! This is an echo response.", role="assistant")

um.divider()

# chat_container()
um.subheader("3. chat_container()")
with um.chat_container(height=200):
    um.chat_message("Message 1 in container", role="assistant")
    um.chat_message("Message 2 in container", role="user")
    um.chat_message("Message 3 in container", role="assistant")
    um.chat_message("Message 4 in container", role="user")
    um.chat_message("Message 5 in container (scroll to see)", role="assistant")

um.divider()

# chat() - full chat interface
um.subheader("4. chat() - Full chat interface")
messages = [
    {"role": "assistant", "content": "Welcome to the chat!"},
    {"role": "user", "content": "Hi there!"},
    {"role": "assistant", "content": "How can I assist you?"},
]
um.chat(messages=messages, key="full_chat")

um.divider()

um.success("Chat components test completed!")
