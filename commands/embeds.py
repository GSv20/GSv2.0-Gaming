import discord
from discord.ext import commands

class embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(())

def setup(bot):
    bot.add_cog(embeds(bot))