import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "users.db")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def record_win(player):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scores(player, wins)
        VALUES (?, 1)
        ON CONFLICT(player)
        DO UPDATE SET wins = wins + 1
    """, (player,))
    conn.commit()
    conn.close()

def get_players():
    return sys.argv[1], sys.argv[2]

def get_players():
    return sys.argv[1], sys.argv[2]