from telegram.ext import CommandHandler

from feature.base_command import BaseCommand
from github.github_functionalities import get_github_repo


class GetRepoCommand(BaseCommand):
    @property
    def help_message(self):
        return "/repo:  Show the list of all repositories inside github.com/indocom\n\n"

    @property
    def handler(self):
        return CommandHandler("list_repo", get_github_repo)
