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

            repo_string_list = [f'- {repo["full_name"]} : {repo["svn_url"]} \n' for repo in response]
            return ''.join(repo_string_list)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Unable to fetch the list of repos from GitHub {e}")
            return ""

    def get_pull_requests(self, repo: str) -> Union[Dict[str, str], List[Dict[str, Any]]]:
        try:
            url = self.indocom_github_pr_api_url.format(repo=repo)
            response = requests.get(url, auth=('user', self.api_token))
            response = response.json()
            return response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Unable to fetch the pr from of repo {repo} because {e}")
            return []

    def get_open_not_registered_pr(self, repo: str) -> Union[Dict[str, str], List[Dict[str, Any]]]:
        try:
            pr_table_name = "pull_request"
            pr_ids = self.database_client.execute_query(f'SELECT * FROM {pr_table_name} WHERE repo_name="{repo}"')
            pr_ids = list(map(lambda x: x[0], pr_ids))

            url = self.indocom_github_pr_api_url.format(repo=repo)
            response = requests.get(url, auth=('user', self.api_token))
            response = response.json()

            if 'message' in response and response['message'] == 'Not Found':
                return []

            return list(filter(lambda x: int(x["id"]) not in pr_ids, response))

        except Exception as e:
            self.logger.error(f"Unable to fetch the pr from of repo {repo} because {e}")
            return []
