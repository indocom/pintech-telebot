import logging
from typing import Any, Dict, List, Union

import requests

from database.database import MySQLClient


class GitHubClient:
    indocom_github_api_url = "https://api.github.com/users/indocom/repos"
    indocom_github_pr_api_url = "https://api.github.com/repos/{repo}/pulls"

    def __init__(self, token, database: MySQLClient):
        self.api_token = token
        self.logger = logging.getLogger(__name__)
        self.database_client = database

    def get_repo_list(self) -> str:
        try:
            response = requests.get(self.indocom_github_api_url, auth=('user', self.api_token))
            response = response.json()

            if 'message' in response:
                self.logger.error(f"Unable to fetch repo list because {response['message']}")
                return ""

            repo_string_list = [f'- {repo["full_name"]} : {repo["svn_url"]} \n' for repo in response]
            return ''.join(repo_string_list)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Unable to fetch the list of repos from GitHub {e}")
            return ""

    def get_open_pr(self, repo: str, chat_id: str) -> Union[None, Dict[str, str], List[Dict[str, Any]]]:
        try:
            url = self.indocom_github_pr_api_url.format(repo=repo)
            response = requests.get(url, auth=('user', self.api_token))
            response = response.json()

            if 'message' in response:
                self.logger.error(f"Unable to fetch the pr from of repo {repo} because {response['message']}")
                return None

            return response

        except Exception as e:
            self.logger.error(f"Unable to fetch the pr from of repo {repo} because {e}")
            return None
