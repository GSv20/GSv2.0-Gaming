import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from datetime import datetime
from .Adminsystem import connect_execute

class LOACog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbp = 'Data/team.db'

    async def cog_load(self):
        await connect_execute(self.dbp, '''CREATE TABLE IF NOT EXISTS abmeldung
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                grund TEXT,
                                start_date TEXT,
                                end_date TEXT)''')

    @slash_command(name="abmelden", description="Melde dich für einen bestimmten Zeitraum ab")
    async def abmelden(self, ctx,
                       grund: Option(str, "Grund für die Abwesenheit", required=True),
                       start_date: Option(str, "Startdatum der Abwesenheit (DD.MM.YYYY)", required=True),
                       end_date: Option(str, "Enddatum der Abwesenheit (DD.MM.YYYY)", required=True)):

        if not any(role.id == 1044557317947019264 for role in ctx.author.roles):
            await ctx.respond("Du benötigst die erforderliche Rolle, um diesen Befehl auszuführen.", ephemeral=True)
            return


        try:
            start_date_obj = datetime.strptime(start_date, '%d.%m.%Y')
            end_date_obj = datetime.strptime(end_date, '%d.%m.%Y')
        except ValueError:
            await ctx.respond("Bitte gebe ein gültiges Datum im Format DD.MM.YYYY an.", ephemeral=True)
            return

        now = datetime.now()
        if start_date_obj < now or end_date_obj < now:
            await ctx.respond("Die angegebenen Daten müssen in der Zukunft liegen.", ephemeral=True)
            return

        if end_date_obj <= start_date_obj:
            await ctx.respond("Das Enddatum muss nach dem Startdatum liegen.", ephemeral=True)
            return

        start_date_iso = start_date_obj.isoformat()
        end_date_iso = end_date_obj.isoformat()

        await connect_execute(self.dbp, '''INSERT INTO abmeldung (user_id, grund, start_date, end_date)
                                   VALUES (?, ?, ?, ?)''', (ctx.author.id, grund, start_date_iso, end_date_iso))

        embed = discord.Embed(
            title="✅ Erfolgreich abgemeldet",
            description="Deine Abwesenheitsinformationen wurden erfasst und das Team informiert.\n"
                        f"**Grund:** {grund}\n"
                        f"**Beginn der Abwesenheit:** <t:{int(start_date_obj.timestamp())}:R>\n"
                        f"**Ende der Abwesenheit:** <t:{int(end_date_obj.timestamp())}:R>",
            color=discord.Color.green()
        )

        await ctx.respond(embed=embed, ephemeral=True)

        channel = self.bot.get_channel(1172557019358703646)

        embed = discord.Embed(
            title=f"✅ {ctx.author.name}s Abmeldung",
            description="Die folgenden Informationen wurden erfasst:\n"
                        f"**Grund:** {grund}\n"
                        f"**Beginn der Abwesenheit:** <t:{int(start_date_obj.timestamp())}:R>\n"
                        f"**Ende der Abwesenheit:** <t:{int(end_date_obj.timestamp())}:R>",
            color=discord.Color.green()
        )

        await channel.send(embed=embed)

    @slash_command(description="Zeige alle deine Abmeldungen an")
    @commands.has_permissions(administrator=True)
    async def user_abmeldung(self, ctx, user: Option(discord.User, "Wähle einen Member")):

        abmeldungen = await connect_execute(self.dbp, '''SELECT grund, start_date, end_date FROM abmeldung WHERE user_id = ?''', (user.id,), datatype="All")
        if not abmeldungen:
            await ctx.respond("Du hast keine Abmeldungen.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"📋 {user.name}s Abmeldungen",
            color=discord.Color.blue()
        )

        [
            embed.add_field(
                name=f"Abmeldung vom {datetime.fromisoformat(start_date).strftime('%d.%m.%Y')} bis {datetime.fromisoformat(end_date).strftime('%d.%m.%Y')}", 
                value=f"**Grund:** {grund}\n**Beginn der Abwesenheit:** <t:{int(datetime.fromisoformat(start_date).timestamp())}:R>\n**Ende der Abwesenheit:** <t:{int(datetime.fromisoformat(end_date).timestamp())}:R>",
                inline=False
            ) 
            for grund, start_date, end_date in abmeldungen]

        await ctx.respond(embed=embed, ephemeral=True)



def setup(bot):
    bot.add_cog(LOACog(bot))