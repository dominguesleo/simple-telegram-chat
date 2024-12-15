from telegram import Update
from telegram.ext import ContextTypes
from database import save_message
from ollama import ollama_request
from database import clear_history
from transcription import transcribe_audio

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    message = update.message.text
    response = ollama_request(user_id, message)
    save_message(user_id, username, message, response['message']['content'])
    await update.message.reply_text(response['message']['content'])

async def handle_audio_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    audio_bytes = await file.download_as_bytearray()

    try:
        message = transcribe_audio(audio_bytes)
    except Exception as e:
        await update.message.reply_text(f"Error al transcribir audio")
        return

    user_id = update.message.from_user.id
    username = update.message.from_user.username
    response = ollama_request(user_id, message)

    save_message(user_id, username, message, response['message']['content'])

    await update.message.reply_text(response['message']['content'])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Saludos, soy el maestro Yoda, un chatbot con inteligencia artificial, soy.\n"
        "Ayudarte puedo, preguntas haz.\n\n"
        "Comandos disponibles, estos son:\n"
        "/start - Iniciar la conversación\n"
        "/clear - Borrar el historial de chat"
    )
    await update.message.reply_text(welcome_text)

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    clear_history(user_id)
    await update.message.reply_text("Historial de chat borrado para tu usuario.")