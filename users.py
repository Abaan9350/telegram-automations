import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


def save_user(user):
    cursor.execute("""
    INSERT INTO users (user_id, username, first_name)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        username = excluded.username,
        first_name = excluded.first_name,
        last_seen = CURRENT_TIMESTAMP
    """, (user.id, user.username, user.first_name))
    conn.commit()


def get_all_users():
    cursor.execute("""
    SELECT user_id, username, first_name, last_seen
    FROM users
    ORDER BY last_seen DESC
    """)
    return cursor.fetchall()