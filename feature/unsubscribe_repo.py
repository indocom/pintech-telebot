from telegram.ext import CommandHandler

from feature.base_command import BaseCommand
from github.github_functionalities import unsubscribe_github_repo


class UnsubscribeRepoCommand(BaseCommand):
    @property
    def help_message(self):
        return "/unsubscribe_repo <REPO_FULL_NAME>: Unsubscribe repo, use /repo to get the repo full name. (e.g. " \
               "/unsubscribe_repo indocom/pinus-client) \n\n "

    @property
    def handler(self):
        return CommandHandler("unsubscribe_repo", unsubscribe_github_repo)
