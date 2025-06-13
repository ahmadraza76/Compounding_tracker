# app/conversations/rate_mode_conversation.py
import asyncio
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.utils.data_utils import update_user_data, get_user_data
from app.config.constants import RATE_MODE
from app.config.messages import MESSAGES

async def handle_rate_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process rate and mode input."""
    user_id = str(update.effective_user.id)
    user_data = await asyncio.to_thread(get_user_data, user_id)
    language = user_data.get("language", "en")
    text = update.message.text.strip()

    try:
        rate, mode = [x.strip() for x in text.split(",")]
        rate = float(rate)
        mode = mode.lower()

        if rate <= 0:
            await update.message.reply_text(
                "❌ कृपया एक सकारात्मक दर दर्ज करें।" if language == "hi" else
                "❌ Please enter a positive rate.",
                parse_mode="Markdown"
            )
            return RATE_MODE

        if mode not in ["daily", "monthly"]:
            await update.message.reply_text(
                "❌ मोड 'daily' या 'monthly' होना चाहिए।" if language == "hi" else
                "❌ Mode must be 'daily' or 'monthly'.",
                parse_mode="Markdown"
            )
            return RATE_MODE

        if not user_data.get("target"):
            await update.message.reply_text(
                "❌ No target set first. Use /target to set one.",
                parse_mode="Markdown"
            )
            return ConversationHandler.END

        target = user_data["target"]
        target["rate"] = rate
        target["mode"] = mode

        await asyncio.to_thread(update_user_data, user_id, {
            "target": target,
            "awaiting": None
        })

        await update.message.reply_text(
            f"✅ दर {rate}% और मोड {mode} पर सेट किया गया!\nअपनी सेटिंग्स देखने के लिए /settings का उपयोग करें।" if language == "hi" else
            f"✅ Rate set to {rate}% and mode to {mode}!\nUse /settings to view your settings.",
            parse_mode="Markdown"
        )

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ Invalid format. Please follow the format: *rate, mode*\nExample: *5, daily*",
            parse_mode="Markdown"
        )
        return RATE_MODE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel rate and mode setting process."""
    user_id = str(update.effective_user.id)
    user_data = await asyncio.to_thread(get_user_data, user_id)
    language = user_data.get("language", "en")

    await asyncio.to_thread(update_user_data, user_id, {"awaiting": None})

    await update.message.reply_text(
        MESSAGES[language]["cancel"],
        parse_mode="Markdown"
    )

    return ConversationHandler.END