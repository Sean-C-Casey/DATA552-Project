import asyncio
import logging
from discord.ext import commands

from settings import BOT_TOKEN, LOGGER_NAME, LOG_FILE
from reddit import RedditConnection


class NotificationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.reddit: RedditConnection
        self.logger = logging.getLogger(LOGGER_NAME)
    
    # Since RedditConnection must be awaited, which we can't do in constructor
    @commands.Cog.listener()
    async def on_ready(self):
        self.reddit = await RedditConnection.get_connection()
    
    @commands.command(name="ping")
    async def test(self, ctx: commands.Context) -> None:
        await ctx.send("Hello!")

    @commands.command(name="get-news")
    async def get_news(self, ctx: commands.Context) -> None:
        results = await self.reddit.get_top_n(3)
        result = results[0]
        msg = f"{result.url}\n\nReddit discussion: https://www.reddit.com{result.permalink}"
        await ctx.send(msg)


if __name__ == "__main__" and BOT_TOKEN is not None:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    log_handler = logging.FileHandler(
        filename=LOG_FILE, 
        encoding="utf-8", 
        mode="w"
    )
    log_handler.setFormatter(
        logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')
    )
    logger.addHandler(log_handler)

    bot = commands.Bot("!")
    cog = NotificationCog(bot)
    bot.add_cog(cog)
    bot.run(BOT_TOKEN)