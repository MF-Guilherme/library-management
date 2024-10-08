import psycopg2
from psycopg2 import sql
import os

db_password = os.getenv('DB_PASSWORD')

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="library",
            user="postgres",
            password=db_password,
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None