# app/conversations/language_conversation.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.data_utils import update_user_data, get_user_data
from app.config.constants import LANGUAGE
from app.config.messages import MESSAGES

async def handle_language_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process language choice."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")
    text = update.message.text.strip().lower()

    if text not in ["hi", "en", "hindi", "english"]:
        await update.message.reply_text(
            "❌ Please choose 'Hindi' or 'English' (en/hi).",
            parse_mode="Markdown"
        )
        return LANGUAGE

    new_language = "hi" if text in ["hi", "hindi"] else "en"

    update_user_data(user_id, {
        "language": new_language,
        "awaiting": None
    })

    await update.message.reply_text(
        MESSAGES[new_language]["language_set"],
        parse_mode="Markdown"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel language selection process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    update_user_data(user_id, {"awaiting": None})

    await update.message.reply_text(
        MESSAGES[language]["cancel"],
        parse_mode="Markdown"
    )

    return ConversationHandler.END
