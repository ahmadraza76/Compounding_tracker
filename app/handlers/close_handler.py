# app/handlers/close_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from app.utils.data_utils import get_user_data, update_user_data
from app.config.constants import CLOSING
from app.config.messages import MESSAGES

async def close_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initiate balance closing process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    if not user_data.get("target"):
        await update.message.reply_text(
            MESSAGES[language]["no_target"],
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    await update.message.reply_text(
        MESSAGES[language]["close_prompt"],
        parse_mode="Markdown"
    )

    update_user_data(user_id, {"awaiting": "closing"})
    return CLOSING
