# app/handlers/broadcast_handler.py
import asyncio
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.data_utils import get_user_data, update_user_data
from app.config.constants import BROADCAST, OWNER_ID
from app.config.messages import MESSAGES

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Initiate broadcast process for owner."""
    user_id = str(update.effective_user.id)
    user_data = await asyncio.to_thread(get_user_data, user_id)
    language = user_data.get("language", "en")

    if user_id != OWNER_ID:
        await update.message.reply_text(
            "❌ यह कमांड केवल बॉट मालिक के लिए है।" if language == "hi" else
            "❌ This command is for the bot owner only.",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    await update.message.reply_text(
        MESSAGES[language]["broadcast_prompt"],
        parse_mode="Markdown"
    )

    await asyncio.to_thread(update_user_data, user_id, {"awaiting": "broadcast"})
    return BROADCAST