import ezcord
from discord.ext import commands
from discord.commands import SlashCommandGroup
import discord


class modmail(ezcord.DBHandler):
    def __init__(self):
        super().__init__("Data/modmail.db")
        self._db_path = "Data/modmail.db"

    async def setup(self):
        await self.execute(
            """CREATE TABLE IF NOT EXISTS blacklist(
                    user_id INTEGER PRIMARY KEY
            )"""
        )

    async def get_blacklist(self, user_id):
        return await self.one("SELECT user_id FROM blacklist WHERE user_id = ?", user_id)

    async def add_blacklist(self, user_id):
        await self.execute("INSERT INTO blacklist(user_id) VALUES (?)", user_id)

    async def remove_blacklist(self, user_id):
        await self.execute("DELETE FROM blacklist WHERE user_id = ?", user_id)


db = modmail()


class blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = modmail()
        self.bot.loop.run_until_complete(self.db.setup())

    blacklist = SlashCommandGroup("dm_support", guild_only=True)

    @blacklist.command(description="Sperre ein User")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, user: discord.User):
        if user.bot:
            await ctx.send("Du kannst keine Bots bannen!")
            return
        if await modmail().get_blacklist(user.id) is not None:
            embed = discord.Embed(
                title="<:off:1238127750372524052> | User ist bereits gesperrt!",
                description="Dieser Benutzer ist bereits gesperrt!",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        await modmail().execute("INSERT INTO blacklist(user_id) VALUES(?)", user.id)
        embed = discord.Embed(
            title="<:verifybadge:1238127161978654822> | User wurde gesperrt!",
            description=f"{user.mention} wurde erfolgreich gesperrt!\n"
                        f"Der Benutzer kann keine tickets mehr erstellen!",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @ban.error
    async def banlist_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title='<:nope:1073700944941957291> | Error', description="Du bist nicht berechtigt, den /set command auszuführen\n\nFrage einen Admin ob er dir den AI channel hinzufügt", color=discord.Color.red())
            em.set_footer(text="Powered by GSV ⚡",
                          icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
            await ctx.respond(embed=em)

    @blacklist.command(description="Entsperre ein User")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, user: discord.User):
        if await modmail().get_blacklist(user.id) is None:
            embed = discord.Embed(
                title="<:off:1238127750372524052> | User ist nicht gesperrt!",
                description="Dieser Benutzer ist nicht gesperrt!",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        await modmail().execute("DELETE FROM blacklist WHERE user_id = ?", user.id)
        embed = discord.Embed(
            title="<:verifybadge:1238127161978654822> | User wurde entsperrt!",
            description=f"{user.mention} wurde erfolgreich entsperrt!",
            color=discord.Color.green()
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @unban.error
    async def banlist_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title='<:nope:1073700944941957291> | Error', description="Du bist nicht berechtigt, den /set command auszuführen\n\nFrage einen Admin ob er dir den AI channel hinzufügt", color=discord.Color.red())
            em.set_footer(text="Powered by GSV ⚡",
                          icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
            await ctx.respond(embed=em)

    @blacklist.command(description="Zeige alle gesperrten User")
    @commands.has_permissions(administrator=True)
    async def list(self, ctx):
        blacklist = await modmail().all("SELECT user_id FROM blacklist")
        if not blacklist:
            await ctx.send("Es sind keine Benutzer auf der Blacklist!")
            return
        blacklist = [f"<@{user_id}>" for user_id in blacklist]
        embed = discord.Embed(
            title="Blacklist",
            description=f"Die Blacklist enthält folgende Benutzer:\n{', '.join(blacklist)}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @list.error
    async def banlist_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title='<:nope:1073700944941957291> | Error', description="Du bist nicht berechtigt diesen Command auszuführen", color=discord.Color.red())
            em.set_footer(text="Powered by GSV ⚡",
                          icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
            await ctx.respond(embed=em)


def setup(bot):
    bot.add_cog(blacklist(bot))
