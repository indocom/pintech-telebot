from telegram.ext import CommandHandler

from feature.base_command import BaseCommand
from github.github_functionalities import subscribe_github_repo


class SubscribeRepoCommand(BaseCommand):
    @property
    def help_message(self):
        return "/subscribe_repo <REPO_FULL_NAME>: Unsubscribe repo, use /repo to get the repo full name. (e.g. " \
               "/subscribe_repo indocom/pinus-client) \n\n "

    @property
    def handler(self):
        return CommandHandler("subscribe_repo", subscribe_github_repo)
