# app/utils/calculation_utils.py
from datetime import datetime
import pytz
import math

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
    if not user_data.get("target"):
        return {
            "days_passed": 0,
            "expected_balance": 0.0,
            "today_profit_goal": 0.0,
            "stoploss_level": None,
            "current_balance": 0.0,
            "status_badge": "🔴"
        }

    target = user_data["target"]
    start_amount = float(target["start_amount"])
    rate = float(target["rate"])
    mode = target["mode"]
    start_date = user_data.get("start_date")
    history = user_data.get("history", [])

    tz = pytz.timezone("Asia/Kolkata")
    current_date = datetime.now(tz)
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d") if start_date else current_date
    days_passed = (current_date - start_datetime).days

    # Calculate expected balance
    expected_balance = calculate_compounding(start_amount, rate, mode, days_passed)

    # Get current balance from history
    current_balance = history[-1]["balance"] if history else start_amount

    # Calculate today's profit goal
    prev_day_balance = calculate_compounding(start_amount, rate, mode, days_passed - 1)
    today_profit_goal = expected_balance - prev_day_balance

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
        "status_badge": status_badge
    }
