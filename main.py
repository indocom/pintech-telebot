import logging

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from feature.features_list import COMMANDS, JOBS
from misc_handlers import handle_unknown_command, handle_help_message

is_started = False


def main():
    global is_started
    BOT_API_TOKEN = "5268775728:AAH6avGSH9fIRNk_caGwHtwwCgRXfLOLNRI"  # Prod Bot
    # BOT_API_TOKEN = "5235631374:AAFPGWzqTcFt3xEAS3reNoQO0ACD2rdfxkU"  # Testing Bot

    set_logging()

    if not is_started:
        updater = Updater(BOT_API_TOKEN)

        set_up_jobs(updater)

        dispatcher = updater.dispatcher
        set_up_handlers(dispatcher)

        logger.info("Start polling")
        updater.start_polling()
        is_started = True


def set_logging():
    global logger
    logging.basicConfig(
        format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)


def set_up_jobs(updater):
    for job in JOBS:
        updater.job_queue.run_repeating(job.get_job(), interval=job.interval, first=0)


def set_up_handlers(dispatcher):
    for command in COMMANDS:
        dispatcher.add_handler(command.handler)
    dispatcher.add_handler(CommandHandler("help", handle_help_message))
    dispatcher.add_handler(MessageHandler(Filters.command, handle_unknown_command))
