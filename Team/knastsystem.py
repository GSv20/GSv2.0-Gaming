import asyncio
import sqlite3

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, Option


class KnastSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timeout_role_id = 1184593699523526696  # ID der Timeout-Rolle
        self.knast_role_id = self.timeout_role_id  # Verwendet dieselbe ID wie die Timeout-Rolle
        self.create_database()

    def create_database(self):
        # Create a database to store the server IDs and welcome channels that have enabled the welcome module
        conn = sqlite3.connect('Data/knast.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS servers (
                        uid INTEGER PRIMARY KEY,
                        reason TEXT,
                        mod_id INTEGER
                    )''')
        conn.commit()
        conn.close()

    @slash_command(description="Stecke Jemand in den Knast")
    @commands.has_permissions(ban_members=True)
    async def knast(self, ctx,
                    member: Option(discord.Member, "Wähle den User aus, den du in den Knast stecken willst",
                                   required=True),
                    reason: Option(str, "Gib einen Grund an, warum du den User in den Knast stecken willst",
                                   required=False, default="Kein Grund angegeben")):
        guild = ctx.guild
        role = guild.get_role(self.knast_role_id)

        if role is None:
            await ctx.respond("Die Knast-Rolle wurde nicht gefunden.", ephemeral=True)
            return

        embed = discord.Embed(
            title="`✅` Erfolgreich!",
            description=f"{member.mention} wurde in den Knast gesteckt\n"
                        f"**weitere Informationen:**\n"
                        f"`👮‍♂️` **Moderator:** {ctx.author}\n"
                        f"`🚨` **Grund:** {reason}"
        )

        try:
            async with aiosqlite.connect("Data/knast.db") as db:
                async with db.execute("SELECT uid FROM servers WHERE uid = ?", (member.id,)) as cursor:
                    existing_user = await cursor.fetchone()

                if existing_user:
                    await db.execute(
                        "UPDATE servers SET reason = ?, mod_id = ? WHERE uid = ?",
                        (reason, ctx.author.id, member.id)
                    )
                else:
                    await db.execute(
                        "INSERT INTO servers (uid, reason, mod_id) VALUES (?, ?, ?)",
                        (member.id, reason, ctx.author.id)
                    )
                await db.commit()

            await member.add_roles(role)
            await ctx.respond(embed=embed, ephemeral=True)
        except Exception as e:
            await ctx.respond(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)

    @slash_command(description="Zeigt eine Liste aller Benutzer im Knast")
    @commands.has_permissions(administrator=True)
    async def knast_list(self, ctx):
        try:
            async with aiosqlite.connect("Data/knast.db") as db:
                async with db.execute("SELECT uid, reason, mod_id FROM servers") as cursor:
                    users = await cursor.fetchall()

            if not users:
                await ctx.respond("Es befinden sich keine Benutzer im Knast.", ephemeral=True)
                return

            guild = ctx.guild
            knast_members = [(guild.get_member(user_id), reason, guild.get_member(mod_id)) for user_id, reason, mod_id
                             in users if guild.get_member(user_id)]

            embed = discord.Embed(
                title="Benutzer im Knast",
                color=discord.Color.red()
            )

            for member, reason, mod in knast_members:
                embed.add_field(name="Benutzer",
                                value=f"{member.mention}\n\nGrund: {reason}\n\nModerator: {mod.mention if mod else 'Unbekannt'}",
                                inline=False)

            if not knast_members:
                embed.description = "Es befinden sich keine Benutzer im Knast."

            await ctx.respond(embed=embed, ephemeral=True)
        except Exception as e:
            await ctx.respond(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)

    @slash_command(description="Entlasse einen User")
    @commands.has_permissions(ban_members=True)
    async def freigabe(self, ctx,
                       member: Option(discord.Member, "Wähle den User aus, den du freigeben willst", required=True)):
        embed = discord.Embed(
            title="`✅` Erfolgreich!",
            description="User wurde entlassen!\n\n"
                        "**Weitere infos:**\n"
                        f"`👮‍♂️` **Moderator:** {ctx.author}",
            color=discord.Color.green()
        )
        try:
            async with aiosqlite.connect("Data/knast.db") as db:
                await db.execute(
                    "DELETE FROM servers WHERE uid = ?",
                    (member.id,)
                )
                await db.commit()

            guild = ctx.guild
            role = guild.get_role(self.knast_role_id)

            if role is None:
                await ctx.respond("Die Knast-Rolle wurde nicht gefunden.", ephemeral=True)
                return

            await member.remove_roles(role)
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"Ein Fehler ist aufgetreten: {e}", ephemeral=True)

    @slash_command(description="Rufe das Knast Menü auf")
    async def knastmenu(self, ctx, option: Option(str, "Wähle einen Text aus", choices=[
        "Anfrage schicken für die besucher rolle",
        "Entlassungs Anfrage", ], required=True)):

        if option == "Entlassungs Anfrage":
            embed = discord.Embed(
                title="✔ | Anfrage Erfolgreich!",
                description=f"{ctx.author.mention} deine Anfrage wurde an das team geschickt!",
                color=discord.Color.green()
            )
            await ctx.respond(embed=embed, ephemeral=True)

            embed = discord.Embed(
                title="🚨 | Neue Anfrage",
                description=f"{ctx.author.mention} möchte Entlassen werden!",
                color=discord.Color.red()
            )

            channel_id = 1251558364635332689  # Replace with your channel ID
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                await channel.send(embed=embed, view=EntlassungButton(ctx.author, self.timeout_role_id))

        if option == "Anfrage schicken für die besucher rolle":
            embed = discord.Embed(
                title="✔ | Anfrage Erfolgreich!",
                description=f"{ctx.author.mention} deine Anfrage wurde an das team geschickt!",
                color=discord.Color.green()
            )
            await ctx.respond(embed=embed, ephemeral=True)

            embed = discord.Embed(
                title="🚨 | Neue Anfrage",
                description=f"{ctx.author.mention} möchte die besucher rolle haben!",
                color=discord.Color.red()
            )

            channel_id = 1251558364635332689  # Replace with your channel ID
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                await channel.send(embed=embed, view=BesuchButton(ctx.author, self.timeout_role_id))


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
        guild = interaction.guild
        member = guild.get_member(self.user.id)
        role_id = 1184550310451101697
        role = guild.get_role(role_id)
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
        guild = interaction.guild
        member = guild.get_member(self.user.id)
        role_id = 1184593699523526696
        role = guild.get_role(role_id)
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
    bot.add_cog(KnastSystem(bot))