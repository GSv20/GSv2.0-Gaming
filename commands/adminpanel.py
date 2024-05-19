import discord
from discord.ext import commands
import asyncio
import datetime


class PunishSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(description="Rufe das Admin Panel auf")
    @commands.has_role(1044557317947019264)
    async def punish(self, ctx, user: discord.Member, reason: str):
        overview_embed = discord.Embed(
            title=f"Wie möchtest du {user.name}#{user.discriminator} sanktionieren?",
            color=discord.Color.dark_red())
        overview_embed.add_field(name="", value=f" ", inline=False)
        overview_embed.add_field(name="joined server", value=user.joined_at.strftime("%d.%m.%Y %H:%M"), inline=True)
        overview_embed.add_field(name="account created", value=user.created_at.strftime("%d.%m.%Y %H:%M"), inline=True)
        overview_embed.add_field(name="Reason:", value=f"```{reason}```", inline=True)
        overview_embed.add_field(name="Was willst du mit ihm machen?", value=f" ", inline=False)
        overview_embed.set_thumbnail(url=user.avatar.url)
        overview_embed.set_footer(
            icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&",
            text="Powered by GSV ⚡")
        await ctx.send(embed=overview_embed, view=PunishView(reason, user, timeout=1800), delete_after=60)


class PunishView(discord.ui.View):
    def __init__(self, reason, user, timeout=1800):
        super().__init__()
        self.reason = reason
        self.user = user
        self.timeout = timeout

    async def log_action(self, action, executor):
        print(f"{executor} {action} {self.user} for reason: {self.reason}")

    @discord.ui.button(label="Ban", style=discord.ButtonStyle.red, custom_id="ban", emoji="🔨")
    async def ban(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        executor = interaction.user
        await self.log_action("banned", executor)
        await asyncio.sleep(5)
        await interaction.followup.send(f"{self.user.mention} wurde gebannt für `{self.reason}`", ephemeral=True)

    @discord.ui.button(label="Kick", style=discord.ButtonStyle.blurple, custom_id="kick", emoji="🚫")
    async def kick(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        executor = interaction.user
        await self.log_action("kicked", executor)
        await asyncio.sleep(5)
        await interaction.followup.send(f"{self.user.mention} wurde gekickt für `{self.reason}`", ephemeral=True)

    @discord.ui.button(label="Timeout", style=discord.ButtonStyle.blurple, custom_id="timeout", emoji="⌛")
    async def timeout(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        executor = interaction.user
        await self.log_action("timed out", executor)
        until = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.timeout)
        await asyncio.sleep(5)
        await interaction.followup.send(f"{self.user.mention} wurde timeout für `{self.reason}`", ephemeral=True)


def setup(bot):
    bot.add_cog(PunishSystem(bot))
