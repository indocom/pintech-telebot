import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext

from database.database import MySQLClient
from github.github import GitHubClient

logger = logging.getLogger(__name__)

load_dotenv()
GITHUB_API_TOKEN = "wooe64XQkRqbL8d4bZvmSiY9hBkSg1nHtGGp_phg"[::-1]

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
