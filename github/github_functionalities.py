import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext

from database.database import MySQLClient
from github.github import GitHubClient

logger = logging.getLogger(__name__)

load_dotenv()
GITHUB_API_TOKEN = "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"

database_name = 'telebot'
database_client = MySQLClient(database_name)
github_client = GitHubClient(GITHUB_API_TOKEN, database_client)

github_telegram_map = {
    'simonjulianl': 'simonjulianl',
    'lauwsj': 'simonjulianl',
    'Amadeus-Winarto': 'amadeusw',
    'bernarduskrishna': 'Bernardus_Krishna',
    'CommanderW324': 'CwD324'
}


def get_github_repo(update: Update, context: CallbackContext):
    repo_list_string = github_client.get_repo_list()
    context.bot.send_message(chat_id=update.effective_chat.id, text=repo_list_string)


def get_subscribed_repo(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    query = f'SELECT DISTINCT repo_name FROM chat_repo WHERE chat_id="{chat_id}"'
    repos = database_client.execute_query(query)
    repos_message = '\n'.join([repo[0] for repo in repos])
    context.bot.send_message(chat_id=chat_id, text=repos_message)


def subscribe_github_repo(update: Update, context: CallbackContext):
    table_name = "chat_repo"
    repo_name = context.args[0]
    chat_id = str(update.effective_chat.id)

    try:
        query = f'INSERT IGNORE INTO {table_name} (chat_id, repo_name) VALUES ("{chat_id}", "{repo_name}")'
        database_client.execute_query(query)
        logger.info(f"{chat_id} has subscribed to {repo_name} successfully")
        message = f"has subscribed to {repo_name} successfully"
        context.bot.send_message(chat_id=chat_id, text=message)

    except Exception as e:
        logger.error(f"Unable to subscribe to {repo_name} because of {e}")
        raise


def unsubscribe_github_repo(update: Update, context: CallbackContext):
    table_name = "chat_repo"
    repo_name = context.args[0]
    chat_id = str(update.effective_chat.id)

    try:
        query = f'DELETE FROM {table_name} WHERE "chat_id"="{chat_id}" AND "repo_name"="{repo_name}"'
        database_client.execute_query(query)
        logger.info(f"{chat_id} has unsubscribed to {repo_name} successfully")
        message = f"has unsubscribed to {repo_name} successfully"
        context.bot.send_message(chat_id=chat_id, text=message)

    except Exception as e:
        logger.error(f"Unable to unsubscribe to {repo_name} because of {e}")
        raise


def broadcast_pull_requests(context: CallbackContext):
    table_name = "chat_repo"
    query = f'SELECT chat_id, repo_name FROM {table_name}'
    chat_repo_tuples = database_client.execute_query(query)
    for chat_id, repo_name in chat_repo_tuples:
        pull_requests = github_client.get_open_pr(repo_name, chat_id)
        filtered_prs = filter_sent_pr(chat_id, pull_requests, repo_name)

        try:
            if pull_requests is not None and len(pull_requests) == 0:
                clean_up_existing_pr_id(repo_name)

            if len(filtered_prs) > 0:
                populate_pr_id(filtered_prs, repo_name, chat_id)
                context.bot.send_message(chat_id=chat_id, text=convert_pr_list_to_string(filtered_prs))
                logger.info(f"PR from {repo_name} has been broadcast successfully to {chat_id}")

        except Exception as e:
            logger.error(f"PR from {repo_name} has failed to be broadcast to {chat_id} because of {e}")


def filter_sent_pr(chat_id, pull_requests, repo_name):
    pr_table_name = "pull_request"
    pr_ids = database_client.execute_query(
        f'SELECT * FROM {pr_table_name} WHERE repo_name="{repo_name}" AND chat_id="{chat_id}"')
    pr_ids = list(map(lambda x: x[0], pr_ids))
    filtered_prs = list(filter(lambda x: int(x["id"]) not in pr_ids, pull_requests))
    return filtered_prs


def populate_pr_id(pull_requests, repo_name, chat_id):
    logger.info(f" Populating PRs of {repo_name} of {chat_id}, has {len(pull_requests)} PRs")

    pr_table_name = "pull_request"
    for pr in pull_requests:
        query = f'INSERT IGNORE INTO {pr_table_name} VALUES ({int(pr["id"])}, "{repo_name}", "{chat_id}")'
        database_client.execute_query(query)


def clean_up_existing_pr_id(repo_name: str):
    logger.info(f"Cleaning up PR from {repo_name}")

    pr_table_name = "pull_request"
    query = f'DELETE FROM {pr_table_name} WHERE repo_name="{repo_name}"'
    database_client.execute_query(query)


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
