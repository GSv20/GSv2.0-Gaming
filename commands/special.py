import discord
from discord.ext import commands

class Special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='📝┃Sende die Liste der Server-Emojis')
    async def emojilist(self, interaction: discord.Interaction):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(
            title='Emojis',
            description='',
            color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        if len(interaction.guild.emojis) > 50:
            embed_2 = discord.Embed(
                title='❌ | Error | ❌',
                description='Anscheinend gibt es zu viele Emojis auf diesem Server :( \nIch bin dadurch leider etwas eingeschränkt',
                color=discord.Color.dark_red())
            embed_2.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=file, embed=embed_2, delete_after=120)
        else:
            for emoji in interaction.guild.emojis:
                embed.description += f'{emoji} - `{emoji}`\n'
            await interaction.response.send_message(file=file, embed=embed, delete_after=120)

    @commands.slash_command(description='.')
    @commands.has_permissions(administrator=True)
    async def coming_soon(self, ctx):
        message = 'coming soon <a:Loading:1073700976000782396>'
        await ctx.respond(message)

    @coming_soon.error
    async def coming_soon_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title=' ❌| Error | ❌',
                               description="Leider ist dies eine Admin Option.\nWenn du Hilfe brauchst, melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.send(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /coming_soon auszuführen')

    @commands.slash_command(description='.')
    @commands.has_any_role(1044557317947019264)
    @commands.cooldown(1, 3600)
    async def deathchat(self, ctx):
        message = '<@&1014881120921321543>'
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(title='💀| Deathchatping |🔔', description=f'{ctx.author.name} hat den ping ausgeführt\n'
                                                                        f'\n'
                                                                        f'Dieser ping ist abstellbar in den <#1073993336890871848>\n'
                                                                        f'PS wir nehmen uns das recht raus sollte dieser ping nix bringen, andere zu pingen\n'
                                                                        f'Hate etc wird schwerstens bestraft, (Keine Angst, wir sind Hard aber Fair)', colour=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.send(message)
        await ctx.respond(file=file, embed=embed)

    @deathchat.error
    async def deathchat_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title=' ❌| Error | ❌',
                               description="Dies ist eine Teamfunktion, bewerbe dich gerne fürs Team unter: <#1073702332082172084>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.send(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /deathchat auszuführen')
        elif isinstance(error, commands.CommandOnCooldown):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title=' ❌| Error | ❌',
                               description=f"Du musst noch {error.retry_after:.2f} Sekunden warten bis du den Command neuausführen kannst",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.send(file=file, embed=em, delete_after=15)

def setup(bot):
    bot.add_cog(Special(bot))
