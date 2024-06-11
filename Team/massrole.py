import discord
from discord.ext import commands

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Gibt allen Mitgliedern die ausgewählte Rolle")
    @commands.has_permissions(administrator=True)
    async def massrole(self, interaction: discord.Interaction, role: discord.Role):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("Dieser Befehl kann nur auf einem Server verwendet werden.", ephemeral=True)
            return

        for member in guild.members:
            try:
                await member.add_roles(role)
            except discord.HTTPException as e:
                print(f"Fehler beim Hinzufügen der Rolle zu {member}: {e}")

        await interaction.response.send_message(f"Rolle {role.name} wurde allen Mitgliedern hinzugefügt.")

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

async def setup(bot):
    await bot.add_cog(RoleManager(bot))
