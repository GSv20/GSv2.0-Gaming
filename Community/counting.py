import discord
from discord.ext import commands
import sqlite3


class CountingCog(commands.Cog):
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id
        self.conn = sqlite3.connect('Data/counting.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS counting (
                          guild_id INTEGER PRIMARY KEY,
                          last_number INTEGER,
                          last_user_id INTEGER)''')
        self.conn.commit()

    def close_connection(self):
        self.c.close()
        self.conn.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel.id != self.channel_id:
            return

        try:
            number = int(message.content)
        except ValueError:
            return

        try:
            await self.handle_counting(message, number)
        except Exception as e:
            print(f"An error occurred: {e}")

    async def handle_counting(self, message, number):
        row = self.c.execute('SELECT last_number, last_user_id FROM counting WHERE guild_id = ?',
                             (message.guild.id,)).fetchone()
        if row:
            last_number, last_user_id = row
            if last_number is None:
                await self.handle_first_counting(message, number)
            elif number == last_number + 1 and last_user_id != message.author.id:
                await self.handle_correct_counting(message, number)
            else:
                await self.handle_incorrect_counting(message, last_user_id)
        else:
            await self.handle_first_counting(message, number)

    async def handle_correct_counting(self, message, number):
        await message.add_reaction('<:yes:1073716074140414013>')
        self.c.execute('UPDATE counting SET last_number = ?, last_user_id = ? WHERE guild_id = ?',
                       (number, message.author.id, message.guild.id))
        self.conn.commit()
        if number % 100 == 0:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            await message.add_reaction('🔥')
            embed = discord.Embed(title='Herzlichen Glückwunsch!', description=f'Ihr seid jetzt schon bei der Nummer: `{number}` 🎉. Weiter so!', colour=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await message.channel.send(file=file, embed=embed, delete_after=120)

    async def handle_incorrect_counting(self, message, last_user_id):
        await message.add_reaction('<:nope:1073700944941957291>')
        row = self.c.execute('SELECT last_number FROM counting WHERE guild_id = ?', (message.guild.id,)).fetchone()
        if row:
            last_number = row[0]
            if last_user_id == message.author.id:
                file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                color = 0x2596be
                embed = discord.Embed(title='<:nope:1073700944941957291> | Error', description=f'{message.author.mention} Du kannst nicht zweimal hintereinander zählen!', colour=color)
                embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                await message.channel.send(file=file, embed=embed, delete_after=30)
                await message.delete()
            else:
                file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                color = 0x2596be
                embed = discord.Embed(title='<:nope:1073700944941957291> | Error', description=f'{message.author.mention} Du hast falsch gezählt, die nächste Zahl wäre `{last_number + 1}`.', colour=color)
                embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                await message.channel.send(file=file, embed=embed, delete_after=30)
                await message.delete()

    async def handle_first_counting(self, message, number):
        self.c.execute('INSERT OR REPLACE INTO counting (guild_id, last_number, last_user_id) VALUES (?, ?, ?)',
                       (message.guild.id, number, message.author.id))
        self.conn.commit()
        await message.add_reaction('<:G_:1158950908613361694>')
        await message.add_reaction('<:S_:1158950928586657802>')
        await message.add_reaction('<:v_:1158950963009310770>')


def setup(bot):
    channel_id = 1243269123379691662
    cog = CountingCog(bot, channel_id)
    bot.add_cog(cog)

    @bot.event
    async def on_ready():
        cog.close_connection()
