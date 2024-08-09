import discord
from discord.ext import commands
import datetime

CHANID = 1218317295345074298


class Log(commands.Cog):
    color = 0x2596be

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_member_join")
    async def log_member_join(self, member):
        em = discord.Embed(
            title="Member Joined",
            description=f"**Nutzer**: {member.name}"
                        f'\r\n**Joined Server**: {member.joined_at.strftime("%d.%m.%Y %H:%M")}'
                        f'\r\n**Account Created**: {member.created_at.strftime("%d.%m.%Y %H:%M")}',
            color=self.color,
            timestamp=datetime.datetime.now())
        em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=file, embed=em)

    @commands.Cog.listener("on_guild_channel_create")
    async def log_on_guild_channel_create(self, channel):
        em = discord.Embed(
            title="Channel wurde erstellt",
            description=f"**Channel Erstellt**: {channel.mention}",
            color=self.color,
            timestamp=datetime.datetime.now())
        em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=file, embed=em)

    @commands.Cog.listener("on_guild_channel_delete")
    async def log_on_guild_channel_delete(self, channel):
        em = discord.Embed(
            title="Channel wurde gelöscht",
            description=f"**Channel wurde gelöscht**: {channel.mention}",
            color=self.color,
            timestamp=datetime.datetime.now())
        em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=file, embed=em)

    @commands.Cog.listener("on_member_update")
    async def log_update_member(self, before, after):
        if len(before.roles) > len(after.roles):
            role = next(role for role in before.roles if role not in after.roles)
            em = discord.Embed(
                title="Rollenänderung",
                description=f"**Name**: {before}\r\n**Entfernte Rolle:**: {role.name}",
                color=self.color,
                timestamp=datetime.datetime.now())

        elif len(after.roles) > len(before.roles):
            role = next(role for role in after.roles if role not in before.roles)
            em = discord.Embed(
                title="Rollenänderung",
                description=f"**Name**: {before}\r\n**Neue Rolle:**: {role.name}",
                color=self.color,
                timestamp=datetime.datetime.now())

        elif before.nick != after.nick:
            em = discord.Embed(
                title="Nickname wurde geändert!",
                description=f"**Name**: {before}\r\n**Alter NickName**: {before.nick}\r\n**Neuer NickName**: {after.nick}",
                color=self.color,
                timestamp=datetime.datetime.now())

        else:
            return

        em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=file, embed=em)

    @commands.Cog.listener("on_message_edit")
    async def log_edit_message(self, before, after):
        if after.author.bot:
            return
        em = discord.Embed(
            title="Messege Edit",
            description=f"**Bearbeitete Nachricht von**: {before.author}"
                        f"\r\n**Alte Nachricht**: {before.content}"
                        f"\r\n**Neue Nachricht**: {after.content}",
            color=self.color,
            timestamp=datetime.datetime.now())
        em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=file, embed=em)

    @commands.Cog.listener("on_message_delete")
    async def log_deleted_message(self, message):
        if message.author.bot:
            return
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(
            title="Message Delete",
            description=f"**Gelöschte Nachricht von**: {message.author}"
                        f"\r\n**Inhalt der Nachricht**: {message.content}"
                        f"\r\n**Im Channel**: {message.channel.mention}",
            color=color,
            timestamp=datetime.datetime.now())
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        if message.embeds:
            for i, embed_obj in enumerate(message.embeds, start=1):
                embed_title = f"Embed {i}" if len(message.embeds) > 1 else "Embed"

                embed_text = embed_obj.description if embed_obj.description else ""

                embed.add_field(name=f"--- {embed_title} ---", value=embed_text)

        channel = await self.bot.fetch_channel(CHANID)

        if channel:
            await channel.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(Log(bot))