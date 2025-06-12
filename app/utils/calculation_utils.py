# app/utils/calculation_utils.py
import logging
from datetime import datetime
import pytz
import math

logger = logging.getLogger(__name__)

def calculate_compounding(start_amount: float, rate: float, mode: str, periods: float) -> float:
    """Calculate compounded balance based on start amount, rate, mode, and periods."""
    if mode == "daily":
        r = rate / 100 / 365  # Daily rate
        n = periods
    else:  # monthly
        r = rate / 100 / 12   # Monthly rate
        n = periods / 30      # Periods in months
    return start_amount * math.pow(1 + r, n)

def check_stoploss(user_data: dict, balance: float) -> bool:
    """Check if balance is below stop-loss level."""
    if not user_data.get("stoploss") or not user_data.get("target"):
        return False
    stoploss_percent = user_data["stoploss"]
    start_amount = float(user_data["target"]["start_amount"])
    stoploss_level = start_amount * (1 - stoploss_percent / 100)
    return balance < stoploss_level

def calculate_progress(user_data: dict) -> dict:
    """Calculate user progress metrics."""
    logger = logging.getLogger(__name__) # Ensure logger is defined

    default_error_return = {
        "days_passed": 0,
        "expected_balance": 0.0,
        "today_profit_goal": 0.0,
        "stoploss_level": None,
        "current_balance": 0.0,
        "status_badge": "🔴" # Or a new badge like "ERR"
    }

    if not user_data.get("target"):
        return {
            **default_error_return,
            "error": "No target set"
        }

    target = user_data["target"]
    user_id = user_data.get('id', 'unknown_user') # For logging

    try:
        start_amount = float(target["start_amount"])
    except ValueError:
        logger.error(f"ValueError for user_id: {user_id} - start_amount is not a valid number.")
        return {
            **default_error_return,
            "error": "Invalid target data: start_amount is not a valid number."
        }

    try:
        rate = float(target["rate"])
    except ValueError:
        logger.error(f"ValueError for user_id: {user_id} - rate is not a valid number.")
        return {
            **default_error_return,
            "error": "Invalid target data: rate is not a valid number."
        }

    try:
        target_amount_val = float(target["target_amount"])
    except ValueError:
        logger.error(f"ValueError for user_id: {user_id} - target_amount is not a valid number.")
        return {
            **default_error_return,
            "error": "Invalid target data: target_amount is not a valid number."
        }

    mode = target["mode"]
    start_date = user_data.get("start_date")
    history = user_data.get("history", [])

    tz = pytz.timezone("Asia/Kolkata")
    current_date = datetime.now(tz)

    if user_data.get("start_date"):
        start_datetime = datetime.strptime(user_data["start_date"], "%Y-%m-%d").replace(tzinfo=tz) # Add timezone info
        if start_datetime > current_date:
            start_datetime = current_date
        days_passed = (current_date - start_datetime).days
    else:
        start_datetime = current_date
        days_passed = 0

    if days_passed < 0: # Should not happen with the logic above, but as a safeguard
        days_passed = 0

    # Calculate expected balance and today's profit goal
    if days_passed == 0:
        expected_balance = start_amount
        today_profit_goal = calculate_compounding(start_amount, rate, mode, 1) - start_amount
    else:
        expected_balance = calculate_compounding(start_amount, rate, mode, days_passed)
        prev_day_balance = calculate_compounding(start_amount, rate, mode, days_passed - 1)
        today_profit_goal = expected_balance - prev_day_balance

    # Get current balance from history
    current_balance = history[-1]["balance"] if history else start_amount

    # Calculate stop-loss level
    stoploss_level = None
    if user_data.get("stoploss"):
        stoploss_percent = user_data["stoploss"]
        stoploss_level = start_amount * (1 - stoploss_percent / 100)

    # Determine status badge
    if current_balance >= expected_balance:
        status_badge = "🟢"  # On track
    elif stoploss_level and current_balance < stoploss_level:
        status_badge = "🔴"  # Below stop-loss
    else:
        status_badge = "🟡"  # Needs attention

    return {
        "days_passed": days_passed,
        "expected_balance": expected_balance,
        "today_profit_goal": today_profit_goal,
        "stoploss_level": stoploss_level,
        "current_balance": current_balance,
        "status_badge": status_badge,
        "start_amount_val": start_amount,
        "target_amount_val": target_amount_val,
        "rate_val": rate,
        "error": None # Explicitly set error to None for successful returns
    }
