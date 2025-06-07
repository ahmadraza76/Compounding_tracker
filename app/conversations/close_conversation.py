# app/conversations/close_conversation.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
import pytz
from app.utils.data_utils import update_user_data, get_user_data
from app.utils.calculation_utils import check_stoploss
from app.config.constants import CLOSING
from app.config.messages import MESSAGES

async def handle_closing_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process closing balance input from user."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")
    text = update.message.text.strip()

    try:
        balance = float(text)
        if balance < 0:
            await update.message.reply_text(
                "❌ कृपया वैध सकारात्मक बैलेंस दर्ज करें।" if language == "hi" else
                "❌ Please enter a valid positive balance.",
                parse_mode="Markdown"
            )
            return CLOSING

        # Check stop-loss
        if check_stoploss(user_data, balance):
            await update.message.reply_text(
                MESSAGES[language]["stoploss_alert"],
                parse_mode="Markdown"
            )

        # Update history
        tz = pytz.timezone("Asia/Kolkata")
        current_date = datetime.now(tz).strftime("%Y-%m-%d")
        
        history = user_data.get("history", [])
        if history and history[-1]["date"] == current_date:
            history[-1]["balance"] = balance
        else:
            history.append({"date": current_date, "balance": balance})

        # Check target
        if user_data.get("target"):
            target_amount = float(user_data["target"]["target_amount"])
            if balance >= target_amount:
                await update.message.reply_text(
                    MESSAGES[language]["target_achieved"],
                    parse_mode="Markdown"
                )

        update_user_data(user_id, {
            "history": history,
            "awaiting": None
        })

        await update.message.reply_text(
            "✅ बैलेंस सफलतापूर्वक रिकॉर्ड किया गया!\nअपनी प्रगति देखने के लिए /status का उपयोग करें।" if language == "hi" else
            "✅ Balance successfully recorded!\nUse /status to view your progress.",
            parse_mode="Markdown"
        )

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid format. Please enter a valid number (e.g., *1500.50*).",
            parse_mode="Markdown"
        )
        return CLOSING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel balance closing process."""
    user_id = str(update.effective_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    update_user_data(user_id, {"awaiting": None})

    await update.message.reply_text(
        MESSAGES[language]["cancel"],
        parse_mode="Markdown"
    )

    return ConversationHandler.END