# app/conversations/broadcast_conversation.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.data_utils import load_data, get_user_data, update_user_data
from app.config.constants import BROADCAST, OWNER_ID
from app.config.messages import MESSAGES

async def handle_broadcast_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process broadcast message input."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    if user_id != OWNER_ID:
        await update.message.reply_text(
            "❌ यह कमांड केवल बॉट मालिक लिए है।" if language == "hi" else
            "❌ This command is for the bot owner only.",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    message = update.message.text.strip()
    if not message or len(message) > 4096:
        await update.message.reply_text(
            "❌ Please enter a valid message between 1 and 4096 characters.",
            parse_mode="Markdown"
        )
        return BROADCAST

    data = load_data()
    for uid in data.keys():
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=message,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Failed to send broadcast to {uid}: {e}")

    update_user_data(user_id, {"awaiting": None})

    await update.message.reply_text(
        "✅ Message successfully broadcasted to all users!",
        parse_mode="Markdown"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel broadcast process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    update_user_data(user_id, {"awaiting": None})

    await update.message.reply_text(
        MESSAGES[language]["cancel"],
        parse_mode="Markdown"
    )

    return ConversationHandler.END
