import os
from urllib.parse import urlparse

import pymysql
import pymysql.cursors

DATABASE_URL = os.environ.get("DATABASE_URL", "")


def get_db_connection():
    parsed = urlparse(str(DATABASE_URL).strip())
    database_name = (parsed.path or "").lstrip("/")
    return pymysql.connect(
        host=parsed.hostname,
        port=parsed.port or 3306,
        user=parsed.username,
        password=parsed.password,
        database=database_name,
        cursorclass=pymysql.cursors.DictCursor,
        ssl={"ssl": {}},
    )


def init_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        conn.commit()
    finally:
        conn.close()


def create_user(username, email, password_hash):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash),
            )
        conn.commit()
        return True
    except pymysql.IntegrityError:
        conn.rollback()
        return False
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cur.fetchone()
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cur.fetchone()
    finally:
        conn.close()
