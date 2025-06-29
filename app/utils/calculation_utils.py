# app/utils/calculation_utils.py
import logging
from datetime import datetime
import pytz
import math
import traceback

logger = logging.getLogger(__name__)

def calculate_compounding(start_amount: float, rate: float, mode: str, periods: float) -> float:
    """Calculate compounded balance based on start amount, rate, mode, and periods."""
    try:
        if mode == "daily":
            r = rate / 100 / 365  # Daily rate
            n = periods
        else:  # monthly
            r = rate / 100 / 12   # Monthly rate
            n = periods / 30      # Periods in months
        
        result = start_amount * math.pow(1 + r, n)
        return result
    except Exception as e:
        logger.error(f"Error in calculate_compounding: {e}")
        return start_amount

def check_stoploss(user_data: dict, balance: float) -> bool:
    """Check if balance is below stop-loss level."""
    try:
        if not user_data.get("stoploss") or not user_data.get("target"):
            return False
        stoploss_percent = user_data["stoploss"]
        start_amount = float(user_data["target"]["start_amount"])
        stoploss_level = start_amount * (1 - stoploss_percent / 100)
        return balance < stoploss_level
    except Exception as e:
        logger.error(f"Error in check_stoploss: {e}")
        return False

def calculate_progress(user_data: dict) -> dict:
    """Calculate user progress metrics."""
    logger.info("Starting progress calculation")
    
    default_error_return = {
        "days_passed": 0,
        "expected_balance": 0.0,
        "today_profit_goal": 0.0,
        "stoploss_level": None,
        "current_balance": 0.0,
        "status_badge": "🔴",
        "start_amount_val": 0.0,
        "target_amount_val": 0.0,
        "rate_val": 0.0,
        "error": None
    }

    try:
        if not user_data.get("target"):
            logger.warning("No target set for user")
            return {
                **default_error_return,
                "error": "No target set"
            }

        target = user_data["target"]
        user_id = user_data.get('id', 'unknown_user')

        # Validate target data
        try:
            start_amount = float(target["start_amount"])
            rate = float(target["rate"])
            target_amount_val = float(target["target_amount"])
        except (ValueError, KeyError) as e:
            logger.error(f"Invalid target data for user {user_id}: {e}")
            return {
                **default_error_return,
                "error": f"Invalid target data: {str(e)}"
            }

        mode = target.get("mode", "daily")
        start_date = user_data.get("start_date")
        history = user_data.get("history", [])

        # Calculate days passed
        tz = pytz.timezone("Asia/Kolkata")
        current_date = datetime.now(tz)

        if start_date:
            try:
                start_datetime = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=tz)
                if start_datetime > current_date:
                    start_datetime = current_date
                days_passed = (current_date - start_datetime).days
            except ValueError as e:
                logger.error(f"Invalid start_date format: {start_date}")
                days_passed = 0
        else:
            days_passed = 0

        if days_passed < 0:
            days_passed = 0

        # Calculate expected balance and today's profit goal
        if days_passed == 0:
            expected_balance = start_amount
            today_profit_goal = calculate_compounding(start_amount, rate, mode, 1) - start_amount
        else:
            expected_balance = calculate_compounding(start_amount, rate, mode, days_passed)
            prev_day_balance = calculate_compounding(start_amount, rate, mode, max(0, days_passed - 1))
            today_profit_goal = expected_balance - prev_day_balance

        # Get current balance from history
        current_balance = start_amount
        if history:
            try:
                current_balance = float(history[-1]["balance"])
            except (ValueError, KeyError, IndexError):
                logger.warning("Invalid balance in history, using start amount")
                current_balance = start_amount

        # Calculate stop-loss level
        stoploss_level = None
        if user_data.get("stoploss"):
            try:
                stoploss_percent = float(user_data["stoploss"])
                stoploss_level = start_amount * (1 - stoploss_percent / 100)
            except ValueError:
                logger.warning("Invalid stoploss value")

        # Determine status badge
        if current_balance >= expected_balance:
            status_badge = "🟢"  # On track
        elif stoploss_level and current_balance < stoploss_level:
            status_badge = "🔴"  # Below stop-loss
        else:
            status_badge = "🟡"  # Needs attention

        result = {
            "days_passed": days_passed,
            "expected_balance": expected_balance,
            "today_profit_goal": today_profit_goal,
            "stoploss_level": stoploss_level,
            "current_balance": current_balance,
            "status_badge": status_badge,
            "start_amount_val": start_amount,
            "target_amount_val": target_amount_val,
            "rate_val": rate,
            "error": None
        }
        
        logger.info(f"Progress calculation completed successfully: {result}")
        return result

    except Exception as e:
        logger.error(f"Unexpected error in calculate_progress: {e}")
        logger.error(traceback.format_exc())
        return {
            **default_error_return,
            "error": f"Calculation error: {str(e)}"
        }