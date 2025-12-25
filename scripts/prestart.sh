#!/bin/bash
set -e

# Wait for database to be ready
python << END
import socket
import time
import os

db_server = os.getenv("POSTGRES_SERVER", "db")
db_port = int(os.getenv("POSTGRES_PORT", 5432))

while True:
    try:
        with socket.create_connection((db_server, db_port), timeout=1):
            print("Database is ready!")
            break
    except (socket.error, socket.timeout):
        print("Waiting for database...")
        time.sleep(1)
END

# Run migrations
alembic upgrade head

# Some initial data could be added here
# python app/initial_data.py
