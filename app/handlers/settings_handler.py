# app/handlers/settings_handler.py
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.utils.data_utils import get_user_data
from app.config.constants import CURRENCY
from app.config.messages import MESSAGES

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display settings menu with inline buttons."""
    user_id = str(update.effective_user.id)
    user_data = await asyncio.to_thread(get_user_data, user_id)
    language = user_data.get("language", "en")

    settings_summary = f"⚙️ *{'सेटिंग्स' if language == 'hi' else 'Settings'}*\n\n"
    settings_summary += f"👤 {'नाम' if language == 'hi' else 'Name'}: {user_data.get('name', 'Not set')}\n"
    settings_summary += f"💰 {'मुद्रा' if language == 'hi' else 'Currency'}: {user_data.get('currency', CURRENCY)}\n"
    settings_summary += f"📉 {'स्टॉप-लॉस' if language == 'hi' else 'Stop-Loss'}: {user_data.get('stoploss', 'Not set')}%\n"
    settings_summary += f"⏰ {'रिमाइंडर' if language == 'hi' else 'Reminders'}: {'चालू' if language == 'hi' else 'Enabled' if user_data.get('reminders', False) else 'बंद' if language == 'hi' else 'Disabled'}\n"

    keyboard = [
        [InlineKeyboardButton("🎯 Edit Target" if language == "en" else "🎯 लक्ष्य संपादित करें", callback_data="edit_target_")],
        [InlineKeyboardButton("📉 Edit Stop-Loss" if language == "en" else "📉 स्टॉप-लॉस संपादित करें", callback_data="edit_stoploss_")],
        [InlineKeyboardButton("👤 Edit Name" if language == "en" else "👤 नाम संपादित करें", callback_data="edit_name_")],
        [InlineKeyboardButton("📈 Edit Rate/Mode" if language == "en" else "📈 दर/मोड संपादित करें", callback_data="edit_rate_mode_")],
        [InlineKeyboardButton("💰 Edit Currency" if language == "en" else "💰 मुद्रा संपादित करें", callback_data="edit_currency_")],
        [InlineKeyboardButton("💼 Update Balance" if language == "en" else "💼 बैलेंस अपडेट करें", callback_data="update_balance_")],
        [InlineKeyboardButton(f"⏰ {'Disable' if user_data.get('reminders', False) else 'Enable'} Reminders" if language == "en" else f"⏰ रिमाइंडर {'बंद' if user_data.get('reminders', False) else 'चालू'} करें", callback_data="toggle_reminders_")],
        [InlineKeyboardButton("🔄 Reset All Data" if language == "en" else "🔄 सभी डेटा रीसेट करें", callback_data="reset_")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        settings_summary + "\n" + MESSAGES[language]["settings_prompt"],
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
