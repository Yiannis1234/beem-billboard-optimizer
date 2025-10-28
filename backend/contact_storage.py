"""
Simple contact form that saves messages to a file
"""

import json
import os
from datetime import datetime

def save_contact_message(name, email, message):
    """Save contact form message to a file"""
    try:
        # Create messages directory if it doesn't exist
        messages_dir = "contact_messages"
        if not os.path.exists(messages_dir):
            os.makedirs(messages_dir)
        
        # Create message data
        message_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "email": email,
            "message": message
        }
        
        # Save to file with timestamp
        filename = f"{messages_dir}/message_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(message_data, f, indent=2, ensure_ascii=False)
        
        return True, f"Message saved successfully!"
        
    except Exception as e:
        return False, f"Failed to save message: {str(e)}"

def get_all_messages():
    """Get all saved contact messages"""
    try:
        messages_dir = "contact_messages"
        if not os.path.exists(messages_dir):
            return []
        
        messages = []
        for filename in sorted(os.listdir(messages_dir)):
            if filename.endswith('.json'):
                filepath = os.path.join(messages_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    message_data = json.load(f)
                    messages.append(message_data)
        
        return messages
        
    except Exception as e:
        print(f"Error reading messages: {e}")
        return []
