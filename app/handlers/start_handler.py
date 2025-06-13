# app/handlers/start_handler.py
import asyncio
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from app.utils.data_utils import update_user_data, get_user_data
from app.utils.image_utils import generate_daily_profile_card
from app.utils.calculation_utils import calculate_progress # Added import
from app.config.messages import MESSAGES
import telegram.error

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command, initializing user and sending profile card."""
    user = update.effective_user
    user_id = str(user.id)
    user_data = await asyncio.to_thread(get_user_data, user_id)
    language = user_data.get("language", "en") # Language can be determined after first get_user_data

    if not user_data.get("name"): # Check if user is new or data wiped
        initial_user_setup = {
            "name": user.first_name,
            "language": language, # Preserve language if it was somehow set before name
            "currency": "₹",
            "reminders": True,
            "history": [],
            "target": None,
            "stoploss": None,
            "start_date": None
        }
        await asyncio.to_thread(update_user_data, user_id, initial_user_setup)
        user_data = await asyncio.to_thread(get_user_data, user_id) # Refresh user_data
        # Language might change if it was default 'en' and user had a different preference stored
        # but "name" was missing. For /start, this is usually initial setup.
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

    # Calculate progress data asynchronously
    # user_data should be up-to-date here from previous steps
    progress_data = await asyncio.to_thread(calculate_progress, user_data)

    # Generate profile card asynchronously
    # Note: generate_daily_profile_card expects (user_data, progress_data, profile_photo)
    daily_profile_card_bytes = await asyncio.to_thread(
        generate_daily_profile_card,
        user_data,
        progress_data,
        profile_photo
    )

    await update.message.reply_photo(
        photo=InputFile(daily_profile_card_bytes),
        caption=MESSAGES[language]["welcome"],
        parse_mode="Markdown"
    )
