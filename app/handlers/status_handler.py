# app/handlers/status_handler.py
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from app.utils.data_utils import get_user_data
from app.utils.image_utils import generate_daily_profile_card
from app.utils.calculation_utils import calculate_progress
from app.config.constants import CURRENCY
from app.config.messages import MESSAGES
import telegram.error

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command, showing progress summary and profile card."""
    user = update.effective_user
    user_id = str(user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    profile_photo = None
    try:
        photos = await context.bot.get_user_profile_photos(user_id, limit=1)
        if photos.photos and photos.photos[0]:
            file = await photos.photos[0][-1].get_file()
            profile_photo = await file.download_as_bytearray()
    except telegram.error.NetworkError:
        print(f"Network error fetching profile photo for user {user_id}")
    except Exception as e:
        print(f"Error fetching profile photo for user {user_id}: {str(e)}")

    daily_profile_card = generate_daily_profile_card(user_data, profile_photo)

    text_summary = f"👤 {'नाम' if language == 'hi' else 'Name'}: {user_data.get('name', user.first_name)}\n"
    if user_data.get("target"):
        target = user_data["target"]
        progress = calculate_progress(user_data)
        days_passed = progress["days_passed"] + 1
        text_summary += (
            f"📅 {'दिन' if language == 'hi' else 'Day'} {days_passed} • {'से शुरू' if language == 'hi' else 'Since'} {user_data['start_date']}\n"
            f"🎯 {'लक्ष्य' if language == 'hi' else 'Target'}: {user_data.get('currency', CURRENCY)}{float(target['target_amount']):,.2f}\n"
            f"💰 {'शुरुआत' if language == 'hi' else 'Start'}: {user_data.get('currency', CURRENCY)}{float(target['start_amount']):,.2f}\n"
            f"📈 {'दर' if language == 'hi' else 'Rate'}: {target['rate']}% {'per' if language == 'en' else 'प्रति'} {target['mode']}\n"
            f"🎯 Today's {'Target' if language == 'en' else 'लक्ष्य'}: {user_data.get('currency', CURRENCY)}{progress['expected_balance']:,.2f}\n"
            f"💵 {'Profit Goal' if language == 'en' else 'लाभ लक्ष्य'}: {user_data.get('currency', CURRENCY)}{progress['today_profit_goal']:,.2f}\n"
            f"📉 {'Stop Loss' if language == 'en' else 'स्टॉप लॉस'}: {user_data.get('currency', CURRENCY)}{progress['stoploss_level']:,.2f if progress['stoploss_level'] else ('Not set' if language == 'en' else 'सेट नहीं')}\n"
            f"💼 {'Closing Balance' if language == 'en' else 'क्लोजिंग बैलेंस'}: {user_data.get('currency', CURRENCY)}{progress['current_balance']:,.2f}\n"
            f"✅ {'Status' if language == 'en' else 'स्थिति'}: {progress['status_badge']}\n"
        )
        if progress["current_balance"] >= float(target["target_amount"]):
            text_summary += MESSAGES[language]["target_achieved"] + "\n"
    else:
        text_summary += MESSAGES[language]["no_target"] + "\n"

    await update.message.reply_photo(
        photo=InputFile(daily_profile_card),
        caption=MESSAGES[language]["status_summary"] + "\n\n" + text_summary,
        parse_mode="Markdown"
    )
