from datetime import datetime, timedelta
import discord
from discord.ext import commands

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
                until = datetime.utcnow() + timedelta(minutes=10)
                await message.author.timeout(until)
                try:
                    file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                    color = 0x2596be
                    embed = discord.Embed(title="Don't Spam", description='Spamme bitte nicht die Kanäle voll\nIch musste dich daher Timeouten\n\nUnd ich werde es wiedertun wenn du weitermachst', color=color)
                    embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                    await message.author.send(file=file, embed=embed)
                except:
                    print(f"Konnte keine Nachricht an {message.author.name} senden")
                    return


def setup(bot):
    bot.add_cog(AntiSpam(bot))
