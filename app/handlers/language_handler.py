# app/handlers/language_handler.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.data_utils import get_user_data, update_user_data
from app.config.constants import LANGUAGE
from app.config.messages import MESSAGES

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initiate language selection process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    await update.message.reply_text(
        MESSAGES[language]["language_prompt"],
        parse_mode="Markdown"
    )

    update_user_data(user_id, {"awaiting": "language"})
    return LANGUAGE