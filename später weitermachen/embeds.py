import discord
from discord.ext import commands

class embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='')
    async def embeds(self, ctx):
        
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be

        discord.Embed()

        await

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(())

def setup(bot):
    bot.add_cog(embeds(bot))