# app/conversations/name_conversation.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.data_utils import update_user_data, get_user_data
from app.config.constants import NAME
from app.config.messages import MESSAGES

async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process name input."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")
    name = update.message.text.strip()

    if not name or len(name) > 50:
        await update.message.reply_text(
            "❌ कृपया 1 से 50 अक्षरों के बीच एक वैध नाम दर्ज करें।" if language == "hi" else
            "❌ Please enter a valid name between 1 and 50 characters.",
            parse_mode="Markdown"
        )
        return NAME

    update_user_data(user_id, {
        "name": name,
        "awaiting": None
    })

    await update.message.reply_text(
        f"✅ नाम {name} पर सेट किया गया!\nअपनी सेटिंग्स देखने के लिए /settings का उपयोग करें।" if language == "hi" else
        f"✅ Name successfully set to {name}!\nUse /settings to view your settings.",
        parse_mode="Markdown"
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel name setting process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    update_user_data(user_id, {"awaiting": None})

    await update.message.reply_text(
        MESSAGES[language]["cancel"],
        parse_mode="Markdown"
    )

    return ConversationHandler.END
