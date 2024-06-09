import discord
from discord.ext import commands, tasks

class VanityRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GUILD = 913082943495344179
        self.STATUS_ROLE = 944555097390723112
        self.STATUS_TEXT = "gsv2.dev"
        self.LOG_CHANNEL = 1218317295345074298
        self.vanity_task.start()

    async def has_vanity(self, member: discord.Member):
        if member.activities:
            for activity in member.activities:
                if isinstance(activity, discord.CustomActivity):
                    if self.STATUS_TEXT in activity.name or self.STATUS_TEXT == activity.name:
                        return True
        return False

    @tasks.loop(minutes=1)
    async def vanity_task(self):
        await self.bot.wait_until_ready()

        guild: discord.Guild = self.bot.get_guild(self.GUILD)
        role = guild.get_role(self.STATUS_ROLE)
        log = self.bot.get_channel(self.LOG_CHANNEL)

        if guild.members:
            for member in guild.members:
                if member.bot:
                    continue
                vanity = await self.has_vanity(member)
                if vanity:
                    if role not in member.roles:
                        await member.add_roles(role, atomic=True)
                        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                        embed = discord.Embed(
                            title="Vanity-Rolle hinzugefügt!",
                            description=f"{member.mention} hat die Vanity-Rolle {role.mention} erhalten.", 
                            color=discord.Color.green())
                        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                        await log.send(file=file, embed=embed)
                else:
                    if role in member.roles:
                        await member.remove_roles(role, atomic=True)
                        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                        embed = discord.Embed(
                            title="Vanity-Rolle entfernt!",
                            description=f"{member.mention} hat die Vanity-Rolle {role.mention} entfernt bekommen.",
                            color=discord.Color.red())
                        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                        await log.send(file=file, embed=embed)

    @vanity_task.before_loop
    async def before_vanity_task(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(VanityRoleCog(bot))