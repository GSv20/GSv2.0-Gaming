import asyncio
from datetime import timedelta
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
            await message.channel.send(f"{message.author.mention}, don't spam!", delete_after=10)

            violations = self.too_many_violations.get_bucket(message)
            check = violations.update_rate_limit()

            if check:

                await message.author.timeout(timedelta(minutes=10))

                try:

                    await message.author.send("You have been muted for spamming!")

                except:

                    return


def setup(bot):
    bot.add_cog(AntiSpam(bot))