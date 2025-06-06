# app/utils/reminder_utils.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application
from app.utils.data_utils import load_data
from app.config.messages import MESSAGES
import pytz
import telegram.error

def schedule_reminders(scheduler: AsyncIOScheduler, application: Application = None) -> None:
    """Schedule daily reminders at 8 PM IST."""
    tz = pytz.timezone("Asia/Kolkata")
    scheduler.add_job(
        send_reminders,
        trigger="cron",
        hour=20,
        minute=0,
        timezone=tz,
        args=[application]
    )

async def send_reminders(application: Application) -> None:
    """Send reminders to users with reminders enabled."""
    data = load_data()
    for user_id, user_data in data.get("users", {}).items():
        if user_data.get("reminders", False) and user_data.get("target"):
            language = user_data.get("language", "en")
            try:
                await application.bot.send_message(
                    chat_id=user_id,
                    text=MESSAGES[language]["reminder_prompt"],
                    parse_mode="Markdown"
                )
            except telegram.error.Forbidden:
                print(f"Cannot send reminder to {user_id}: Bot blocked")
            except Exception as e:
                print(f"Failed to send reminder to {user_id}: {e}")
