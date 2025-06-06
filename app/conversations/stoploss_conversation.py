# app/conversations/stoploss_conversation.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.data_utils import update_user_data, get_user_data
from app.config.constants import STOPLOSS
from app.config.messages import MESSAGES

async def handle_stoploss_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process stop-loss percentage input."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")
    text = update.message.text.strip()

    try:
        stoploss = float(text)
        if stoploss < 0 or stoploss > 100:
            await update.message.reply_text(
                "❌ कृपया 0 और 100 के बीच एक वैध प्रतिशत दर्ज करें।" if language == "hi" else
                "❌ Please enter a valid percentage between 0 and 100.",
                parse_mode="Markdown"
            )
            return STOPLOSS

        update_user_data(user_id, {
            "stoploss": stoploss,
            "awaiting": None
        })

        await update.message.reply_text(
            f"✅ स्टॉप-लॉस {stoploss}% पर सेट किया गया!\nअपनी सेटिंग्स देखने के लिए /settings का उपयोग करें।" if language == "hi" else
            f"✅ Stop-loss set to {stoploss}%!\nUse /settings to view your settings.",
            parse_mode="Markdown"
        )

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ गलत प्रारूप। कृपया एक वैध संख्या दर्ज करें (उदाहरण: *10*).",
            parse_mode="Markdown"
        )
        return STOPLOSS

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel stop-loss setting process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    update_user_data(user_id, {"awaiting": None})

    await update.message.reply_text(
        MESSAGES[language]["cancel"],
        parse_mode="Markdown"
    )

    return ConversationHandler.END
