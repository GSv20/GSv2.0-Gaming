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


        dm_keywords = ["dm", "pn", "direct message", "private message"]
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
                file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                color = discord.Color.dark_red()
                embed = discord.Embed(
                    title='❌ | Error',
                    description=('Hey hey,\nDMs (usw) sind hier eher unerwünscht.\nWir müssen auch ein bisschen auf unsere User aufpassen und die Community, '
                                 'daher versuche bitte es zu vermeiden in Private chats usw zu switchen\n\nFür Probleme, Einzelgespräche und sonnstiges bieten '
                                 'wir sogar seperate räume an\n\nDanke das du dich an die Regeln hälst, des Servers willen.'),
                    color=color)
                embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                await message.channel.send(f"{message.author.mention}", delete_after=115)
                await message.channel.send(file=file, embed=embed, delete_after=120)
            else:
                try:
                    file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                    color = discord.Color.dark_red()
                    user_embed = discord.Embed(title='GSv2.0 | DM System', description='Hey hey,\nIrgentwas hat da nicht so ganz geklappt.\ndir wurde ein warn Hinzugefügt, und dadurch auch ein Timeout\nDer Grund dafür ist: DM is not allowed\n\nWenn du denkst das es sich hierbei um einen Fehler handelt so melde dich gerne im <#1073700885886152837>', color=color)
                    user_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                    await message.author.send(file=file, embed=user_embed)
                except discord.Forbidden:
                    print(f"Direktnachricht an {message.author.name} konnte nicht zugestellt werden, wurde getimeotet\n(DM System)")
                finally:
                    file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                    color = discord.Color.dark_red()
                    embed = discord.Embed(
                        title='❌ | Error',
                        description=f'{message.author.mention} hat zu oft gegen die Regeln verstoßen.\n'
                                    f'Aktionen wurden daher ausgeführt, wir bitten dies zu berücksichtigen',
                        color=color)
                    embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                    await message.channel.send(f"{message.author.mention}", delete_after=50)
                    await message.channel.send(file=file, embed=embed, delete_after=60)
                    await message.author.timeout(datetime.timedelta(minutes=1))

def setup(bot):
    bot.add_cog(DM(bot))
