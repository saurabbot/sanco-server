#!/bin/bash
set -e

# Wait for database to be ready
python << END
import socket
import time
import os

db_server = os.getenv("POSTGRES_SERVER", "db")
db_port = int(os.getenv("POSTGRES_PORT", 5432))

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

for name, host, port in [("PostgreSQL", db_server, db_port), ("Redis", redis_host, redis_port)]:
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"{name} is ready!")
                break
        except (socket.error, socket.timeout):
            print(f"Waiting for {name}...")
            time.sleep(1)
END

# Run migrations
alembic upgrade head

# Some initial data could be added here
# python app/initial_data.py
