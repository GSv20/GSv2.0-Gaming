import asyncio
import datetime
from discord.commands import slash_command, Option
import discord
import sqlite3
from discord.ext import commands, tasks


class Team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('Data/team_messages.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS team_members
                               (user_id INTEGER PRIMARY KEY, message_count INTEGER, strikes INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS message_history
                               (user_id INTEGER, date TEXT, message_count INTEGER)''')
        self.conn.commit()
        self.bot.loop.create_task(self.start_loops())

    async def start_loops(self):
        await self.bot.wait_until_ready()
        self.check_messages.start()

    def seconds_until_saturday_noon(self):
        now = datetime.datetime.now()
        next_saturday = now + datetime.timedelta((5 - now.weekday() + 7) % 7)
        next_saturday_noon = next_saturday.replace(hour=12, minute=0, second=0, microsecond=0)
        seconds_until = (next_saturday_noon - now).total_seconds()
        if seconds_until < 0:
            seconds_until += 7 * 24 * 60 * 60
        return seconds_until

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        special_role_id = 1044557317947019264

        if message.guild is None:
            return

        special_role = discord.utils.get(message.guild.roles, id=special_role_id)
        if special_role in message.author.roles:
            date = datetime.date.today().isoformat()
            self.cursor.execute("SELECT * FROM message_history WHERE user_id = ? AND date = ?",
                                (message.author.id, date))
            result = self.cursor.fetchone()
            if result:
                self.cursor.execute(
                    "UPDATE message_history SET message_count = message_count + 1 WHERE user_id = ? AND date = ?",
                    (message.author.id, date))
            else:
                self.cursor.execute("INSERT INTO message_history VALUES (?, ?, ?)", (message.author.id, date, 1))
            self.conn.commit()

    @slash_command(description="Auswertung der Teammitglieder history")
    async def history(self, ctx,
                      user: Option(discord.User, "Der User dessen history ausgewertet werden soll", required=True)):
        two_weeks_ago = (datetime.date.today() - datetime.timedelta(weeks=1)).isoformat()
        self.cursor.execute("SELECT SUM(message_count) FROM message_history WHERE user_id = ? AND date >= ?",
                            (user.id, two_weeks_ago))
        result = self.cursor.fetchone()
        if result and result[0] is not None:
            total_messages = result[0]
            goal_reached = 'Ja' if total_messages >= 150 else 'Nein'

            embed = discord.Embed(
                title="User Evaluation",
                description=f"User: {user.name}\nGesamtzahl der Nachrichten in den letzten zwei Wochen: {total_messages}\nDas Ziel ist erreicht: {goal_reached}",
                color=discord.Color.blue()
            )

            embed.set_author(name=user.name, icon_url=user.avatar.url)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("User not found or no messages in the last two weeks")

    @slash_command(description="Vorhersage, ob der Benutzer das Ziel bis Samstag erreicht")
    async def progress(self, ctx,
                       user: Option(discord.User, "Der User dessen Fortschritt vorhergesagt werden soll",
                                    required=True)):
        today = datetime.date.today()
        next_saturday = today + datetime.timedelta((5 - today.weekday() + 7) % 7)
        days_until_saturday = (next_saturday - today).days

        self.cursor.execute("SELECT date, SUM(message_count) FROM message_history WHERE user_id = ? GROUP BY date",
                            (user.id,))
        results = self.cursor.fetchall()
        if results:
            total_messages = sum(message_count for date, message_count in results)
            total_days = len(results)
            average_messages_per_day = total_messages / total_days

            predicted_messages = average_messages_per_day * days_until_saturday
            goal_reached = 'Ja' if predicted_messages >= 150 else 'Nein'

            embed = discord.Embed(
                title="User Prediction",
                description=f"User: {user.name}\nVoraussichtliche Gesamtzahl der Nachrichten bis Samstag: {predicted_messages}\nDas Ziel wird erreicht: {goal_reached}",
                color=discord.Color.blue()
            )

            embed.set_author(name=user.name, icon_url=user.avatar.url)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("User not found or no messages in the history")

    @tasks.loop(seconds=7 * 24 * 60 * 60)
    async def check_messages(self):
        guild_id = 913082943495344179
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            return
        tmod_role_id = 1052676334247219291
        tmod_role = discord.utils.get(guild.roles, id=tmod_role_id)
        tsup_role_id = 997504163544039484
        tsup_role = discord.utils.get(guild.roles, id=tsup_role_id)
        sup_role_id = 997504036041412619
        sup_role = discord.utils.get(guild.roles, id=sup_role_id)
        mod_role_id = 914076712373989386
        mod_role = discord.utils.get(guild.roles, id=mod_role_id)
        teamleitung_role_id = 1070336143373119593
        teamleitung_role = discord.utils.get(guild.roles, id=teamleitung_role_id)
        special_role_id = 1044557317947019264
        special_role = discord.utils.get(guild.roles, id=special_role_id)
        if special_role is None:
            return
        evaluation_channel_id = 1073701381069869056
        evaluation_channel = self.bot.get_channel(evaluation_channel_id)

        for member in special_role.members:
            self.cursor.execute("SELECT * FROM team_members WHERE user_id = ?", (member.id,))
            result = self.cursor.fetchone()
            if result:
                user_id, message_count, strikes = result
                user = self.bot.get_user(user_id)

                for member in special_role.members:
                    if special_role not in member.roles:
                        roles_to_remove = [tmod_role, mod_role, teamleitung_role, tsup_role, sup_role]
                        for role in roles_to_remove:
                            if role in member.roles:
                                await member.remove_roles(role)
                if strikes > 2:  # Wenn Strikes größer als 2 sind, entferne die Rolle
                    await member.remove_roles(special_role)
                    self.cursor.execute("DELETE FROM team_members WHERE user_id = ?", (user_id,))
                    continue

                if message_count >= 150:
                    strikes = max(0, strikes - 1)
                elif message_count == 0:
                    strikes += 1

                self.cursor.execute("UPDATE team_members SET message_count = 0, strikes = ? WHERE user_id = ?",
                                    (strikes, user_id,))

                embed = discord.Embed(
                    title="User Evaluation",
                    description=f"User: {user.name}\nMessage Count: {message_count}\nStrikes: {strikes}",
                    color=discord.Color.blue()
                )

                embed.set_author(name=user.name, icon_url=user.avatar.url)
                await evaluation_channel.send(embed=embed)

            else:
                self.cursor.execute("INSERT INTO team_members VALUES (?, ?, ?)", (member.id, 0, 1))
        self.conn.commit()

    @check_messages.before_loop
    async def before_check_messages(self):
        await self.bot.wait_until_ready()
        seconds_until = self.seconds_until_saturday_noon()
        await asyncio.sleep(seconds_until)


def setup(bot):
    bot.add_cog(Team(bot))