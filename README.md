# db-export-rest-api

This project provides a REST API to export data from a relational database into CSV files and log the execution details.  
It is implemented using **FastAPI**, **SQLAlchemy**, and **Pandas**.

All generated files (`exports` folder and `export.log`) are created relative to the location of the executable (or script) being run.

---

## Overview

The API exposes a single endpoint to:

1. Connect to a database.
2. Execute a predefined SQL `SELECT` query.
3. Write the results to a CSV file on disk.
4. Log the export details (file name, creation date, record count, and execution times) in a database table.

---

## Requirements

- Python 3.8+
- PostgreSQL (or any SQL database supported by SQLAlchemy)
- Python packages:
  ```bash
  pip install fastapi uvicorn sqlalchemy pandas psycopg2-binary
  ```
  
### Configuration

All configuration is stored in config.py.
You can modify these values to match your database, export folder, and API host/port.

### File Structure

db-export-rest-api/
├─ main.py           # FastAPI application
├─ export_db.py      # Export logic (SQL SELECT + CSV + logging)
├─ config.py         # Database and application configuration
├─ exports/          # CSV files will be saved here (auto-created)
└─ export.log        # Application log file (auto-created)


### Running the API

Start the API using: python main.py
Or using Uvicorn directly: uvicorn main:app --host 127.0.0.1 --port 8000

The API will start and listen on HOST:PORT

### Export Query

The predefined `SELECT` query used to retrieve data from the database is built in the `build_export_query` function in `export_db.py`.

### REST Endpoint

The service exposes a single endpoint for exporting data:

- **URL:** `/export`
- **Method:** `POST`
- **Description:** Calls the `export_users()` function, which executes the predefined SQL SELECT query, writes the results to a CSV file, and logs execution metadata in the database.

