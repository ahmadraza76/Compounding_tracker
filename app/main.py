import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# app/main.py
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.handlers.start_handler import start
from app.handlers.target_handler import set_target
from app.handlers.close_handler import close_balance
from app.handlers.status_handler import status
from app.handlers.settings_handler import settings
from app.handlers.reset_handler import reset
from app.handlers.broadcast_handler import broadcast
from app.handlers.export_handler import export
from app.handlers.language_handler import set_language
from app.handlers.help_handler import help_command
from app.handlers.callback_handler import handle_settings_callback
from app.conversations.target_conversation import handle_target_input, cancel_callback as target_cancel
from app.conversations.close_conversation import handle_closing_input, cancel as close_cancel
from app.conversations.stoploss_conversation import handle_stoploss_input, cancel as stoploss_cancel
from app.conversations.name_conversation import handle_name_input, cancel as name_cancel
from app.conversations.rate_mode_conversation import handle_rate_input, cancel as rate_mode_cancel
from app.conversations.currency_conversation import handle_currency_input, cancel as currency_cancel
from app.conversations.broadcast_conversation import handle_broadcast_input, cancel as broadcast_cancel
from app.conversations.language_conversation import handle_language_input, cancel as language_cancel
from app.utils.reminder_utils import schedule_reminders
from app.utils.data_utils import get_user_data
from app.config.constants import TARGET, CLOSING, STOPLOSS, NAME, RATE_MODE, CURRENCY_CHANGE, BROADCAST, LANGUAGE
from app.config.messages import MESSAGES

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    try:
        user_id = str(update.effective_user.id)
        user_data = get_user_data(user_id)
        language = user_data.get("language", "en")
        await update.message.reply_text(
            MESSAGES[language]["unknown_command"],
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error in unknown_command handler: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    # Try to send error message to user if possible
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ Sorry, something went wrong. Please try again later.",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Could not send error message to user: {e}")

def main() -> None:
    """Initialize and run the bot."""
    try:
        load_dotenv()
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment")

        logger.info("Starting Compounding Tracker Bot...")

        # Create application
        application = Application.builder().token(bot_token).build()

        # Add error handler
        application.add_error_handler(error_handler)

        # Command Handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("status", status))
        application.add_handler(CommandHandler("settings", settings))
        application.add_handler(CommandHandler("reset", reset))
        application.add_handler(CommandHandler("export", export))
        application.add_handler(CommandHandler("help", help_command))

        # Conversation Handlers
        target_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("target", set_target), CallbackQueryHandler(handle_settings_callback, pattern="^edit_target_")],
            states={TARGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_target_input)]},
            fallbacks=[CommandHandler("cancel", target_cancel)]
        )
        
        closing_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("close", close_balance), CallbackQueryHandler(handle_settings_callback, pattern="^update_balance_")],
            states={CLOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_closing_input)]},
            fallbacks=[CommandHandler("cancel", close_cancel)]
        )
        
        stoploss_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(handle_settings_callback, pattern="^edit_stoploss_")],
            states={STOPLOSS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_stoploss_input)]},
            fallbacks=[CommandHandler("cancel", stoploss_cancel)]
        )
        
        name_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(handle_settings_callback, pattern="^edit_name_")],
            states={NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_input)]},
            fallbacks=[CommandHandler("cancel", name_cancel)]
        )
        
        rate_mode_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(handle_settings_callback, pattern="^edit_rate_mode_")],
            states={RATE_MODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_rate_input)]},
            fallbacks=[CommandHandler("cancel", rate_mode_cancel)]
        )
        
        currency_conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(handle_settings_callback, pattern="^edit_currency_")],
            states={CURRENCY_CHANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_currency_input)]},
            fallbacks=[CommandHandler("cancel", currency_cancel)]
        )
        
        broadcast_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("broadcast", broadcast)],
            states={BROADCAST: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_broadcast_input)]},
            fallbacks=[CommandHandler("cancel", broadcast_cancel)]
        )
        
        language_conv_handler = ConversationHandler(
            entry_points=[CommandHandler("language", set_language)],
            states={LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language_input)]},
            fallbacks=[CommandHandler("cancel", language_cancel)]
        )

        # Add all handlers
        application.add_handler(target_conv_handler)
        application.add_handler(closing_conv_handler)
        application.add_handler(stoploss_conv_handler)
        application.add_handler(name_conv_handler)
        application.add_handler(rate_mode_conv_handler)
        application.add_handler(currency_conv_handler)
        application.add_handler(broadcast_conv_handler)
        application.add_handler(language_conv_handler)
        application.add_handler(CallbackQueryHandler(handle_settings_callback, pattern="^(edit_|toggle_|reset_|confirm_|cancel_)"))
        application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

        # Schedule Reminders
        try:
            scheduler = AsyncIOScheduler()
            schedule_reminders(scheduler, application)
            scheduler.start()
            logger.info("Scheduler started successfully")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")

        # Start Bot
        logger.info("Bot started successfully! Listening for messages...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()