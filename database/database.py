import logging
import os
from typing import List, Tuple

import mysql.connector
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class MySQLClient:
    def __init__(self, database: str):
        load_dotenv()
        mysql_endpoint = "telebot-1.ctonbvirgbl3.ap-southeast-1.rds.amazonaws.com"
        mysql_username = "pintech_admin"
        mysql_password = "pintechtelebotadmin"

        try:
            mydb = mysql.connector.connect(
                host=mysql_endpoint,
                user=mysql_username,
                password=mysql_password,
                database=database
            )

            self.mydb = mydb
        except Exception as e:
            logging.error(f"Error retrieving database {e}")

    def execute_query(self, query: str) -> List[Tuple]:
        cursor = self.mydb.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self.mydb.commit()

        return [line for line in result]
