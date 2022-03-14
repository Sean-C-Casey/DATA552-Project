import os
from dotenv import load_dotenv

load_dotenv()

# Discord stuff
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Reddit stuff
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")