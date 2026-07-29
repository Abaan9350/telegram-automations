import asyncio
from commands.epicgames import fetch_free_games

async def main():
    games = await fetch_free_games()

    print(f"Found {len(games)} free game(s):\n")

    for game in games:
        print(game["title"])
        print(game["url"])
        print("-" * 50)

asyncio.run(main())