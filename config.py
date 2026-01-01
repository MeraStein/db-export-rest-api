import os

DB_DATA = {
    "type": "postgresql+psycopg2",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432",
    "db_name": "my_test_db"
}

EXPORT_DIR = "exports"
LOG_TABLE = "export_log"

HOST = os.getenv("APP_HOST", "127.0.0.1")
PORT = int(os.getenv("APP_PORT", 8000))