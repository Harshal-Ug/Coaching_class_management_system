import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "2005"),
        database=os.getenv("MYSQL_DATABASE", os.getenv("MYSQL_DB", "coaching_db")),
    )


