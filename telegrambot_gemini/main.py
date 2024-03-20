import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import google.generativeai as genai

PORT = int(os.environ.get('PORT', 5000))
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_response(msg) :
    response = model.generate_content(
        msg,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7)
    )
    return response.text





def start(update, context):
    """Send a message when the command /start is issued."""
    bot = context.bot
    chat_id = update.message.chat_id

    welcome = """Hello, 🌟Welcome the Gemini Bot """

    bot.send_message(chat_id=chat_id, text=welcome)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def user_message(update, context):
    bot = context.bot
    chat_id = update.message.chat_id

    user_input = update.message.text
    ai_output = generate_response(user_input)

    bot.send_message(chat_id=chat_id, text=ai_output)



def main():
    """Start the bot."""

    updater = Updater(bot_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, user_message))

    # log all errors
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
