import logging
import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from database import init_db
from telegram_handler import handle_text_message, handle_audio_message, start, clear

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Initialize database
    init_db()

    # Create the application builder
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_audio_message))

    # Run the bot
    application.run_polling()

