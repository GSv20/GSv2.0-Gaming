import asyncio
import discord
from discord.commands import Option
from discord.ext import commands
from discord.utils import format_dt
from discord.ui import View, Button


class Boosttime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.premium_since is None and after.premium_since is not None:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            booster = after
            embed = discord.Embed(title='', description=f'Vielen Dank, {booster.mention}, dass du den Server geboostet hast! Wir schätzen deine Unterstützung!', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            channel_id = 1073701634863009933
            channel = self.bot.get_channel(channel_id)

            if channel is not None:
                await channel.send(file=file, embed=embed)

    @commands.slash_command(name="boostzeit", description="🚀〢 Zeigt dir deine Boostzeit an!")
    async def boostime(self, ctx, member: Option(discord.Member, "Wähle ein Server-Mitglied aus!", required=False) = None):
        user = member or ctx.author
        boostzeit = user.premium_since
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(title='❌ | Error', description='**Bots können keine Server boosten!**', color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        if user.bot:
            await ctx.respond(file=file, embed=embed)
            return
        if user not in ctx.guild.members:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='❌ | Error', description='**Dieser User ist leider nicht in GSv2.0**', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=embed)
            return

        if boostzeit is None:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='❌ | Error', description='**`❌` | Dieser User hat noch nicht geboostet!**',
                                  color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=embed)
            return
        else:
            boostzeit_formatted = format_dt(boostzeit, style="R")
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='❌ | Error', description=f"**`🚀` | {user.mention} hat das Server Boosting auf diesem Server {boostzeit_formatted} gestartet!**", color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=embed)


class button(View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)

        @discord.ui.button(label='join GSv clan', style=discord.ButtonStyle.blurple, custom_id='join')
        async def action_button_pressed(self, button: Button, interaction: discord.Interaction):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            role = 1026556535909929040
            embed = discord.Embed(title='<a:party_blob:1073701093101551676> Willkommen im GSv clan', description='Du hast damit nun viele coole Extra rechte auf dem Discord und Zugriff zu exklusiven channels\n'
                                                                                                                 'wir wünschen viel spaß <3', colour=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.user.add_roles(role)
            asyncio.sleep(1)
            await interaction.respond(file=file, embed=embed)


def setup(bot):
    bot.add_cog(Boosttime(bot))
