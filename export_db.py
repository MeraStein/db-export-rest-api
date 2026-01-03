from sqlalchemy import create_engine, text
import pandas as pd
import time
from datetime import datetime
import os
from fastapi import HTTPException
from config import DB_DATA, EXPORT_DIR, LOG_TABLE
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("export.log"),
        logging.StreamHandler()
    ]
)

db_data_url = (
    f"{DB_DATA['type']}://{DB_DATA['user']}:{DB_DATA['password']}"
    f"@{DB_DATA['host']}:{DB_DATA['port']}/{DB_DATA['db_name']}"
)

# create engine with SQLAlchemy
engine = create_engine(db_data_url)

# -----------------------------
# FUNCTIONS
# -----------------------------

def ensure_log_table(table_name=LOG_TABLE):
    """Creates the log table if it doesn't exist yet."""
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        file_name VARCHAR(255) NOT NULL,
        date_created TIMESTAMP NOT NULL,
        record_count INT NOT NULL,
        select_time FLOAT NOT NULL,
        write_time FLOAT NOT NULL
    );
    """
    with engine.begin() as conn:
        conn.execute(text(create_table_sql))


def build_export_query():
    return """
        SELECT u.name, u.email, o.total_amount
        FROM users u
        JOIN orders o ON o.user_id = u.id;
    """


def export_users():
    try:
        logging.info("Starting export_users()")

        # create log table if not exists
        ensure_log_table()

        # run SELECT + measure time
        query = build_export_query()

        # SELECT and time it took to do it
        start_select = time.time()
        df = pd.read_sql(query, engine)
        select_time = time.time() - start_select
        logging.info(f"Selected {len(df)} rows in {select_time:.2f} seconds")

        # write CSV + measure time
        os.makedirs(EXPORT_DIR, exist_ok=True)
        file_name =  os.path.join(
                        EXPORT_DIR,
                        f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                    )

        start_write = time.time()
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            df.to_csv(f, index=False)
        write_time = time.time() - start_write
        logging.info(f"Wrote CSV '{file_name}' in {write_time:.2f} seconds")

        record_count = len(df)

        # insert log record
        insert_log_sql = f"""
        INSERT INTO {LOG_TABLE}
        (file_name, date_created, record_count, select_time, write_time)
        VALUES (:file_name, :date_created, :record_count, :select_time, :write_time)
        """

        with engine.begin() as conn:
            conn.execute(
                text(insert_log_sql),
                {
                    "file_name": file_name,
                    "date_created": datetime.now(),
                    "record_count": record_count,
                    "select_time": select_time,
                    "write_time": write_time
                }
            )

            return {
                "file_name": file_name,
                "record_count": record_count,
                "select_time": select_time,
                "write_time": write_time
            }

    except Exception as e:
        logging.error("Export failed", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
