# app/handlers/status_handler.py
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from app.utils.data_utils import get_user_data
from app.utils.image_utils import generate_daily_profile_card
from app.utils.calculation_utils import calculate_progress
from app.config.constants import CURRENCY
from app.config.messages import MESSAGES
import telegram.error
import logging

logger = logging.getLogger(__name__)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command, showing progress summary and profile card."""
    user = update.effective_user
    user_id = str(user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    logger.info(f"Generating status for user {user_id} (language: {language})")

    # Call calculate_progress early
    progress_data = calculate_progress(user_data)

    # Handle Data Validation Errors
    if progress_data.get("error"):
        error_message_text = MESSAGES[language]["status_data_error"].format(error_details=progress_data["error"])
        await update.message.reply_text(error_message_text)
        return

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

    # Proceed with generating image if no data error
    try:
        # Pass progress_data to the image generation function
        daily_profile_card_bytes = generate_daily_profile_card(user_data, progress_data, profile_photo)
    except Exception as e:
        logger.error(f"Error generating profile card for user {user_id}: {e}", exc_info=True)
        daily_profile_card_bytes = None

    # Construct text_summary using progress_data
    text_summary = f"👤 {'नाम' if language == 'hi' else 'Name'}: {user_data.get('name', user.first_name)}\n"
    if user_data.get("target"): # Target still exists, so we can show target related info
        target_info = user_data["target"] # For mode, original rate display
        days_passed = progress_data["days_passed"] + 1
        text_summary += (
            f"📅 {'दिन' if language == 'hi' else 'Day'} {days_passed} • {'से शुरू' if language == 'hi' else 'Since'} {user_data.get('start_date', 'N/A')}\n"
            f"🎯 {'लक्ष्य' if language == 'hi' else 'Target'}: {user_data.get('currency', CURRENCY)}{progress_data['target_amount_val']:,.2f}\n"
            f"💰 {'शुरुआत' if language == 'hi' else 'Start'}: {user_data.get('currency', CURRENCY)}{progress_data['start_amount_val']:,.2f}\n"
            f"📈 {'दर' if language == 'hi' else 'Rate'}: {target_info['rate']}% {'per' if language == 'en' else 'प्रति'} {target_info['mode']}\n" # Display original rate and mode
            f"🎯 Today's {'Target' if language == 'en' else 'लक्ष्य'}: {user_data.get('currency', CURRENCY)}{progress_data['expected_balance']:,.2f}\n"
            f"💵 {'Profit Goal' if language == 'en' else 'लाभ लक्ष्य'}: {user_data.get('currency', CURRENCY)}{progress_data['today_profit_goal']:,.2f}\n"
            f"📉 {'Stop Loss' if language == 'en' else 'स्टॉप लॉस'}: {user_data.get('currency', CURRENCY)}{progress_data['stoploss_level']:,.2f if progress_data['stoploss_level'] is not None else (MESSAGES[language]['not_set'])}\n"
            f"💼 {'Closing Balance' if language == 'en' else 'क्लोजिंग बैलेंस'}: {user_data.get('currency', CURRENCY)}{progress_data['current_balance']:,.2f}\n"
            f"✅ {'Status' if language == 'en' else 'स्थिति'}: {progress_data['status_badge']}\n"
        )
        if progress_data["current_balance"] >= progress_data['target_amount_val']:
            text_summary += MESSAGES[language]["target_achieved"] + "\n"
    else: # This case should ideally be caught by progress_data['error'] == "No target set"
        text_summary += MESSAGES[language]["no_target"] + "\n"

    if daily_profile_card_bytes is None:
        # If already sent a data error message, this might be redundant or indicate a different issue.
        # The current logic will send status_image_error if card generation itself failed after valid data.
        await update.message.reply_text(MESSAGES[language]["status_image_error"])
    else:
        await update.message.reply_photo(
            photo=InputFile(daily_profile_card_bytes),
            caption=MESSAGES[language]["status_summary"] + "\n\n" + text_summary,
            parse_mode="Markdown"
        )
