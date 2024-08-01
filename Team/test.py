import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import datetime
from discord import ButtonStyle
from discord.ext.commands.cooldowns import CooldownMapping
from main import connect_execute


class Teampanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.mdb = "Data/mod_sys.db"

    @commands.Cog.listener()
    async def on_ready(self):
        await connect_execute(self.bot.mdb, """
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
        squad = member.public_flags

        if squad.hypesquad_bravery:
            squad = "House of Bravery"
        elif squad.hypesquad_brilliance:
            squad = "House of Brilliance"
        elif squad.hypesquad_balance:
            squad = "House of Balance"
        else:
            squad = "None"

        embed = discord.Embed(
            title=f"{member.name} | AdminPanel",
            description=(
                f"`👥 User Name` - {member.name} \n `🆔 User ID` - {member.id} \n `👥 Display/Server name` - {member.display_name} \n "
                f"`⏰ Created At` - <t:{int(member.created_at.timestamp())}:R> \n `⏰ Joined At` - <t:{int(member.joined_at.timestamp())}:R> \n"
                f"`🪪 Hypersquad` {squad} \n `📢 Mention` - {member.mention} \n `🔗 Avatar Url` - [Click Here]({member.display_avatar.url})"),
            color=0x2596be)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.respond(file=file, embed=embed, view=AdminView(member, reason), ephemeral=True)

    @slash_command(description="Lösche Nachrichten aus dem Channel")
    @commands.has_permissions(administrator=True)
    @discord.guild_only()
    async def purge(self, ctx, amount: Option(int, "Anzahl an Nachrichten (min. 1 | max. 100)", required=True)):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        if amount > 100:
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
            success_embed = discord.Embed(
                title="`✅` Erfolgreich!",
                description=f"**{len(deleted)}** `Nachrichten gelöscht!`",
                color=0x2596be)
            success_embed.set_thumbnail(url=ctx.guild.icon.url)
            success_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            success_embed.set_author(name=f"Purge | GSv2.0", icon_url=ctx.bot.user.avatar.url)
            await ctx.respond(file=file2, embed=success_embed, delete_after=10, ephemeral=True)

    @slash_command(description="Zeige alle Warns eines Users aus dem Server an")
    @commands.has_role(1044557317947019264)
    @discord.guild_only()
    async def warnings(self, ctx, member: discord.Member):
        warns_info = []
        rows = await connect_execute(self.bot.mdb,
                                     "SELECT warn_id, mod_id, warn_reason, warn_time FROM WarnList WHERE user_id = ? AND guild_id = ?",
                                     (member.id, ctx.guild.id), datatype="All")
        for row in rows:
            warn_id, mod_id, warn_reason, warn_time = row
            warn_time = datetime.datetime.strptime(warn_time, '%Y-%m-%d %H:%M:%S')
            warns_info.append((
                              f"**Warn-ID:** __{warn_id}__ | **Warn ausgestellt am:** {warn_time.strftime('%Y-%m-%d %H:%M:%S')}",
                              f"**Moderator:** <@{mod_id}> | **Mod-ID**: __{mod_id}__",
                              f"**> Grund:**\n```{warn_reason}```"))

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        warnings_embed = discord.Embed(title=f"`⚠️` Warn Liste {member.name}")
        warnings_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        warnings_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)
        warnings_embed.set_thumbnail(url=member.avatar.url)

        if warns_info == []:
            warnings_embed.description = f"The user has no warns!"
            warnings_embed.color = discord.Color.red()

        else:
            warnings_embed.description = "__**Liste der Warns**__"
            warnings_embed.color = 0x2596be

            [warnings_embed.add_field(name=f"{warntime}", value=f"{mod}\n{reason}", inline=False) for
             warntime, mod, reason in warns_info]

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
    bot.add_cog(Teampanel(bot))


class AdminView(discord.ui.View):
    def __init__(self, member, reason):
        super().__init__()
        self.member = member
        self.reason = reason
        self.mdb = "Data/mod_sys.db"
        self.cooldown = CooldownMapping.from_cooldown(1, 300, commands.BucketType.member)

    @discord.ui.button(label="Warn", emoji="🚧")
    async def warn_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await connect_execute(self.mdb,
                              "INSERT INTO WarnList (user_id, guild_id, warns, warn_reason, mod_id, warn_time) VALUES (?, ?, ?, ?, ?, ?)",
                              (self.member.id, interaction.guild.id, 1, self.reason, interaction.user.id, warn_time))
        row = await connect_execute(self.mdb,
                                    "SELECT warn_id FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1",
                                    (self.member.id, interaction.guild.id), datatype="One")
        warn_id = row[0]

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        warnUser_embed = discord.Embed(
            title="`⚠️` Warn",
            description=f"Du wurdest auf dem Server **{interaction.guild.name}** verwarnt.",
            color=0x2596be,
            timestamp=datetime.datetime.now())
        warnUser_embed.add_field(name="Moderator:", value=f"```{interaction.user.name}```", inline=False)
        warnUser_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        warnUser_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        warnUser_embed.set_author(name=f"{interaction.guild.name}", icon_url=self.member.avatar.url)
        warnUser_embed.set_thumbnail(url=self.member.avatar.url)
        warnUser_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        warn_embed = discord.Embed(
            title="`✅` Warn",
            description=f"Du hast den User {self.member.mention} auf dem Server **{interaction.guild.name}** gewarnt.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now())
        warn_embed.add_field(name="Moderator:", value=f"```{interaction.user.name}```", inline=False)
        warn_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        warn_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        warn_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.user.avatar.url)
        warn_embed.set_thumbnail(url=self.member.avatar.url)
        warn_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        await self.member.send(file=file, embed=warnUser_embed)
        await interaction.respond(file=file, embed=warn_embed, ephemeral=False)

    @discord.ui.button(label="Unwarn", emoji="🍀")
    async def unwarn_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        warn_id = None  # Define warn_id variable
        row = await connect_execute(self.mdb,
                                    "SELECT warn_id FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1",
                                    (self.member.id, interaction.guild.id), datatype="One")
        warn_id = row[0]
        await connect_execute(self.mdb, "DELETE FROM WarnList WHERE user_id = ? AND guild_id = ? AND warn_id = ?",
                              (self.member.id, interaction.guild.id, warn_id))

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        unwarnUser_embed = discord.Embed(
            title="`🍀` Unwarn",
            description=f"Ein Warn von dir vom Server **{interaction.guild.name}** wurde zurückgezogen.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now())
        unwarnUser_embed.add_field(name="Moderator:", value=f"```{interaction.user.name}```", inline=False)
        unwarnUser_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        unwarnUser_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        unwarnUser_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.client.user.avatar.url)
        unwarnUser_embed.set_thumbnail(url=interaction.guild.icon.url)
        unwarnUser_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        unwarn_embed = discord.Embed(
            title=f"`✅` Unwarn",
            description=f"Du hast den {self.member.mention} aus dem Server **{interaction.guild.name}** unwarned.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now())
        unwarn_embed.add_field(name="Moderator:", value=f"```{interaction.user.name}```", inline=False)
        unwarn_embed.add_field(name="Warn ID:", value=f"```{warn_id}```", inline=False)
        unwarn_embed.add_field(name="Grund:", value=f"```{self.reason}```", inline=False)
        unwarn_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.client.user.avatar.url)
        unwarn_embed.set_thumbnail(url=self.member.avatar.url)
        unwarn_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        await self.member.send(file=file, embed=unwarnUser_embed)
        await interaction.respond(file=file, embed=unwarn_embed, ephemeral=False)

    @discord.ui.button(label="Timeout", emoji="⌛", style=ButtonStyle.secondary)
    async def timeout_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title='<:nope:1073700944941957291> | Error', color=0x2596be)
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        if self.member == interaction.guild.owner:
            embed.description = 'Der Owner kann nicht getimeouted werden'
        elif self.member == self.bot.user:
            embed.description = 'Ich kann nicht getimeouted werden'
        elif self.member == interaction.user:
            embed.description = 'Du kannst dich nicht selber timeouten'
        else:
            await self.member.timeout_for(datetime.timedelta(minutes=5))
            embed.title = ''
            embed.description = f'{self.member.mention} wurde getimeouted'

        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

    @discord.ui.button(label="Kick", emoji="🚫", style=ButtonStyle.danger)
    async def kick_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        embed = discord.Embed(title='<:nope:1073700944941957291> | Error', color=0x2596be)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        if self.member == self.guild.owner:
            embed.description = 'Der Owner kann nicht gekickt werden'
        elif self.member == self.bot.user:
            embed.description = 'Ich kann mich nicht kicken'
        elif self.member == interaction.user:
            embed.description = 'Du kannst dich nicht selber kicken'
        else:
            await self.member.kick(reason=f"wurde von {interaction.user.name} übers Admin panel gekickt")
            embed.title = ""
            embed.description = f"{self.member.name} wurde von {interaction.guild.name} gekickt"

        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

    @discord.ui.button(label="Ban", emoji="🔨", style=ButtonStyle.danger)
    async def ban_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        embed = discord.Embed(title='<:nope:1073700944941957291> | Error', color=0x2596be)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        if self.member == self.guild.owner:
            embed.description = 'Der Owner kann nicht gebannt werden!'
        elif self.member == self.bot.user:
            embed.description = 'Ich kann mich nicht bannen!'
        elif self.member == interaction.user:
            embed.description = 'Du kannst dich nicht selber bannen!'
        else:
            await self.member.ban(reason=f"wurde von {interaction.user.name} übers Admin panel gebannt")
            embed.title = ""
            embed.description = f"{self.member.name} wurde von {interaction.guild.name} gebannt"

        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)