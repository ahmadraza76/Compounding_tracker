# app/utils/data_utils.py
import json
import os
from threading import Lock

DATA_FILE = "user_data.json"
lock = Lock()

def load_data():
    """Load user data from JSON file."""
    with lock:
        if not os.path.exists(DATA_FILE):
            return {"users": {}}
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"users": {}}

def save_data(data):
    """Save user data to JSON file."""
    with lock:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

def get_user_data(user_id: str) -> dict:
    """Retrieve user data by ID."""
    data = load_data()
    return data.get("users", {}).get(user_id, {})

def update_user_data(user_id: str, updates: dict) -> None:
    """Update user data with new values."""
    data = load_data()
    if "users" not in data:
        data["users"] = {}
    if user_id not in data["users"]:
        data["users"][user_id] = {}
    data["users"][user_id].update(updates)
    save_data(data)
