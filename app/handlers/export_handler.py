# app/handlers/export_handler.py
import asyncio
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from app.utils.data_utils import get_user_data
from app.utils.export_utils import generate_excel_report
from app.config.messages import MESSAGES

async def export(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /export command, sending Excel report."""
    user_id = str(update.effective_user.id)
    user_data = await asyncio.to_thread(get_user_data, user_id)
    language = user_data.get("language", "en")

    report_buffer = await asyncio.to_thread(generate_excel_report, user_id)
    if not report_buffer:
        await update.message.reply_text(
            MESSAGES[language]["no_history"],
            parse_mode="Markdown"
        )
        return

    await update.message.reply_document(
        document=InputFile(report_buffer, filename="progress_report.xlsx"),
        caption=MESSAGES[language]["export_success"],
        parse_mode="Markdown"
    )
