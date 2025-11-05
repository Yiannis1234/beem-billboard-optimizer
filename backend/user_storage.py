"""
Persistent storage for user accounts.
Stores user data in a JSON file so accounts persist across server restarts.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional

USER_DATA_FILE = os.getenv("USER_DATA_FILE", "user_accounts.json")


def _load_users() -> Dict[str, Dict]:
    """Load user accounts from JSON file."""
    if not os.path.exists(USER_DATA_FILE):
        return {}
    
    try:
        with open(USER_DATA_FILE, 'r') as f:
            data = json.load(f)
            return data.get('users', {})
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading user data: {e}")
        return {}


def _save_users(users: Dict[str, Dict]) -> None:
    """Save user accounts to JSON file."""
    try:
        data = {
            'users': users,
            'lastUpdated': datetime.utcnow().isoformat() + 'Z',
        }
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving user data: {e}")


def get_user(email: str) -> Optional[Dict]:
    """Get user account by email."""
    users = _load_users()
    return users.get(email.lower().strip())


def create_user(email: str, token: str, trial: bool = True, paid: bool = False, stripe_session_id: Optional[str] = None) -> Dict:
    """Create or update a user account."""
    users = _load_users()
    email = email.lower().strip()
    
    user_data = {
        "email": email,
        "trial": trial,
        "paid": paid,
        "token": token,
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "lastLogin": datetime.utcnow().isoformat() + "Z",
    }
    
    if stripe_session_id:
        user_data["stripeSessionId"] = stripe_session_id
    
    users[email] = user_data
    _save_users(users)
    
    return user_data


def update_user(email: str, **updates) -> Optional[Dict]:
    """Update user account fields."""
    users = _load_users()
    email = email.lower().strip()
    
    if email not in users:
        return None
    
    users[email].update(updates)
    users[email]["lastLogin"] = datetime.utcnow().isoformat() + "Z"
    _save_users(users)
    
    return users[email]


def verify_token(token: str) -> Optional[Dict]:
    """Verify auth token and return user account."""
    users = _load_users()
    
    for user in users.values():
        if user.get("token") == token:
            # Update last login
            user["lastLogin"] = datetime.utcnow().isoformat() + "Z"
            _save_users(users)
            return user
    
    return None


def get_all_users() -> Dict[str, Dict]:
    """Get all user accounts."""
    return _load_users()

