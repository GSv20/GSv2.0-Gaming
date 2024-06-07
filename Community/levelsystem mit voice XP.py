import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, Option
import aiosqlite

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "Data/level.db"

    @staticmethod
    def get_level(xp):
        lvl = 1
        amount = 100 # Werte zum Leveln angeben

        while True:
            xp -= amount
            if xp < 0:
                return lvl
            lvl += 1
            if lvl >= 5 and lvl <= 20:
                amount += 200
            elif lvl >= 20:
                amount += 400
            amount += 250

    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def get_xp(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    async def get_msgcount(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT msg_count FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    async def get_voicecount(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT voice_count FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
        return result[0]

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                msg_count INTEGER DEFAULT 0,
                voice_count INTEGER DEFAULT 0,
                xp INTEGER DEFAULT 0
                )"""
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        global lvlup
        if message.author.bot:
            return
        if not message.guild:
            return
        xp = 10

        await self.check_user(message.author.id)
        async with aiosqlite.connect(self.DB) as db:
            await db.execute(
                "UPDATE users SET msg_count = msg_count + 1, xp = xp + ? WHERE user_id = ?", (xp, message.author.id)
            )
            await db.commit()

        new_xp = await self.get_xp(message.author.id)
        old_level = self.get_level(new_xp - xp)
        new_level = self.get_level(new_xp)
        msgcount = await self.get_msgcount(message.author.id)
        voicecount = await self.get_voicecount(message.author.id)
        if old_level == new_level:
            return

        if new_level == 5:
            lvl = message.guild.get_role(1017133827631611954) # IDs von Levelrollen
            await message.author.add_roles(lvl)
            rolledazu = "ja"
        # Weitere Level-Rollen hinzufügen...

        else:
            rolledazu = "nein"
            lvlup = discord.Embed(
                title="Level up!",
                description=f"Herzlichen Glückwunsch <@{message.author.id}> du bist jetzt **Level {new_level}!** \nDu "
                            f"hast insgesamt **{msgcount} Nachrichten** geschrieben!",
                color=discord.Color.dark_gold())
            lvlup.set_footer(text="Powered by GSV ⚡",
                             icon_url="https://cdn.discordapp.com/attachments/999378185282142258/1052978247538856087/Werble-141D560B04.gif")

            if voicecount != 0:
                lvlup = discord.Embed(
                    title="Level up!",
                    description=f"Herzlichen Glückwunsch <@{message.author.id}> du bist jetzt **Level {new_level}!**\n \n Du hast insgesamt **{msgcount} Nachrichten** geschrieben und {voicecount} Minuten im Voice verbracht!",
                    color=discord.Color.dark_gold())
                lvlup.set_footer(text="Powered by GSV ⚡",
                                 icon_url="https://cdn.discordapp.com/attachments/999378185282142258/1052978247538856087/Werble-141D560B04.gif")

        if rolledazu == "ja":
            lvlup = discord.Embed(
                title="Level up!",
                description=f"Herzlichen Glückwunsch <@{message.author.id}> du bist jetzt **Level {new_level}!**\n \n Du hast insgesamt **{msgcount} Nachrichten** geschrieben!\n Du hast die Rolle `{lvl}` freigeschaltet!",
                color=discord.Color.dark_gold())
            lvlup.set_footer(text="Powered by GSV ⚡",
                             icon_url="https://cdn.discordapp.com/attachments/999378185282142258/1052978247538856087/Werble-141D560B04.gif")

            if voicecount != 0:
                lvlup = discord.Embed(
                    title="Level up!",
                    description=f"Herzlichen Glückwunsch <@{message.author.id}> du bist jetzt **Level {new_level}!**\n \n Du hast insgesamt **{msgcount} Nachrichten** geschrieben und {voicecount} Minuten im Voice verbracht!\n Du hast die Rolle `{lvl}` freigeschaltet!",
                    color=discord.Color.dark_gold())
                lvlup.set_footer(text="Powered by GSV ⚡",
                                 icon_url="https://cdn.discordapp.com/attachments/999378185282142258/1052978247538856087/Werble-141D560B04.gif")

        ch = message.author.dm_channel
        if ch is None:
            try:
                ch = await message.author.create_dm()
            except discord.HTTPException:
                print("Kann keine Nachricht an diesen Benutzer senden.")
                return

        try:
            await ch.send(embed=lvlup)
        except discord.HTTPException:
            await message.channel.send(message.author.mention, embed=lvlup, delete_after=400)

class VoiceLeveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "Data/level.db"

    @staticmethod
    def get_level(xp):
        lvl = 1
        amount = 10

        while True:
            xp -= amount
            if xp < 0:
                return lvl
            lvl += 1
            amount += 300

    async def check_user(self, user_id):
        async with aiosqlite.connect(self.DB) as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def get_xp(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    async def get_msgcount(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT msg_count FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    async def get_voicecount(self, user_id):
        await self.check_user(user_id)
        async with aiosqlite.connect(self.DB) as db:
            async with db.execute("SELECT voice_count FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()

        return result[0]

    @commands.Cog.listener()
    async def on_ready(self):
        self.is_connected.start()

    @tasks.loop(minutes=1)
    async def is_connected(self):
        global lvlup, lvl
        xp = 10
        guild = self.bot.get_guild(913082943495344179)  # Server-ID

        radio_channel_ids = [1076577676271304724, 1073702324217860118, 1077643360841515089, 1155364945135947877,
                             1073701292146430033]
        radio_channels = [self.bot.get_channel(channel_id) for channel_id in radio_channel_ids]

        for member in guild.members:
            if member.voice:
                if member.voice.channel in radio_channels:
                    pass

                if len(member.voice.channel.voice_states.keys()) >= 2:

                    async with aiosqlite.connect(self.DB) as db:
                        await db.execute(
                            "UPDATE users SET voice_count = voice_count + 1, xp = xp + ? WHERE user_id = ?",
                            (xp, member.id)
                        )
                        await db.commit()
                    new_xp = await self.get_xp(member.id)
                    old_level = self.get_level(new_xp - xp)
                    new_level = self.get_level(new_xp)
                    voicecount = await self.get_voicecount(member.id)
                    msgcount = await self.get_msgcount(member.id)
                    if old_level == new_level:
                        pass
                    else:

                        if new_level == 5:
                            lvl = guild.get_role(1017133827631611954)#ids von levelrollen
                            await member.add_roles(lvl)
                            rolledazu = "ja"

                        elif new_level == 20:
                            lvl = guild.get_role(1051796133317464074)
                            await member.add_roles(lvl)
                            rolledazu = "ja"
                        elif new_level == 50:
                            lvl = guild.get_role(1017134812802322503)
                            await member.add_roles(lvl)
                            rolledazu = "ja"
                        elif new_level == 75:
                            lvl = guild.get_role(1032672722007904346)
                            await member.add_roles(lvl)
                            rolledazu = "ja"

                        elif new_level == 99:
                            lvl = guild.get_role(1032673100409606204)
                            await member.add_roles(lvl)
                            rolledazu = "ja"
                        else:
                            rolledazu = "nein"
                            lvlup = discord.Embed(
                                title="Level up!",
                                description=f"Herzlichen Glückwunsch <@{member.id}> du bist jetzt **Level {new_level}!** \nDu "
                                            f"warst insgesamt **{voicecount}** Minuten im Voice!",
                                color=discord.Color.dark_gold())
                            lvlup.set_footer(text="Powered by GSV ⚡",
                                             icon_url="https://cdn.discordapp.com/attachments/999378185282142258/1052978247538856087/Werble-141D560B04.gif")


                            if msgcount != 0:
                                lvlup = discord.Embed(
                                    title="Level up!",
                                    description=f"Herzlichen Glückwunsch <@{member.id}> du bist jetzt **Level {new_level}!** \nDu "
                                                f"warst insgesamt **{voicecount}** Minuten im Voice und hast **{msgcount}** Nachrichten geschrieben geschrieben!",
                                    color=discord.Color.dark_gold())
                                lvlup.set_footer(text="Powered by GSV ⚡",
                                                 icon_url="https://cdn.discordapp.com/attachments/999378185282142258/1052978247538856087/Werble-141D560B04.gif")

                        if rolledazu == "ja":
                            lvlup = discord.Embed(
                                title="Level up!",
                                description=f"Herzlichen Glückwunsch <@{member.id}> du bist jetzt **Level {new_level}!**\n \nDu warst insgesamt **{voicecount}** Minuten im Voice!\n Du hast die Rolle `{lvl}` freigeschaltet!",
                                color=discord.Color.dark_gold())
                            lvlup.set_footer(text="Powered by GSV ⚡",
                                             icon_url="https://cdn.discordapp.com/attachments/999378185282142258/1052978247538856087/Werble-141D560B04.gif")
                            if msgcount != 0:
                                lvlup = discord.Embed(
                                    title="Level up!",
                                    description=f"Herzlichen Glückwunsch <@{member.id}> du bist jetzt **Level {new_level}!**\n \nDu warst insgesamt **{voicecount}** Minuten im Voice und hast **{msgcount}** Nachrichten geschrieben!\n Du hast die Rolle `{lvl}` freigeschaltet!",
                                    color=discord.Color.dark_gold())
                                lvlup.set_footer(text="Powered by GSV ⚡",
                                                 icon_url="https://cdn.discordapp.com/attachments/999378185282142258/1052978247538856087/Werble-141D560B04.gif")
                        ch = member.dm_channel
                        if ch is None:
                            try:
                                ch = await member.create_dm()
                            except discord.HTTPException:
                                chat = guild.get_channel()#channel wo lvl up nachricht hin soll wenn die nachricht nich per dm geschickt werden kann
                                await chat.send(member.name, embed=lvlup, delete_after=400)

def setup(bot):
    bot.add_cog(LevelSystem(bot))
    bot.add_cog(VoiceLeveling(bot))