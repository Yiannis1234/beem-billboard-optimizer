"""
Admin page to view contact messages
"""

import streamlit as st
from backend.contact_storage import get_all_messages

def render_admin_contact_messages():
    """Render admin page to view contact messages"""
    st.title("📧 Contact Messages")
    
    messages = get_all_messages()
    
    if not messages:
        st.info("No messages yet.")
        return
    
    st.write(f"**Total messages: {len(messages)}**")
    
    for i, msg in enumerate(messages, 1):
        with st.expander(f"Message #{i} - {msg['name']} ({msg['timestamp']})"):
            st.write(f"**Name:** {msg['name']}")
            st.write(f"**Email:** {msg['email']}")
            st.write(f"**Time:** {msg['timestamp']}")
            st.write(f"**Message:**")
            st.write(msg['message'])
            
            # Add reply button
            if st.button(f"Reply to {msg['name']}", key=f"reply_{i}"):
                st.info(f"📧 Reply to: {msg['email']}")

if __name__ == "__main__":
    render_admin_contact_messages()
