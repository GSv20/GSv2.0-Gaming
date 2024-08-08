import asyncio
import datetime
import sys
import traceback
from discord.ext.commands.cooldowns import CooldownMapping
import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, Option
from discord import ButtonStyle
from .Adminsystem import connect_execute


class ModSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timeout_role_id = 1184593699523526696
        self.knast_role_id = self.timeout_role_id
        self.db_path = 'mod_sys.db'
        self.create_database()

    @tasks.loop(minutes=10)
    async def knastlist(self):
        guild = self.bot.get_guild(913082943495344179)
        channel = guild.get_channel(1234567890123456789)  # channel id für den channel wo die knastliste reinkommen soll
        users = await connect_execute("Data/knast.db", "SELECT uid, reason, mod_id FROM servers", datatype="All")
        knast_members = [(guild.get_member(user_id), reason, guild.get_member(mod_id)) for user_id, reason, mod_id in
                         users if guild.get_member(user_id)]

        embed = discord.Embed(
            title="Benutzer im Knast",
            color=discord.Color.red()
        )
        if knast_members != []:
            if users <= 25:
                [embed.add_field(name=member.name,
                                 value=f"Grund: {reason}\n\nModerator: {mod.mention if mod else 'Unbekannt'}") for
                 member, reason, mod in knast_members]
            else:
                embedcount = (int(len(users) / 25) + 1)
                embedlist = []
                rest = round(len(users) / embedcount)
                for i in range(embedcount):
                    if i == 1:
                        fembed = embed
                        [embed.add_field(name=member.name,
                                         value=f"Grund: {reason}\n\nModerator: {mod.mention if mod else 'Unbekannt'}")
                         for member, reason, mod in knast_members[:rest]]
                        [knast_members.remove(a) for a in knast_members[:rest]]
                        embedlist.append(fembed)
                    else:
                        if len(knast_members) <= rest:
                            nembed = discord.Embed(title="", description="", color=embed.color)
                            [embed.add_field(name=member.name,
                                             value=f"Grund: {reason}\n\nModerator: {mod.mention if mod else 'Unbekannt'}")
                             for member, reason, mod in knast_members]
                            embedlist.append(nembed)
                        else:
                            nembed = discord.Embed(title="", description="", color=embed.color)
                            [embed.add_field(name=member.name,
                                             value=f"Grund: {reason}\n\nModerator: {mod.mention if mod else 'Unbekannt'}")
                             for member, reason, mod in knast_members[:rest]]
                            [knast_members.remove(a) for a in knast_members[:rest]]
                            embedlist.append(nembed)
        else:
            embed.description = "Es befinden sich keine Benutzer im Knast."
        try:
            message = await channel.fetch_message(
                2345678901234567890)  # message id von der nachricht, die die liste beinhaltet
            if not embedlist:
                await message.edit(embed=embed)
            else:
                await message.edit(embeds=embedlist)
        except discord.NotFound:
            print("knastlist: nachricht gibts nich")

    async def create_database(self):
        try:
            await connect_execute(self.db_path, '''CREATE TABLE IF NOT EXISTS servers (
                                        uid INTEGER PRIMARY KEY,
                                        reason TEXT,
                                        mod_id INTEGER)''')

            await connect_execute(self.db_path, """
                    CREATE TABLE IF NOT EXISTS WarnList (
                    warn_id INTEGER PRIMARY KEY,
                    mod_id INTEGER,
                    guild_id INTEGER,
                    user_id INTEGER,
                    warns INTEGER DEFAULT 0,
                    warn_reason TEXT,
                    warn_time TEXT)""")
            print("Datenbank und Tables erfolgreich erstellt.")
        except Exception as e:
            print(f"Fehler beim Erstellen der Datenbank: {e}")

    async def cog_load(self):
        await self.create_database()
        if await self.bot.wait_until_ready():
            self.knastlist.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} has connected to Discord!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None or message.author.bot:
            return

        dm_keywords = ["dm", "direct message", "private message"]
        if any([keyword in message.content.lower() for keyword in dm_keywords]):
            row = await connect_execute(self.db_path,
                                        "SELECT warns FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1",
                                        (message.author.id, message.guild.id), datatype="One")
            if row:
                warns = row[0] + 1
            else:
                warns = 1

                warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await connect_execute(self.db_path,
                                      "INSERT INTO WarnList (user_id, guild_id, warns, warn_reason, mod_id, warn_time) VALUES (?, ?, ?, ?, ?, ?)",
                                      (message.author.id, message.guild.id, warns, "Mentioning DMs is not allowed",
                                       self.bot.user.id, warn_time))

            if warns <= 3:
                await message.channel.send(
                    f"{message.author.mention}, DMs are not allowed. Please use the server channels.")
            else:
                await message.channel.send(
                    f"{message.author.mention}, you have been warned multiple times about mentioning DMs. Further actions may be taken.")

    @slash_command(description='Manage User sofern sie scheiße bauen (lol)')
    @commands.has_role(1044557317947019264)
    async def teampanel(self, ctx, member: Option(discord.Member, required=True), reason: Option(str, required=True)):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        squad = member.public_flags
        view = AdminView(member, reason)

        knastuser = await connect_execute(self.db_path, "SELECT uid FROM servers WHERE uid = ?", (member.id,),
                                          datatype="One")
        if knastuser:
            view.children[5].disabled = True
        else:
            view.children[6].disabled = True

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
    async def warnings(self, ctx, member: discord.Member):
        warns_info = []
        rows = await connect_execute(self.db_path,
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
    async def teampanel_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title='Support Anfrage',
                               description="Leider ist dies eine Team Option\nWenn du Hilfe brauchst melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /teampanel auszuführen')
        else:
            print(f"Exception raised in appcommand {ctx.command.name}:" if ctx.command else "Exception raised in View:")
            traceback.print_exception(type(error), error, error.__traceback__, limit=None, file=sys.stderr)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title='Support Anfrage',
                               description="Leider ist dies eine Team Option\nWenn du Hilfe brauchst melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /purge auszuführen')
        else:
            print(f"Exception raised in appcommand {ctx.command.name}:" if ctx.command else "Exception raised in View:")
            traceback.print_exception(type(error), error, error.__traceback__, limit=None, file=sys.stderr)

    @slash_command(description="Rufe das Knast Menü auf")
    async def knastmenu(self, ctx):
        embed = discord.Embed(title="Knast Menü", description="Wähle hier aus was du machen möchtest",
                              color=discord.Colour.random())
        await ctx.respond(embed=embed, view=KnastMenu())


class KnastMenu(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Besucherrollenantrag", style=discord.ButtonStyle.primary)
    async def besuch_Button(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✔ | Anfrage Erfolgreich!",
            description=f"{interaction.user.mention} deine Anfrage wurde an das team geschickt!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title="🚨 | Neue Anfrage",
            description=f"{interaction.user.mention} möchte die besucher rolle haben!",
            color=discord.Color.red()
        )
        self.disable_all_buttons()
        channel = interaction.guild.get_channel(1251558364635332689)  # Replace with your channel ID
        if channel:
            await channel.send(embed=embed, view=BesuchButton(interaction.user, 1184593699523526696))

    @discord.ui.button(label="Entlassungsantrag", style=discord.ButtonStyle.primary)
    async def entlassung_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✔ | Anfrage Erfolgreich!",
            description=f"{interaction.user.mention} deine Anfrage wurde an das team geschickt!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(
            title="🚨 | Neue Anfrage",
            description=f"{interaction.user.mention} möchte Entlassen werden!",
            color=discord.Color.red()
        )
        self.disable_all_buttons()
        channel = interaction.guild.get_channel(1251558364635332689)  # Replace with your channel ID
        if channel:
            await channel.send(embed=embed, view=EntlassungButton(interaction.user, 1184593699523526696))

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True


class BesuchButton(discord.ui.View):
    def __init__(self, user, role):
        super().__init__()
        self.user = user
        self.role = role

    async def interaction_check(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Du hast nicht die erforderlichen Berechtigungen!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.success, custom_id="besuchen_button", emoji="✔")
    async def besuchen(self, button: discord.ui.Button, interaction: discord.Interaction):
        member = interaction.guild.get_member(self.user.id)
        role = interaction.guild.get_role(1184550310451101697)
        if member and role:
            await member.add_roles(role)
            try:
                await self.user.send("Deine Anfrage für die Entlassung wurde akzeptiert.")
            except discord.Forbidden:
                pass
            embed = discord.Embed(
                title="Anfrage",
                description=f"{self.user.mention} hat eine Anfrage geschickt und wurde akzeptiert."
            )
            self.disable_all_buttons()
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            self.start_removal_task(member, role)

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.red, custom_id="ablehnen_button", emoji="❌")
    async def ablehnen(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await self.user.send("Deine Anfrage für die Besucherrolle wurde abgelehnt.")
        except discord.Forbidden:
            pass
        embed = discord.Embed(
            title="Anfrage",
            description=f"{self.user.mention} hat eine Anfrage geschickt und wurde abgelehnt."
        )
        self.disable_all_buttons()
        await interaction.message.edit(view=self)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

    def start_removal_task(self, member, role):
        async def remove_role_after_delay():
            await asyncio.sleep(1800)  # 30 minutes in seconds
            await member.remove_roles(role)
            try:
                await member.send(f"Deine Besucherrolle wurde entfernt nach 30 Minuten.")
            except discord.Forbidden:
                pass

        asyncio.create_task(remove_role_after_delay())


class EntlassungButton(discord.ui.View):
    def __init__(self, user, role):
        super().__init__()
        self.user = user
        self.role = role

    async def interaction_check(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Du hast nicht die erforderlichen Berechtigungen!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Annehmen", style=discord.ButtonStyle.success, custom_id="entlassung_annehmen", emoji="✔")
    async def annehmen(self, button: discord.ui.Button, interaction: discord.Interaction):
        member = interaction.guild.get_member(self.user.id)
        role = interaction.guild.get_role(1184593699523526696)
        if member and role:
            try:
                await member.remove_roles(role)
                await self.user.send("Deine Anfrage für die Entlassung wurde akzeptiert.")
            except discord.Forbidden:
                pass

            embed = discord.Embed(
                title="Anfrage akzeptiert",
                description=f"{self.user.mention} wurde aus dem Knast entlassen."
            )
            self.disable_all_buttons()
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Ablehnen", style=discord.ButtonStyle.danger, custom_id="entlassung_ablehnen", emoji="❌")
    async def ablehnen(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            await self.user.send("Deine Anfrage für die Entlassung wurde abgelehnt.")
        except discord.Forbidden:
            pass

        embed = discord.Embed(
            title="Anfrage abgelehnt",
            description=f"{self.user.mention} wurde nicht aus dem Knast entlassen."
        )
        self.disable_all_buttons()
        await interaction.message.edit(view=self)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True


def setup(bot):
    bot.add_cog(ModSystem(bot))


class AdminView(discord.ui.View):
    def __init__(self, member, reason):
        super().__init__()
        self.member = member
        self.reason = reason
        self.mdb = "mod_sys.db"
        self.kdb = "Data/knast.db"
        self.knast_role_id = 1184593699523526696
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
        await self.ctx.respond(file=file, embed=warn_embed, ephemeral=False)

    @discord.ui.button(label="Warnings", style=discord.ButtonStyle.primary)
    async def warnings_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        warns_info = []
        rows = await connect_execute(self.db_path,
                                     "SELECT warn_id, mod_id, warn_reason, warn_time FROM WarnList WHERE user_id = ? AND guild_id = ?",
                                     (self.member.id, interaction.guild.id), datatype="All")
        for row in rows:
            warn_id, mod_id, warn_reason, warn_time = row
            warn_time = datetime.datetime.strptime(warn_time, '%Y-%m-%d %H:%M:%S')
            warns_info.append((
                              f"**Warn-ID:** __{warn_id}__ | **Warn ausgestellt am:** {warn_time.strftime('%Y-%m-%d %H:%M:%S')}",
                              f"**Moderator:** <@{mod_id}> | **Mod-ID**: __{mod_id}__",
                              f"**> Grund:**\n```{warn_reason}```"))

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        warnings_embed = discord.Embed(title=f"`⚠️` Warn Liste {self.member.name}")
        warnings_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        warnings_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        warnings_embed.set_thumbnail(url=self.member.avatar.url)

        if warns_info == []:
            warnings_embed.description = f"The user has no warns!"
            warnings_embed.color = discord.Color.red()

        else:
            warnings_embed.description = "__**Liste der Warns**__"
            warnings_embed.color = 0x2596be

            [warnings_embed.add_field(name=f"{warntime}", value=f"{mod}\n{reason}", inline=False) for
             warntime, mod, reason in warns_info]

        await interaction.response.send_message(file=file, embed=warnings_embed, ephemeral=False)

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
            embed.title = ''
            embed.description = f'{self.member.mention} wurde getimeouted'
            try:
                membed = discord.Embed(title="Getimeouted",
                                       description=f"Du wurdest im server {interaction.guild.name} getimeouted\nGrund: {self.reason}",
                                       color=0x2596be)
                await self.member.send(embed=membed)
            except:
                embed.description += "\n\nBenutzer konnte nicht angeschrieben werden"
                print("Geht net")
            await self.member.timeout_for(datetime.timedelta(minutes=5))

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
            embed.title = ""
            embed.description = f"{self.member.name} wurde von {interaction.guild.name} gekickt"
            try:
                membed = discord.Embed(title="Gekickt",
                                       description=f"Du wurdest im server {interaction.guild.name} gekickt\nGrund: {self.reason}",
                                       color=0x2596be)
                await self.member.send(embed=membed)
            except:
                embed.description += "\n\nBenutzer konnte nicht angeschrieben werden"
                print("Geht net")
            await self.member.kick(reason=f"wurde von {interaction.user.name} übers Admin panel gekickt")

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
            embed.title = ""
            embed.description = f"{self.member.name} wurde von {interaction.guild.name} gebannt"
            try:
                membed = discord.Embed(title="Gebannt",
                                       description=f"Du wurdest im server {interaction.guild.name} gebannt\nGrund: {self.reason}",
                                       color=0x2596be)
                await self.member.send(embed=membed)
            except discord.Forbidden:
                embed.description += "\n\nBenutzer konnte nicht angeschrieben werden"
                print("Geht net")
            await self.member.ban(reason=f"wurde von {interaction.user.name} übers Admin panel gebannt")

        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

    @discord.ui.button(label="Knast", style=discord.ButtonStyle.danger)
    async def knast_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.knast_role_id)

        if role is None:
            await interaction.response.send_message("Die Knast-Rolle wurde nicht gefunden.", ephemeral=True)
            return

        embed = discord.Embed(
            title="`✅` Erfolgreich!",
            description=f"{self.member.mention} wurde in den Knast gesteckt\n"
                        f"**weitere Informationen:**\n"
                        f"`👮‍♂️` **Moderator:** {interaction.user}\n"
                        f"`🚨` **Grund:** {self.reason}")

        try:
            await connect_execute(self.kdb, "INSERT INTO servers (uid, reason, mod_id) VALUES (?, ?, ?)",
                                  (self.member.id, self.reason, interaction.user.id))

            await self.member.add_roles(role)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)

    @discord.ui.button(label="knastentlassen", style=discord.ButtonStyle.success)
    async def entlassung_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="`✅` Erfolgreich!",
            description="User wurde entlassen!\n\n"
                        "**Weitere infos:**\n"
                        f"`👮‍♂️` **Moderator:** {interaction.user.name}",
            color=discord.Color.green()
        )
        try:
            await connect_execute(self.kdb, "DELETE FROM servers WHERE uid = ?", (self.member.id,))

            role = interaction.guild.get_role(self.knast_role_id)

            if role is None:
                await interaction.response.send_message("Die Knast-Rolle wurde nicht gefunden.", ephemeral=True)
                return

            await self.member.remove_roles(role)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)