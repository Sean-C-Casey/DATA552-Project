import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

# Discord stuff
BOT_TOKEN = os.getenv("BOT_TOKEN")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", 24))  # Note: this is in hours!

# Reddit stuff
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

# Logging
LOGGER_NAME = "discord-bot"
LOG_FILE = os.getenv(
    "LOG_FILE", 
    default=str(pathlib.Path(__file__).parent.joinpath("info.log"))
)
