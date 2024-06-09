import discord
from discord.ext import commands
from discord.commands import slash_command, Option

OPTIONS = ['Voice', 'Deathchat', 'Team', 'Admin']

class Special(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Pings command with multiple options.")
    async def pings(self, ctx, option: Option(str, "Choose an option", choices=OPTIONS)):
        if option == 'Deathchat':
            await self.deathchat(ctx)
        elif option == 'Team':
            await self.team(ctx)
        elif option == 'Admin':
            await self.admin(ctx)
        elif option == 'Voice':
            await self.voice(ctx)
        else:
            await ctx.respond("Invalid option selected.", ephemeral=True)

    async def deathchat(self, ctx: discord.ApplicationContext):
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

    async def team(self, ctx: discord.ApplicationContext):
        if 1070336143373119593 not in [role.id for role in ctx.author.roles]:
            await self.send_error(ctx, '"Dies ist eine Teamfunktion, bewerbe dich gerne fürs Team unter: <#1073702332082172084>"')
            return

        message = '<@&1044557317947019264>'
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(title='💀| Teamping |🔔', description=f'{ctx.author.name} hat den ping ausgeführt', colour=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.send(message)
        await ctx.respond(file=file, embed=embed)

    async def admin(self, ctx: discord.ApplicationContext):
        if 1044557317947019264 not in [role.id for role in ctx.author.roles]:
            await self.send_error(ctx, "Dies ist eine Adminfunktion.")
            return

        message = '<@696282645100888086>'
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(title='💀| Adminping |🔔', description=f'{ctx.author.name} hat den ping ausgeführt', colour=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.send(message)
        await ctx.respond(file=file, embed=embed)

    async def voice(self, ctx: discord.ApplicationContext):
        message = '<@&1248706499539238956>'
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(title='🔊| Voiceping |🔔', description=f'{ctx.author.name} hat den ping ausgeführt\n'
                                                                   'Wie es aussieht sucht da jemand nen call\n'
                                                                   'Hoffe wir finden schnell Leute die sich anschließen <3', colour=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.send(message)
        await ctx.respond(file=file, embed=embed)

    async def send_error(self, ctx: discord.ApplicationContext, error_message: str):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        em = discord.Embed(title=' ❌| Error | ❌', description=error_message, color=discord.Color.red())
        em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.send(file=file, embed=em, delete_after=15)

    @commands.slash_command(description='📝┃Sende die Liste der Server-Emojis')
    async def emojilist(self, ctx: discord.ApplicationContext):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(
            title='Emojis',
            description='',
            color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        if len(ctx.guild.emojis) > 50:
            embed_2 = discord.Embed(
                title='❌ | Error | ❌',
                description='Anscheinend gibt es zu viele Emojis auf diesem Server :( \nIch bin dadurch leider etwas eingeschränkt',
                color=discord.Color.dark_red())
            embed_2.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=embed_2, delete_after=120)
        else:
            for emoji in ctx.guild.emojis:
                embed.description += f'{emoji} - `{emoji}`\n'
            await ctx.respond(file=file, embed=embed, delete_after=120)

    @commands.slash_command(description='.')
    @commands.has_permissions(administrator=True)
    async def coming_soon(self, ctx: discord.ApplicationContext):
        message2 = 'erfolgreich gesendet'
        message = '# Coming Soon <a:Loading:1073700976000782396>'
        await ctx.respond(message2, ephemeral=True)
        await ctx.send(message)

    @coming_soon.error
    async def coming_soon_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.MissingPermissions):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            em = discord.Embed(title=' ❌| Error | ❌',
                               description="Leider ist dies eine Admin Option.\nWenn du Hilfe brauchst, melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.send(file=file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /coming_soon auszuführen')

def setup(bot):
    bot.add_cog(Special(bot))