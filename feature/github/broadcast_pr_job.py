import logging

from telegram.ext import CallbackContext

from database.database import MySQLClient
from feature.base_job import BaseJob
from github.github import GitHubClient
from github.github_functionalities import GITHUB_API_TOKEN

github_telegram_map = {
    'simonjulianl': 'simonjulianl',
    'lauwsj': 'simonjulianl',
    'Amadeus-Winarto': 'amadeusw',
    'bernarduskrishna': 'Bernardus_Krishna',
    'CommanderW324': 'CwD324'
}


class BroadcastPrJob(BaseJob):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        database_name = 'telebot'
        self.database_client = MySQLClient(database_name)
        self.github_client = GitHubClient(GITHUB_API_TOKEN, self.database_client)

    @property
    def help_message(self):
        return f"Broadcast new pr every {self.interval} s from subscribed repos"

    def get_job(self):
        def broadcast_pull_requests(context: CallbackContext):
            table_name = "chat_repo"
            query = f'SELECT chat_id, repo_name FROM {table_name}'
            chat_repo_tuples = self.database_client.execute_query(query)
            for chat_id, repo_name in chat_repo_tuples:
                pull_requests = self.github_client.get_open_pr(repo_name, chat_id)
                filtered_prs = filter_sent_pr(chat_id, pull_requests, repo_name)

                try:
                    if pull_requests is not None and len(pull_requests) == 0:
                        clean_up_existing_pr_id(repo_name)

                    if len(filtered_prs) > 0:
                        populate_pr_id(filtered_prs, repo_name, chat_id)
                        context.bot.send_message(chat_id=chat_id, text=convert_pr_list_to_string(filtered_prs))
                        self.logger.info(f"PR from {repo_name} has been broadcast successfully to {chat_id}")

                except Exception as e:
                    self.logger.error(f"PR from {repo_name} has failed to be broadcast to {chat_id} because of {e}")

        def populate_pr_id(pull_requests, repo_name, chat_id):
            self.logger.info(f" Populating PRs of {repo_name} of {chat_id}, has {len(pull_requests)} PRs")

            pr_table_name = "pull_request"
            for pr in pull_requests:
                query = f'INSERT IGNORE INTO {pr_table_name} VALUES ({int(pr["id"])}, "{repo_name}", "{chat_id}")'
                self.database_client.execute_query(query)

        def clean_up_existing_pr_id(repo_name: str):
            self.logger.info(f"Cleaning up PR from {repo_name}")

            pr_table_name = "pull_request"
            query = f'DELETE FROM {pr_table_name} WHERE repo_name="{repo_name}"'
            self.database_client.execute_query(query)

        def convert_pr_list_to_string(pull_requests):
            return ''.join([
                f'New PR [opened by @{github_telegram_map.get(resp["user"]["login"], resp["user"]["login"])}] : {resp["title"]}\n'
                f'Link: {resp["html_url"]}\n'
                f'Reviewer : {get_reviewers(resp)} \n\n'
                for resp in pull_requests])

        def get_reviewers(pull_request):
            reviewer = ','.join(['@' + github_telegram_map.get(resp["login"], resp["login"]) for resp in
                                 pull_request["requested_reviewers"]])
            return reviewer

        def filter_sent_pr(chat_id, pull_requests, repo_name):
            pr_table_name = "pull_request"
            pr_ids = self.database_client.execute_query(
                f'SELECT * FROM {pr_table_name} WHERE repo_name="{repo_name}" AND chat_id="{chat_id}"')
            pr_ids = list(map(lambda x: x[0], pr_ids))
            filtered_prs = list(filter(lambda x: int(x["id"]) not in pr_ids, pull_requests))
            return filtered_prs

        return broadcast_pull_requests

    @property
    def interval(self):
        return 10
