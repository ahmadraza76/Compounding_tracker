# app/handlers/start_handler.py
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from app.utils.data_utils import update_user_data, get_user_data
from app.utils.image_utils import generate_daily_profile_card
from app.config.messages import MESSAGES
import telegram.error

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command, initializing user and sending profile card."""
    user = update.effective_user
    user_id = str(user.id)
    user_data = get_user_data(user_id)
    language = user_data.get("language", "en")

    if not user_data.get("name"):
        update_user_data(user_id, {
            "name": user.first_name,
            "language": "en",
            "currency": "₹",
            "reminders": True,
            "history": [],
            "target": None,
            "stoploss": None,
            "start_date": None
        })

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

    daily_profile_card = generate_daily_profile_card(get_user_data(user_id), profile_photo)

    await update.message.reply_photo(
        photo=InputFile(daily_profile_card),
        caption=MESSAGES[language]["welcome"],
        parse_mode="Markdown"
    )
