# app/handlers/help_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from app.utils.data_utils import get_user_data
from app.config.messages import MESSAGES

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command with comprehensive command guide."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    await update.message.reply_text(
        MESSAGES[language]["help_text"],
        parse_mode="Markdown"
    )