# app/conversations/target_conversation.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
import pytz
from app.utils.data_utils import update_user_data, get_user_data
from app.config.constants import TARGET
from app.config.messages import MESSAGES

async def handle_target_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process target input from user."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")
    text = update.message.text.strip()

    try:
        start_amount, target_amount, rate, mode = [x.strip() for x in text.split(",")]
        start_amount = float(start_amount)
        target_amount = float(target_amount)
        rate = float(rate)
        mode = mode.lower()

        if start_amount <= 0 or target_amount <= 0 or rate <= 0:
            await update.message.reply_text(
                "❌ कृपया सकारात्मक मान दर्ज करें।" if language == "hi" else
                "❌ Please enter positive values.",
                parse_mode="Markdown"
            )
            return TARGET

        if target_amount <= start_amount:
            await update.message.reply_text(
                "❌ लक्ष्य राशि शुरुआती राशि से अधिक होनी चाहिए।" if language == "hi" else
                "❌ Target amount must be greater than start amount.",
                parse_mode="Markdown"
            )
            return TARGET

        if mode not in ["daily", "monthly"]:
            await update.message.reply_text(
                "❌ मोड 'daily' या 'monthly' होना चाहिए।" if language == "hi" else
                "❌ Mode must be 'daily' or 'monthly'.",
                parse_mode="Markdown"
            )
            return TARGET

        tz = pytz.timezone("Asia/Kolkata")
        start_date = datetime.now(tz).strftime("%Y-%m-%d")

        update_user_data(user_id, {
            "target": {
                "start_amount": start_amount,
                "target_amount": target_amount,
                "rate": rate,
                "mode": mode
            },
            "start_date": start_date,
            "history": [{"date": start_date, "balance": start_amount}],
            "awaiting": None
        })

        await update.message.reply_text(
            "✅ लक्ष्य सफलतापूर्वक सेट किया गया!\nअपनी प्रगति देखने के लिए /status का उपयोग करें।" if language == "hi" else
            "✅ Target successfully set!\nUse /status to view your progress.",
            parse_mode="Markdown"
        )

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ गलत प्रारूप। कृपया प्रारूप का पालन करें: *start_amount, target_amount, rate, mode*\nउदाहरण: *1500, 10000, 5, daily*"
            if language == "hi" else
            "❌ Invalid format. Please follow the format: *start_amount, target_amount, rate, mode*\nExample: *1500, 10000, 5, daily*",
            parse_mode="Markdown"
        )
        return TARGET

async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel target setting process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    update_user_data(user_id, {"awaiting": None})

    await update.message.reply_text(
        MESSAGES[language]["cancel"],
        parse_mode="Markdown"
    )

    return ConversationHandler.END
