# app/handlers/callback_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.data_utils import update_user_data, get_user_data
from app.config.constants import TARGET, STOPLOSS, NAME, RATE_MODE, CURRENCY_CHANGE, CLOSING
from app.config.messages import MESSAGES

async def handle_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle callback queries from settings inline buttons."""
    query = update.callback_query
    user_id = str(query.from_user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")
    data = query.data

    await query.answer()

    if data.startswith("edit_target_"):
        await query.message.reply_text(
            MESSAGES[language]["target_prompt"],
            parse_mode="Markdown"
        )
        update_user_data(user_id, {"awaiting": "target"})
        return TARGET

    elif data.startswith("edit_stoploss_"):
        await query.message.reply_text(
            "कृपया स्टॉप-लॉस प्रतिशत दर्ज करें (0-100)।\nउदाहरण: *10*" if language == "hi" else
            "Please enter the stop-loss percentage (0-100).\nExample: *10*",
            parse_mode="Markdown"
        )
        update_user_data(user_id, {"awaiting": "stoploss"})
        return STOPLOSS

    elif data.startswith("edit_name_"):
        await query.message.reply_text(
            "कृपया अपना नया नाम दर्ज करें।" if language == "hi" else
            "Please enter your new name.",
            parse_mode="Markdown"
        )
        update_user_data(user_id, {"awaiting": "name"})
        return NAME

    elif data.startswith("edit_rate_mode_"):
        await query.message.reply_text(
            "कृपया नई दर और मोड दर्ज करें।\nउदाहरण: *5, daily*" if language == "hi" else
            "Please enter the new rate and mode.\nExample: *5, daily*",
            parse_mode="Markdown"
        )
        update_user_data(user_id, {"awaiting": "rate_mode"})
        return RATE_MODE

    elif data.startswith("edit_currency_"):
        await query.message.reply_text(
            "कृपया नया मुद्रा प्रतीक दर्ज करें।\nउदाहरण: *$*" if language == "hi" else
            "Please enter the new currency symbol.\nExample: *$*",
            parse_mode="Markdown"
        )
        update_user_data(user_id, {"awaiting": "currency"})
        return CURRENCY_CHANGE

    elif data.startswith("update_balance_"):
        await query.message.reply_text(
            MESSAGES[language]["close_prompt"],
            parse_mode="Markdown"
        )
        update_user_data(user_id, {"awaiting": "closing"})
        return CLOSING

    elif data.startswith("toggle_reminders_"):
        reminders = not user_data.get("reminders", False)
        update_user_data(user_id, {"reminders": reminders})
        await query.message.reply_text(
            f"✅ रिमाइंडर {'चालू' if reminders else 'बंद'} किए गए!" if language == "hi" else
            f"✅ Reminders {'enabled' if reminders else 'disabled'}!",
            parse_mode="Markdown"
        )
        return None

    elif data.startswith("reset_"):
        keyboard = [
            [InlineKeyboardButton("✅ Yes" if language == "en" else "✅ हाँ", callback_data="confirm_reset_")],
            [InlineKeyboardButton("❌ No" if language == "en" else "❌ नहीं", callback_data="cancel_reset_")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            MESSAGES[language]["reset_prompt"],
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return None

    elif data.startswith("confirm_reset_"):
        update_user_data(user_id, {
            "history": [],
            "target": None,
            "stoploss": None,
            "start_date": None,
            "awaiting": None
        })
        await query.message.reply_text(
            "✅ सभी डेटा रीसेट कर दिए गए!\nनया लक्ष्य सेट करने के लिए /target का उपयोग करें।" if language == "hi" else
            "✅ All data has been reset!\nUse /target to set a new goal.",
            parse_mode="Markdown"
        )
        return None

    elif data.startswith("cancel_reset_"):
        await query.message.reply_text(
            MESSAGES[language]["cancel"],
            parse_mode="Markdown"
        )
        return None

    return None
