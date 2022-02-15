from telegram.ext import CommandHandler

from feature.base_command import BaseCommand
from github.github_functionalities import get_subscribed_repo


class GetSubscribedRepoCommand(BaseCommand):
    @property
    def help_message(self):
        return "/check_subscribed_repo: Show list of all repositories that you have subscribed\n\n"

    @property
    def handler(self):
        return CommandHandler("check_subscribed_repo", get_subscribed_repo)
