# app/handlers/target_handler.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.data_utils import get_user_data, update_user_data
from app.config.constants import TARGET
from app.config.messages import MESSAGES

async def set_target(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initiate target setting process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    if user_data.get("target"):
        await update.message.reply_text(
            MESSAGES[language]["target_exists"],
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    await update.message.reply_text(
        MESSAGES[language]["target_prompt"],
        parse_mode="Markdown"
    )

    update_user_data(user_id, {"awaiting": "target"})
    return TARGET