import random

from telegram import Update
from telegram.ext import MessageHandler, Filters

from feature.base_command import BaseCommand


class ReplyKudoMessage(BaseCommand):
    def __init__(self):
        self.messages = [
            "Sick Beast!",
            "Teamwork!",
            "Aye aye boi",
            "Sugoi des",
            "Subarashi",
            "Hen Hao!",
            "Good boi!"
        ]

    @property
    def help_message(self):
        return "@{tele_username}++ {description} to give kudo, more features coming soon!\n\n"

    @property
    def handler(self):
        def reply_kudo(update: Update, _) -> None:
            text = update.message.text
            list_of_words = text.split(' ')
            first_word = list_of_words[0]
            if first_word[-2:] == "++":
                username = first_word[:-2]
                message = ' '.join(list_of_words[1:]) if len(list_of_words) > 1 else random.choice(self.messages)
                message = username + " " + message
                update.message.reply_text(message)

        return MessageHandler(Filters.text & ~Filters.command, reply_kudo)
