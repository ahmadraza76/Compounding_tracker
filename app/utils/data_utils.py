# app/utils/data_utils.py
import json
import os
from threading import Lock
import logging

DATA_FILE = "user_data.json"
lock = Lock()
logger = logging.getLogger(__name__)

def ensure_data_directory():
    """Ensure data directory exists."""
    data_dir = os.path.dirname(DATA_FILE)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)

def load_data():
    """Load user data from JSON file with error handling."""
    with lock:
        ensure_data_directory()
        if not os.path.exists(DATA_FILE):
            logger.info(f"Data file {DATA_FILE} not found, creating new one")
            return {"users": {}}
        
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure proper structure
                if "users" not in data:
                    data = {"users": data} if data else {"users": {}}
                return data
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {DATA_FILE}: {e}")
            # Backup corrupted file
            backup_file = f"{DATA_FILE}.backup"
            if os.path.exists(DATA_FILE):
                os.rename(DATA_FILE, backup_file)
                logger.info(f"Corrupted file backed up to {backup_file}")
            return {"users": {}}
        except Exception as e:
            logger.error(f"Error loading data from {DATA_FILE}: {e}")
            return {"users": {}}

def save_data(data):
    """Save user data to JSON file with error handling."""
    with lock:
        ensure_data_directory()
        try:
            # Write to temporary file first
            temp_file = f"{DATA_FILE}.tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Replace original file
            if os.path.exists(DATA_FILE):
                os.replace(temp_file, DATA_FILE)
            else:
                os.rename(temp_file, DATA_FILE)
                
        except Exception as e:
            logger.error(f"Error saving data to {DATA_FILE}: {e}")
            # Clean up temp file if it exists
            temp_file = f"{DATA_FILE}.tmp"
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise

def get_user_data(user_id: str) -> dict:
    """Retrieve user data by ID with default values."""
    try:
        data = load_data()
        user_data = data.get("users", {}).get(user_id, {})
        
        # Ensure default values
        defaults = {
            "name": "",
            "language": "en",
            "currency": "₹",
            "reminders": True,
            "history": [],
            "target": None,
            "stoploss": None,
            "start_date": None,
            "awaiting": None
        }
        
        for key, default_value in defaults.items():
            if key not in user_data:
                user_data[key] = default_value
        
        return user_data
    except Exception as e:
        logger.error(f"Error getting user data for {user_id}: {e}")
        return {
            "name": "",
            "language": "en",
            "currency": "₹",
            "reminders": True,
            "history": [],
            "target": None,
            "stoploss": None,
            "start_date": None,
            "awaiting": None
        }

def update_user_data(user_id: str, updates: dict) -> None:
    """Update user data with new values."""
    try:
        data = load_data()
        if "users" not in data:
            data["users"] = {}
        if user_id not in data["users"]:
            data["users"][user_id] = {}
        
        data["users"][user_id].update(updates)
        save_data(data)
        logger.debug(f"Updated user data for {user_id}: {list(updates.keys())}")
    except Exception as e:
        logger.error(f"Error updating user data for {user_id}: {e}")
        raise