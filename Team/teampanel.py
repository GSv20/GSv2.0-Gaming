import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import ezcord
import aiosqlite
import datetime
from discord import ButtonStyle
from discord.ext.commands.cooldowns import CooldownMapping

class teampanel(ezcord.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("Data/mod_sys.db") as db:
            await db.executescript("""
                CREATE TABLE IF NOT EXISTS WarnList (
                warn_id INTEGER PRIMARY KEY,
                mod_id INTEGER,
                guild_id INTEGER,
                user_id INTEGER,
                warns INTEGER DEFAULT 0,
                warn_reason TEXT,
                warn_time TEXT)""")

    @slash_command(description='Manage User sofern sie scheiße bauen (lol)')
    @commands.has_role(1044557317947019264)
    @discord.guild_only()
    async def teampanel(self, ctx, member: Option(discord.Member, required=True), reason: Option(str, required=True)):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        squad = member.public_flags

        if squad.hypesquad_bravery:
            squad = "House of Bravery"
        elif squad.hypesquad_brilliance:
            squad = "House of Brilliance"
        elif squad.hypesquad_balance:
            squad = "House of Balance"
        else:
            squad = "None"

        description = (f"`👥 User Name` - {member.name} \n `🆔 User ID` - {member.id} \n `👥 Display/Server name` - {member.display_name} \n "
                       f"`⏰ Created At` - <t:{int(member.created_at.timestamp())}:R> \n `⏰ Joined At` - <t:{int(member.joined_at.timestamp())}:R> \n"
                       f"`🪪 Hypersquad` {squad} \n `📢 Mention` - {member.mention} \n `🔗 Avatar Url` - [Click Here]({member.display_avatar.url})")

        embed = discord.Embed(
            title=f"{member.name} | AdminPanel",
            description=description,
            color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.respond(file=file, embed=embed, view=AdminView(self.bot, member, reason, ctx.guild, ctx), ephemeral=True)

    @slash_command(description="Lösche Nachrichten aus dem Channel")
    @commands.has_permissions(administrator=True)
    @discord.guild_only()
    async def purge(self, ctx, amount: Option(int, "Anzahl an Nachrichten (min. 1 | max. 100)", required=True)):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        amount += 1
        if amount > 101:
            error_embed = discord.Embed(
                title="`❌` Fehler!",
                description="`Ich kann nicht mehr als 100 Nachrichten löschen!`",
                color=discord.Color.dark_red())
            error_embed.set_thumbnail(url=ctx.guild.icon.url)
            error_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            error_embed.set_author(name=f"Purge | GSv2.0", icon_url=ctx.bot.user.avatar.url)

            await ctx.respond(file=file, embed=error_embed, delete_after=6, ephemeral=True)
        else:
            deleted = await ctx.channel.purge(limit=amount)
            file2 = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            success_embed = discord.Embed(
                title="`✅` Erfolgreich!",
                description=f"**{len(deleted)}** `Nachrichten gelöscht!`",
                color=color)
            success_embed.set_thumbnail(url=ctx.guild.icon.url)
            success_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            success_embed.set_author(name=f"Purge | GSv2.0", icon_url=ctx.bot.user.avatar.url)
            await ctx.respond(file=file2, embed=success_embed, delete_after=10, ephemeral=True)

    @slash_command(description="Zeige alle Warns eines Users aus dem Server an")
    @commands.has_role(1044557317947019264)
    @discord.guild_only()
    async def warnings(self, ctx, member: discord.Member):
        warns_info = []
        async with aiosqlite.connect("Data/mod_sys.db") as db:
            async with db.execute("SELECT warn_id, mod_id, guild_id, user_id, warns, warn_reason, warn_time FROM WarnList WHERE user_id = ? AND guild_id = ?",
                                  (member.id, ctx.guild.id)) as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    warn_id, mod_id, guild_id, user_id, warns, warn_reason, warn_time = row
                    warn_time = datetime.datetime.strptime(warn_time, '%Y-%m-%d %H:%M:%S')
                    warns_info.append(f"**Warn-ID:** __{warn_id}__ | **Warn ausgestellt am:** {warn_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    warns_info.append(f"**Moderator:** <@{mod_id}> | **Mod-ID**: __{mod_id}__\n")
                    warns_info.append(f"**> Grund:**\n```{warn_reason}```\n")

        if not warns_info:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            warnings_embed = discord.Embed(
                title="`⚠️` The user has no warns!",
                description=f"User: {member.mention}",
                color=discord.Color.red())
            warnings_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        else:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            warnings_embed = discord.Embed(
                title=f"`⚠️` Warn Liste {member.name}#{member.discriminator}",
                description=f"__**Liste der Warns**__",
                color=color)
            warnings_embed.add_field(name="", value="".join(warns_info), inline=False)
        warnings_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)
        warnings_embed.set_thumbnail(url=member.avatar.url)
        warnings_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.respond(file=file, embed=warnings_embed, ephemeral=False)

    @teampanel.error
    async def tickets_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title='Support Anfrage',
                               description="Leider ist dies eine Team Option\nWenn du Hilfe brauchst melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /teampanel auszuführen')

    @warnings.error
    async def tickets_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title='Support Anfrage',
                               description="Leider ist dies eine Team Option\nWenn du Hilfe brauchst melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /warnings auszuführen')

    @purge.error
    async def tickets_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title='Support Anfrage',
                               description="Leider ist dies eine Team Option\nWenn du Hilfe brauchst melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /purge auszuführen')

def setup(bot):
    bot.add_cog(teampanel(bot))


class AdminView(discord.ui.View):
    def __init__(self, bot, member, reason, guild, ctx):
        super().__init__()
        self.bot = bot
        self.member = member
        self.reason = reason
        self.guild = guild
        self.ctx = ctx
        self.cooldown = CooldownMapping.from_cooldown(1, 300, commands.BucketType.member)

    @discord.ui.button(label="Warn", emoji="🚧")
    async def warn_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with aiosqlite.connect("Data/mod_sys.db") as db:
            await db.execute(
                "INSERT INTO WarnList (user_id, guild_id, warns, warn_reason, mod_id, warn_time) VALUES (?, ?, ?, ?, ?, ?)",
                (self.member.id, self.ctx.guild.id, 1, self.reason, self.ctx.author.id, warn_time))
            await db.commit()

            async with db.execute(
                    "SELECT warn_id FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1",
                    (self.member.id, self.ctx.guild.id)) as cursor:
                row = await cursor.fetchone()
                warn_id = row[0]

        file1 = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        warnUser_embed = discord.Embed(
            title="`⚠️` Warn",
            description=f"Du wurdest auf dem Server **{self.ctx.guild.name}** gewarnt.",
            color=color,
            timestamp=datetime.datetime.utcnow())
        warnUser_embed.add_field(name="Moderator:", value=f"```{self.ctx.author}```", inline=False)
        warnUser_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        warnUser_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        warnUser_embed.set_author(name=f"{self.ctx.guild.name}", icon_url=self.member.avatar.url)
        warnUser_embed.set_thumbnail(url=self.member.avatar.url)
        warnUser_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        file2 = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        warn_embed = discord.Embed(
            title="`✅` Warn",
            description=f"Du hast den User {self.member.mention} auf dem Server **{self.ctx.guild.name}** gewarnt.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow())
        warn_embed.add_field(name="Moderator:", value=f"```{self.ctx.author}```", inline=False)
        warn_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        warn_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        warn_embed.set_author(name=f"{self.ctx.guild.name}", icon_url=self.ctx.user.avatar.url)
        warn_embed.set_thumbnail(url=self.member.avatar.url)
        warn_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        await self.member.send(file=file1, embed=warnUser_embed)
        await self.ctx.respond(file=file2, embed=warn_embed, ephemeral=False)

    @discord.ui.button(label="Unwarn", emoji="🍀")
    async def unwarn_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        warn_id = None  # Define warn_id variable
        async with aiosqlite.connect("Data/mod_sys.db") as db:
            async with db.execute(
                    "SELECT warn_id FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1",
                    (self.member.id, self.ctx.guild.id)) as cursor:
                row = await cursor.fetchone()
                warn_id = row[0]

            await db.execute("DELETE FROM WarnList WHERE user_id = ? AND guild_id = ? AND warn_id = ?",
                             (self.member.id, self.ctx.guild.id, warn_id))
            await db.commit()

        file1 = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        unwarnUser_embed = discord.Embed(
            title="`🍀` Unwarn",
            description=f"Ein Warn von dir vom Server **{self.ctx.guild.name}** wurde zurückgezogen.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow())
        unwarnUser_embed.add_field(name="Moderator:", value=f"```{self.ctx.author}```", inline=False)
        unwarnUser_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        unwarnUser_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        unwarnUser_embed.set_author(name=f"{self.ctx.guild.name}", icon_url=self.ctx.bot.user.avatar.url)
        unwarnUser_embed.set_thumbnail(url=self.ctx.guild.icon.url)
        unwarnUser_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        file2 = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        unwarn_embed = discord.Embed(
            title=f"`✅` Unwarn",
            description=f"Du hast den {self.member.mention} aus dem Server **{self.ctx.guild.name}** unwarned.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow())
        unwarn_embed.add_field(name="Moderator:", value=f"```{self.ctx.author}```", inline=False)
        unwarn_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        unwarn_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        unwarn_embed.set_author(name=f"{self.ctx.guild.name}", icon_url=self.ctx.bot.user.avatar.url)
        unwarn_embed.set_thumbnail(url=self.member.avatar.url)
        unwarnUser_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        await self.member.send(file=file1, embed=unwarnUser_embed)
        await self.ctx.respond(file=file2, embed=unwarn_embed, ephemeral=False)

    @discord.ui.button(label="Timeout", emoji="⌛", style=ButtonStyle.secondary)
    async def timeout_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await self.member.send(self.reason)
        except:
            print("Geht net")
        if self.member == self.guild.owner:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='<:nope:1073700944941957291> | Error', description='Der Owner kann nicht getimeouted werden', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            return await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
        elif self.member == self.bot.user:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed =discord.Embed(title='<:nope:1073700944941957291> | Error', description='Ich kann nicht getimeouted werden', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            return await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
        elif self.member == interaction.user:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='<:nope:1073700944941957291> | Error', description='Du kannst dich nicht selber timeouten', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            return await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
        else:
            await self.member.timeout_for(datetime.timedelta(minutes=5))
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='', description=f'{self.member.mention} wurde getimeouted', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

    @discord.ui.button(label="Kick", emoji="🚫", style=ButtonStyle.danger)
    async def kick_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await self.member.send(self.reason)
        except:
            print("Geht net")
        if self.member == self.guild.owner:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='<:nope:1073700944941957291> | Error', description='Der Owner kann nicht gekickt werden', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            return await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
        elif self.member == self.bot.user:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed =discord.Embed(title='<:nope:1073700944941957291> | Error', description='Ich kann mich nicht kicken', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            return await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
        elif self.member == interaction.user:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='<:nope:1073700944941957291> | Error', description='Du kannst dich nicht selber kicken', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            return await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
        await self.member.kick(reason=f"wurde von {interaction.user.name} übers Admin panel gekickt")

    @discord.ui.button(label="Ban", emoji="🔨", style=ButtonStyle.danger)
    async def ban_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await self.member.send(self.reason)
        except:
            print("Geht net")
        if self.member == self.guild.owner:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='<:nope:1073700944941957291> | Error', description='Der Owner kann nicht gebannt werden!', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            return await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
        elif self.member == self.bot.user:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed= discord.Embed(title='<:nope:1073700944941957291> | Error', description='Ich kann mich nicht bannen!', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            return await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
        elif self.member == interaction.user:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed= discord.Embed(title='<:nope:1073700944941957291> | Error', description='Du kannst dich nicht selber bannen!', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            return await interaction.response.send_message(file=file, embed=embed, ephemeral=True)
        await self.member.ban(reason=f"wurde von {interaction.user.name} übers Admin panel gebannt")