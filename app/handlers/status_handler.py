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
import traceback

logger = logging.getLogger(__name__)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command, showing progress summary and profile card."""
    try:
        user = update.effective_user
        user_id = str(user.id)
        user_data = get_user_data(user_id)
        language = user_data.get("language", "en")

        logger.info(f"Processing status command for user {user_id}")

        # Check if user has target set
        if not user_data.get("target"):
            await update.message.reply_text(
                MESSAGES[language]["no_target"],
                parse_mode="Markdown"
            )
            return

        # Calculate progress data
        progress_data = calculate_progress(user_data)
        logger.info(f"Progress data calculated for user {user_id}: {progress_data}")

        # Handle Data Validation Errors
        if progress_data.get("error"):
            error_message_text = MESSAGES[language]["status_data_error"].format(error_details=progress_data["error"])
            await update.message.reply_text(error_message_text, parse_mode="Markdown")
            return

        # Try to get profile photo
        profile_photo = None
        try:
            photos = await context.bot.get_user_profile_photos(user_id, limit=1)
            if photos.photos and photos.photos[0]:
                file = await photos.photos[0][-1].get_file()
                profile_photo = await file.download_as_bytearray()
                logger.info(f"Profile photo downloaded for user {user_id}")
        except telegram.error.NetworkError:
            logger.warning(f"Network error fetching profile photo for user {user_id}")
        except Exception as e:
            logger.warning(f"Error fetching profile photo for user {user_id}: {str(e)}")

        # Generate profile card
        try:
            daily_profile_card_bytes = generate_daily_profile_card(user_data, progress_data, profile_photo)
            logger.info(f"Profile card generated successfully for user {user_id}")
        except Exception as e:
            logger.error(f"Error generating profile card for user {user_id}: {e}")
            logger.error(traceback.format_exc())
            # Send text-only status if image generation fails
            await send_text_status(update, user_data, progress_data, language)
            return

        # Construct text summary
        text_summary = build_status_summary(user_data, progress_data, language, user)

        # Send the profile card with caption
        try:
            await update.message.reply_photo(
                photo=InputFile(daily_profile_card_bytes),
                caption=MESSAGES[language]["status_summary"] + "\n\n" + text_summary,
                parse_mode="Markdown"
            )
            logger.info(f"Status card sent successfully to user {user_id}")
        except Exception as e:
            logger.error(f"Error sending photo to user {user_id}: {e}")
            # Fallback to text-only status
            await send_text_status(update, user_data, progress_data, language)

    except Exception as e:
        logger.error(f"Unexpected error in status handler for user {user_id}: {e}")
        logger.error(traceback.format_exc())
        try:
            await update.message.reply_text(
                "❌ Sorry, there was an error processing your status. Please try again later.",
                parse_mode="Markdown"
            )
        except:
            pass

async def send_text_status(update: Update, user_data: dict, progress_data: dict, language: str) -> None:
    """Send text-only status when image generation fails."""
    try:
        user = update.effective_user
        text_summary = build_status_summary(user_data, progress_data, language, user)
        
        await update.message.reply_text(
            MESSAGES[language]["status_summary"] + "\n\n" + text_summary,
            parse_mode="Markdown"
        )
        logger.info(f"Text-only status sent to user {user.id}")
    except Exception as e:
        logger.error(f"Error sending text status: {e}")

def build_status_summary(user_data: dict, progress_data: dict, language: str, user) -> str:
    """Build status summary text."""
    try:
        text_summary = f"👤 {'नाम' if language == 'hi' else 'Name'}: {user_data.get('name', user.first_name)}\n"
        
        if user_data.get("target"):
            target_info = user_data["target"]
            days_passed = progress_data["days_passed"] + 1
            currency = user_data.get('currency', CURRENCY)
            
            text_summary += (
                f"📅 {'दिन' if language == 'hi' else 'Day'} {days_passed} • {'से शुरू' if language == 'hi' else 'Since'} {user_data.get('start_date', 'N/A')}\n"
                f"🎯 {'लक्ष्य' if language == 'hi' else 'Target'}: {currency}{progress_data['target_amount_val']:,.2f}\n"
                f"💰 {'शुरुआत' if language == 'hi' else 'Start'}: {currency}{progress_data['start_amount_val']:,.2f}\n"
                f"📈 {'दर' if language == 'hi' else 'Rate'}: {target_info['rate']}% {'per' if language == 'en' else 'प्रति'} {target_info['mode']}\n"
                f"🎯 {'आज का लक्ष्य' if language == 'hi' else 'Today\\'s Target'}: {currency}{progress_data['expected_balance']:,.2f}\n"
                f"💵 {'लाभ लक्ष्य' if language == 'hi' else 'Profit Goal'}: {currency}{progress_data['today_profit_goal']:,.2f}\n"
                f"📉 {'स्टॉप लॉस' if language == 'hi' else 'Stop Loss'}: {currency}{progress_data['stoploss_level']:,.2f if progress_data['stoploss_level'] is not None else (MESSAGES[language]['not_set'])}\n"
                f"💼 {'वर्तमान बैलेंस' if language == 'hi' else 'Current Balance'}: {currency}{progress_data['current_balance']:,.2f}\n"
                f"✅ {'स्थिति' if language == 'hi' else 'Status'}: {progress_data['status_badge']}\n"
            )
            
            if progress_data["current_balance"] >= progress_data['target_amount_val']:
                text_summary += "\n" + MESSAGES[language]["target_achieved"] + "\n"
        else:
            text_summary += MESSAGES[language]["no_target"] + "\n"
            
        return text_summary
    except Exception as e:
        logger.error(f"Error building status summary: {e}")
        return "❌ Error building status summary"