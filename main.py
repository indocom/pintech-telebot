import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters

from feature.commands import COMMANDS
from github.github_functionalities import broadcast_pull_requests
from misc_handlers import handle_unknown_command


def main():
    load_dotenv()
    BOT_API_TOKEN = os.environ.get('BOT_API_TOKEN')
    set_logging()

    updater = Updater(BOT_API_TOKEN)

    set_up_jobs(updater)

    dispatcher = updater.dispatcher
    set_up_handlers(dispatcher)

    updater.start_polling()
    updater.idle()


def set_logging():
    global logger
    logging.basicConfig(
        format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)


def set_up_jobs(updater):
    updater.job_queue.run_repeating(broadcast_pull_requests, interval=30, first=0)


def set_up_handlers(dispatcher):
    for command in COMMANDS:
        dispatcher.add_handler(command.handler)
    dispatcher.add_handler(MessageHandler(Filters.command, handle_unknown_command))


if __name__ == '__main__':
    main()
