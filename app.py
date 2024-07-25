
import streamlit as st
import sqlite3
import time

# Initialize connection to the SQLite database
conn = sqlite3.connect('chat.db')
c = conn.cursor()

# Create chat messages table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS messages (
    room TEXT,
    user TEXT,
    message TEXT,
    timestamp REAL
)
''')
conn.commit()

# Function to add a message to the database
def add_message(room, user, message):
    c.execute('INSERT INTO messages (room, user, message, timestamp) VALUES (?, ?, ?, ?)',
              (room, user, message, time.time()))
    conn.commit()

# Function to get messages from the database
def get_messages(room):
    c.execute('SELECT user, message, timestamp FROM messages WHERE room = ? ORDER BY timestamp ASC', (room,))
    return c.fetchall()

# Streamlit app setup
st.set_page_config(page_title="Chat App", layout="wide")

# Sidebar for navigation
st.sidebar.title("Chat App")
page = st.sidebar.radio("Navigate", ["Create/Join Room", "Chat Room"])

def display_messages(messages):
    for message in messages:
        user, text, timestamp = message
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        if user == st.session_state["display_name"]:
            st.markdown(f'<div style="text-align: right; padding: 10px;">'
                        f'<span style="display: inline-block; padding: 10px; background-color: #DCF8C6; '
                        f'border-radius: 10px; margin-bottom: 5px;">{text}</span>'
                        f'<div style="font-size: 10px; color: gray;">{timestamp}</div>'
                        f'</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align: left; padding: 10px;">'
                        f'<span style="display: inline-block; padding: 10px; background-color: #ECECEC; '
                        f'border-radius: 10px; margin-bottom: 5px;">{text}</span>'
                        f'<div style="font-size: 10px; color: gray;">{timestamp}</div>'
                        f'</div>', unsafe_allow_html=True)

if page == "Create/Join Room":
    st.title("Create or Join a Chat Room")
    chat_room = st.text_input("Enter chat room name")
    display_name = st.text_input("Enter your display name")

    if st.button("Join Chat Room"):
        if chat_room and display_name:
            st.session_state["chat_room"] = chat_room
            st.session_state["display_name"] = display_name
            st.success(f"Joined chat room: {chat_room} as {display_name}")
        else:
            st.error("Please enter both chat room name and display name")

if page == "Chat Room":
    if "chat_room" in st.session_state and "display_name" in st.session_state:
        st.title(f"Chat Room: {st.session_state['chat_room']}")
        chat_room = st.session_state["chat_room"]
        display_name = st.session_state["display_name"]

        # Display chat messages
        st.subheader("Messages")
        messages = get_messages(chat_room)
        display_messages(messages)

        # Input for new messages
        st.subheader("New Message")
        new_message = st.text_input("Type your message")
        if st.button("Send"):
            if new_message:
                add_message(chat_room, display_name, new_message)
                st.experimental_rerun()
            else:
                st.error("Message cannot be empty")
    else:
        st.warning("Please join a chat room first from the 'Create/Join Room' page.")
