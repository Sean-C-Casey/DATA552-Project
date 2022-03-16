import logging
import pathlib
from discord.ext import commands

from settings import BOT_TOKEN
from reddit import RedditConnection


class NotificationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.reddit = RedditConnection()
        self.last_post = None
    
    @commands.command(name="ping")
    async def test(self, ctx: commands.Context) -> None:
        await ctx.send("Hello!")

    @commands.command(name="get-news")
    async def get_news(self, ctx: commands.Context) -> None:
        results = self.reddit.get_top_n(3)
        result = results[0]
        msg = f"{result.url}\n\nReddit discussion: https://www.reddit.com{result.permalink}"
        await ctx.send(msg)


if __name__ == "__main__" and BOT_TOKEN is not None:
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    log_file = pathlib.Path(__file__).parent.joinpath("info.log")
    log_handler = logging.FileHandler(
        filename=log_file, 
        encoding="utf-8", 
        mode="w"
    )
    log_handler.setFormatter(
        logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')
    )
    logger.addHandler(log_handler)

    bot = commands.Bot("!")
    bot.add_cog(NotificationCog(bot))
    bot.run(BOT_TOKEN)