import logging
import pathlib
from discord.ext import commands

from settings import BOT_TOKEN


class NotificationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name="test")
    async def test(self, ctx: commands.Context) -> None:
        await ctx.send("Hello!")


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