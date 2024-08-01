import discord
from discord.ext import commands
import aiosqlite
import datetime

class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None or message.author.bot:
            return


        dm_keywords = ["dm", "direct message", "private message"]
        if any(keyword in message.content.lower() for keyword in dm_keywords):
            async with aiosqlite.connect("Data/mod_sys.db") as db:
                async with db.execute(
                    "SELECT warns FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1",
                    (message.author.id, message.guild.id)
                ) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        warns = row[0] + 1
                    else:
                        warns = 1

                warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await db.execute(
                    "INSERT INTO WarnList (user_id, guild_id, warns, warn_reason, mod_id, warn_time) VALUES (?, ?, ?, ?, ?, ?)",
                    (message.author.id, message.guild.id, warns, "Mentioning DMs is not allowed", self.bot.user.id, warn_time)
                )
                await db.commit()

            if warns <= 3:
                await message.channel.send(f"{message.author.mention}, DMs are not allowed. Please use the server channels.")
            else:
                await message.channel.send(f"{message.author.mention}, you have been warned multiple times about mentioning DMs. Further actions may be taken.")

def setup(bot):
    bot.add_cog(DM(bot))
