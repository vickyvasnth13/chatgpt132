import os
import logging
import openai
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

# Set logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# Define OpenAI API key
openai.api_key = os.getenv("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")

# Handle /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm your personal openai bot.")

# Generate response
async def generate_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get user message
    message = update.message.text

    #
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message}\n",
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    # Send message back
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Handle unknow command
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't understand your command.")

if __name__ == '__main__':
    # Set Telegram bot
    application = ApplicationBuilder().token(os.getenv("6217863695:AAGKfl6kDsblPL6_D3e5G8mAl66imDKWBgQ")).build()

    # /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Message handler
    generate_response_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), generate_response)
    application.add_handler(generate_response_handler)

    # Unknown command handler
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    # Start bot
    application.run_polling()