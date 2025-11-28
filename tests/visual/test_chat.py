"""Test chat components"""
import umara as um

um.set_page_config(page_title="Chat Test", layout="wide")

um.title("Chat Components Test")

um.subheader("chat_message()")
um.chat_message("Hello! How can I help you?", role="assistant")
um.chat_message("I need help with Umara", role="user")
um.chat_message("Sure! Umara is a Python UI framework.", role="assistant")

um.divider()

um.subheader("chat_input()")
user_msg = um.chat_input("Type your message...", key="chat_input")
if user_msg:
    um.text(f"You typed: {user_msg}")

um.divider()
um.success("Chat components test loaded!")
