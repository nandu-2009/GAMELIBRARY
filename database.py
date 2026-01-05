import sqlite3
import hashlib

class Database:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            player TEXT PRIMARY KEY,
            wins INTEGER DEFAULT 0
        )
        """)

        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, username, password):
        hashed = self.hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
        return self.cursor.fetchone() is not None

    def create_user(self, username, password):
        try:
            hashed = self.hash_password(password)
            self.cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, hashed))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_player_score(self, player):
        self.cursor.execute("SELECT wins FROM scores WHERE player=?", (player,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def record_win(self, player):
        self.cursor.execute("""
        INSERT INTO scores(player, wins)
        VALUES (?, 1)
        ON CONFLICT(player)
        DO UPDATE SET wins = wins + 1
        """, (player,))
        self.conn.commit()

    def close(self):
        self.conn.close()