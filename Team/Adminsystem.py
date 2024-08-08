from datetime import datetime, timedelta
import discord, aiosqlite
from typing import Optional, Literal
from discord.ext import commands


async def connect_execute(database, query: str, injectiontuple: Optional[tuple]=None, datatype: Optional[Literal["All", "One"]]=None):
	async with aiosqlite.connect(database) as conn:
		async with conn.execute(query, injectiontuple if injectiontuple is not None else None) as cur:
			if datatype == "All":
				return await cur.fetchall()
			elif datatype == "One":
				return await cur.fetchone()
			else:
				 await conn.commit()

class AntiSpam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if type(message.channel) is not discord.TextChannel or message.author.bot:
            return

        bucket = self.anti_spam.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after:

            await message.delete()
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='Nicht Spammen', description=f"{message.author.mention}, don't spam!", color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await message.channel.send(file=file, embed=embed, delete_after=10)

            violations = self.too_many_violations.get_bucket(message)
            check = violations.update_rate_limit()

            if check:
                until = datetime.now() + timedelta(minutes=10)
                await message.author.timeout(until)
                try:
                    embed = discord.Embed(title="Don't Spam", description='Spamme bitte nicht die Kanäle voll\nIch musste dich daher Timeouten\n\nUnd ich werde es wiedertun wenn du weitermachst', color=color)
                    embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                    await message.author.send(file=file, embed=embed)
                except:
                    print(f"Konnte keine Nachricht an {message.author.name} senden")
                    return

class Massrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Gibt allen Mitgliedern die ausgewählte Rolle")
    @commands.has_permissions(administrator=True)
    async def massrole(self, ctx, role: discord.Role):
        guild = ctx.guild
        for member in guild.members:
            try:
                await member.add_roles(role)
            except discord.HTTPException as e:
                print(f"Fehler beim Hinzufügen der Rolle zu {member}: {e}")
        await ctx.respond(f"Rolle {role.name} wurde allen Mitgliedern hinzugefügt.")

    @massrole.error
    async def massrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title='Support Anfrage',
                               description="Leider ist dies eine Admin Option\nWenn du Hilfe brauchst melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /massrole auszuführen')

def setup(bot):
    bot.add_cog(Massrole(bot))
    bot.add_cog(AntiSpam(bot))