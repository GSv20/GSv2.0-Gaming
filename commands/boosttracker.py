import discord
from discord.commands import Option
from discord.ext import commands
from discord.utils import format_dt
# nachrichten in embeds coden
class Boostime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            booster = after
            nachricht = f"Vielen Dank, {booster.mention}, dass du den Server geboostet hast! Wir schätzen deine Unterstützung!"

            channel_id = 1073701634863009933  # Hier die ID des channel einfügen
            channel = self.bot.get_channel(channel_id)

            if channel is not None:
                await channel.send(nachricht)

    @commands.slash_command(name="boostzeit", description="🚀〢 Zeigt dir deine Boostzeit an!")
    async def boostime(self, ctx, member: Option(discord.Member, "Wähle ein Server-Mitglied aus!", required=False) = None):
        user = member or ctx.author
        boostzeit = user.premium_since

        if user.bot:
            await ctx.respond(content="**`❌` | Bots können keine Server boosten!**")
            return
        if user not in ctx.guild.members:
            await ctx.respond(content="**`❌` | Dieser User ist nicht auf diesem Server!**")
            return

        if boostzeit is None:
            await ctx.respond(content="**`❌` | Dieser User hat noch nicht geboostet!**")
            return
        else:
            boostzeit_formatted = format_dt(boostzeit, style="R")
            await ctx.respond(
                content=f"**`🚀` | {user.mention} hat das Server Boosting auf diesem Server {boostzeit_formatted} gestartet!**")

def setup(bot):
    bot.add_cog(Boostime(bot))