from telegram import Update
from telegram.ext import CallbackContext

from feature.commands import COMMANDS


def track_users(update: Update, context: CallbackContext):
    """
    Testing the metadata of each update
    > dispatcher.add_handler(TypeHandler(Update, track_users), group=-1)
    """
    if update.effective_user:
        pass


def handle_unknown_command(update: Update, context: CallbackContext):
    message = "What command is that UwU~"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def handle_help_message(update: Update, context: CallbackContext):
    text = "Hi, there! here is the list of commands available:\n\n"
    for command in COMMANDS:
        text += command.help_message

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
