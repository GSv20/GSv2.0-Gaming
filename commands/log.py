import discord
from discord.ext import commands
import datetime

ID = 1218317295345074298
class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await self.log_deleted_message(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.log_edit_message(before, after)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await self.log_update_member(before, after)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await self.log_on_guild_channel_create(channel)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await self.log_on_guild_channel_delete(channel)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.log_member_remove(member)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.log_member_join(member)

    async def log_member_remove(self, member):
        em = discord.Embed(
            title="Member Leave",
            description=f"**Nutzer**: {member.name}"
                        f'\r\n**Joined Server**: {member.joined_at.strftime("%d.%m.%Y %H:%M")}'
                        f'\r\n**Account Created**: {member.created_at.strftime("%d.%m.%Y %H:%M")}',
            color=discord.Color.dark_gold(),
            timestamp=datetime.datetime.utcnow(),)
        em.set_footer(text="Powered by GSV ⚡", icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')

        channel_id = ID
        channel = await self.bot.fetch_channel(channel_id)

        if channel:
            await channel.send(embed=em)

    async def log_member_join(self, member):
        em = discord.Embed(
            title="Member Joined",
            description=f"**Nutzer**: {member.name}"
                        f'\r\n**Joined Server**: {member.joined_at.strftime("%d.%m.%Y %H:%M")}'
                        f'\r\n**Account Created**: {member.created_at.strftime("%d.%m.%Y %H:%M")}',
            color=discord.Color.dark_gold(),
            timestamp=datetime.datetime.utcnow())
        em.set_footer(text="Powered by GSV ⚡",
                      icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')

        channel_id = ID
        channel = await self.bot.fetch_channel(channel_id)

        if channel:
            await channel.send(embed=em)

    async def log_on_guild_channel_create(self, channel):
        em = discord.Embed(
            title="Channel wurde erstellt",
            description=f"**Channel Erstellt**: {channel.mention}",
            color=discord.Color.dark_gold(),
            timestamp=datetime.datetime.utcnow())
        em.set_footer(text="Powered by GSV ⚡",
                      icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')

        channel_id = ID
        channel = await self.bot.fetch_channel(channel_id)

        if channel:
            await channel.send(embed=em)

    async def log_on_guild_channel_delete(self, channel):
        em = discord.Embed(
            title="Channel wurde gelöscht",
            description=f"**Channel wurde gelösch**: {channel.mention}",
            color=discord.Color.dark_gold(),
            timestamp=datetime.datetime.utcnow())
        em.set_footer(text="Powered by GSV ⚡",
                      icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')

        channel_id = ID
        channel = await self.bot.fetch_channel(channel_id)

        if channel:
            await channel.send(embed=em)

    async def log_update_member(self, before, after):
        if len(before.roles) > len(after.roles):
            role = next(role for role in before.roles if role not in after.roles)
            em = discord.Embed(
                title="Rollenänderung",
                description=f"**Name**: {before}\r\n**Entfernte Rolle:**: {role.name}",
                color=discord.Color.dark_gold(),
                timestamp=datetime.datetime.utcnow())
            em.set_footer(text="Powered by GSV ⚡",
                          icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')

        elif len(after.roles) > len(before.roles):
            role = next(role for role in after.roles if role not in before.roles)
            em = discord.Embed(
                title="Rollenänderung",
                description=f"**Name**: {before}\r\n**Neue Rolle:**: {role.name}",
                color=discord.Color.dark_gold(),
                timestamp=datetime.datetime.utcnow())
            em.set_footer(text="Powered by GSV ⚡",
                          icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')

        elif before.nick != after.nick:
            em = discord.Embed(
                title="Nickname wurde geändert!",
                description=f"**Name**: {before}\r\n**Alter NickName**: {before.nick}\r\n**Neuer NickName**: {after.nick}",
                color=discord.Color.dark_gold(),
                timestamp=datetime.datetime.utcnow())
            em.set_footer(text="Powered by GSV ⚡",
                          icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')

        else:
            return
        channel_id = ID
        channel = await self.bot.fetch_channel(channel_id)

        if channel:
            await channel.send(embed=em)

    async def log_edit_message(self, before, after):
        if after.author.bot:
            return
        em = discord.Embed(
            title="Messege Edit",
            description=f"**Bearbeitete Nachricht von**: {before.author}"
                        f"\r\n**Alte Nachricht**: {before.content}"
                        f"\r\n**Neue Nachricht**: {after.content}",
            color=discord.Color.dark_gold(),
            timestamp=datetime.datetime.utcnow())
        em.set_footer(text="Powered by GSV ⚡",
                      icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
        channel_id = ID
        channel = await self.bot.fetch_channel(channel_id)

        if channel:
            await channel.send(embed=em)

    async def log_deleted_message(self, message):
        if message.author.bot:
            return
        embed = discord.Embed(
            title="Message Delete",
            description=f"**Gelöschte Nachricht von**: {message.author}"
                        f"\r\n**Inhalt der Nachricht**: {message.content}"
                        f"\r\n**Im Channel**: {message.channel.mention}",
            color=discord.Color.dark_gold(),
            timestamp=discord.utils.utcnow())
        embed.set_footer(text="Powered by GSV ⚡",
                      icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')

        if message.embeds:
            for i, embed_obj in enumerate(message.embeds, start=1):
                embed_title = f"Embed {i}" if len(message.embeds) > 1 else "Embed"

                embed_text = self.extract_text_from_embed(embed_obj)

                embed.add_field(name=f"--- {embed_title} ---", value=embed_text)

        channel_id = ID
        channel = await self.bot.fetch_channel(channel_id)

        if channel:
            await channel.send(embed=embed)

    def extract_text_from_embed(self, embed):
        text = embed.description if embed.description else ""
        return text


def setup(bot):
    bot.add_cog(log(bot))