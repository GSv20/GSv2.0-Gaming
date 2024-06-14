import discord
from discord.ext import commands

class massrole(commands.Cog):
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
    async def tickets_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title='Support Anfrage',
                               description="Leider ist dies eine Admin Option\nWenn du Hilfe brauchst melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /tickets auszuführen')

def setup(bot):
    bot.add_cog(massrole(bot))
