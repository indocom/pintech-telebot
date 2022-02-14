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
        query = f'INSERT INTO {table_name} (chat_id, repo_name) VALUES ("{chat_id}", "{repo_name}")'
        database_client.execute_query(query)
        logger.info(f"{chat_id} has subscribed to {repo_name} successfully")
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
    except Exception as e:
        logger.error(f"Unable to unsubscribe to {repo_name} because of {e}")
        raise


def broadcast_pull_requests(context: CallbackContext):
    table_name = "chat_repo"
    query = f'SELECT chat_id, repo_name FROM {table_name}'
    chat_repo_tuples = database_client.execute_query(query)
    for chat_id, repo_name in chat_repo_tuples:
        pull_requests = github_client.get_open_not_registered_pr(repo_name)

        try:
            if len(pull_requests) == 0:
                clean_up_existing_pr_id(repo_name)
            else:
                populate_pr_id(pull_requests, repo_name)
                context.bot.send_message(chat_id=chat_id, text=convert_pr_list_to_string(pull_requests))
            logger.info(f"PR from {repo_name} has been broadcast successfully to {chat_id}")

        except Exception as e:
            logger.error(f"PR from {repo_name} has failed to be broadcast to {chat_id} because of {e}")


def populate_pr_id(pull_requests, repo_name):
    logger.info(f" Populating PRs of {repo_name}")

    pr_table_name = "pull_request"
    for pr in pull_requests:
        query = f'INSERT INTO {pr_table_name} VALUES ({int(pr["id"])}, "{repo_name}")'
        database_client.execute_query(query)


def clean_up_existing_pr_id(repo_name: str):
    logger.info(f"Cleaning up PR from {repo_name}")

    pr_table_name = "pull_request"
    query = f'DELETE FROM {pr_table_name} WHERE repo_name="{repo_name}"'
    database_client.execute_query(query)


def convert_pr_list_to_string(pull_requests):
    return ''.join([f'- {resp["title"]} : {resp["html_url"]} \n\n' for resp in pull_requests])
