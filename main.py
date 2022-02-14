import logging
import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, TypeHandler
from dotenv import load_dotenv

# Setting up environment variables
load_dotenv()
BOT_API_TOKEN = os.environ.get('BOT_API_TOKEN')
GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN')
DROPBOX_API_TOKEN = os.environ.get('DROPBOX_API_TOKEN')

# Setting up Logging config
logging.basicConfig(
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Testing")


def track_users(update: Update, context: CallbackContext) -> None:
    """Store the user id of the incoming update, if any."""
    if update.effective_user:
        print(update.effective_user)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there")


def main():
    updater = Updater(BOT_API_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(TypeHandler(Update, track_users), group=-1)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
