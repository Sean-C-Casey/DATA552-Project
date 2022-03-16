import logging
import discord
from discord.ext import commands, tasks

from settings import BOT_TOKEN, LOGGER_NAME, LOG_FILE, UPDATE_INTERVAL
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
        self.monitor_news.start()
    
    @commands.command(name="ping")
    async def test(self, ctx: commands.Context) -> None:
        log_msg = f"Pinged by user {ctx.author}"
        self.logger.info(log_msg)
        print(log_msg)
        await ctx.send("Hello!")

    @commands.command(name="get-news")
    async def get_news(self, ctx: commands.Context) -> None:
        results = await self.reddit.get_top_n(3)
        result = results[0]
        msg = f"{result.url}\n\nReddit discussion: https://www.reddit.com{result.permalink}"
        await ctx.send(msg)
    
    @tasks.loop(hours=UPDATE_INTERVAL)
    async def monitor_news(self) -> None:
        server: discord.Guild = self.bot.get_guild(952745969391386625)
        if server is None:
            self.logger.error("Could not find notification server")
            print("WTF!")
        channel: discord.TextChannel = discord.utils.get(server.channels, name="dev")
        results = await self.reddit.get_top_n(3)
        result = results[0]
        msg = f"{result.url}\n\nReddit discussion: https://www.reddit.com{result.permalink}"
        await channel.send(msg)
    
    @monitor_news.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()
        self.logger.info("Beginning news monitoring loop")


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