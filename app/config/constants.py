# app/config/constants.py

# Conversation states
TARGET = "TARGET"
CLOSING = "CLOSING"
STOPLOSS = "STOPLOSS"
NAME = "NAME"
RATE_MODE = "RATE_MODE"
CURRENCY_CHANGE = "CURRENCY_CHANGE"
BROADCAST = "BROADCAST"
LANGUAGE = "LANGUAGE"

# Default settings
CURRENCY = "₹"  # Default currency symbol
OWNER_ID = "5620922625"  # Replace with your actual Telegram ID

# Bot configuration
BOT_NAME = "Compounding Tracker Bot"
BOT_VERSION = "2.0.0"

# File paths
DATA_FILE = "user_data.json"
FONT_DIR = "assets/fonts"

# Reminder settings
REMINDER_HOUR = 20  # 8 PM
REMINDER_MINUTE = 0
TIMEZONE = "Asia/Kolkata"

# Image settings
CARD_WIDTH = 900
CARD_HEIGHT = 700
PROFILE_PHOTO_SIZE = 100

# Progress thresholds
EXCELLENT_THRESHOLD = 1.0   # 100% or above
GOOD_THRESHOLD = 0.8        # 80% or above
WARNING_THRESHOLD = 0.5     # 50% or above
# Below 50% is considered poor