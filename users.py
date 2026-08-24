import aiosqlite


async def _init_db():
    """Initialize the database schema if it doesn't exist."""
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        await db.commit()


# Initialize database on module import
import asyncio
try:
    asyncio.get_running_loop().create_task(_init_db())
except RuntimeError:
    # No event loop running yet, will be initialized on first use
    pass


async def save_user(user):
    # Ensure database is initialized
    try:
        await _init_db()
    except:
        pass

    async with aiosqlite.connect("users.db") as db:
        # Check if user already exists
        cursor = await db.execute(
            "SELECT 1 FROM users WHERE user_id = ?",
            (user.id,)
        )
        is_new = await cursor.fetchone() is None

        await db.execute("""
        INSERT INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_seen = CURRENT_TIMESTAMP
        """, (user.id, user.username, user.first_name))

        await db.commit()

        return is_new


async def get_all_users():
    async with aiosqlite.connect("users.db") as db:
        cursor = await db.execute("""
        SELECT user_id, username, first_name, last_seen
        FROM users
        ORDER BY last_seen DESC
        """)
        return await cursor.fetchall()