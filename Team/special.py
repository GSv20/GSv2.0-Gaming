import discord
from discord.ext import commands
from discord.commands import slash_command, Option

OPTIONS = ['Voice', 'Deathchat', 'Team', 'Admin']


class Special(commands.Cog):
    file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
    color = 0x2596be
    embed = discord.Embed(color=color)

    def __init__(self, bot):
        self.embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
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
        self.embed.title = '💀| Deathchatping |🔔'
        self.embed.description = f'''{ctx.author.name} hat den ping ausgeführt\n'
                                 \nDieser ping ist abstellbar in den <#1073993336890871848>
                                 \nPS wir nehmen uns das recht raus sollte dieser ping nix bringen, andere zu pingen
                                 \nHate etc wird schwerstens bestraft, (Keine Angst, wir sind Hard aber Fair)'''
        await ctx.send(message)
        await ctx.respond(file=self.file, embed=self.embed)

    async def team(self, ctx: discord.ApplicationContext):
        if 1070336143373119593 not in [role.id for role in ctx.author.roles]:
            await self.send_error(ctx,
                                  '"Dies ist eine Teamfunktion, bewerbe dich gerne fürs Team unter: <#1073702332082172084>"')
            return

        message = '<@&1044557317947019264>'
        self.embed.title = '💀| Teamping |🔔'
        self.embed.description = f'{ctx.author.name} hat den ping ausgeführt'
        await ctx.send(message)
        await ctx.respond(file=self.file, embed=self.embed)

    async def admin(self, ctx: discord.ApplicationContext):
        if 1044557317947019264 not in [role.id for role in ctx.author.roles]:
            await self.send_error(ctx, "Dies ist eine Adminfunktion.")
            return

        message = '<@696282645100888086>'
        self.embed.title = '💀| Adminping |🔔'
        self.embed.description = f'{ctx.author.name} hat den ping ausgeführt'
        await ctx.send(message)
        await ctx.respond(file=self.file, embed=self.embed)

    async def voice(self, ctx: discord.ApplicationContext):
        message = '<@&1248706499539238956>'
        self.embed.title = '🔊| Voiceping |🔔'
        self.embed.description = f'''{ctx.author.name} hat den ping ausgeführt\n
                             Wie es aussieht sucht da jemand nen call\n
                             Hoffe wir finden schnell Leute die sich anschließen <3'''
        await ctx.send(message)
        await ctx.respond(file=self.file, embed=self.embed)

    async def send_error(self, ctx: discord.ApplicationContext, error_message: str):
        em = discord.Embed(title=' ❌| Error | ❌', description=error_message, color=discord.Color.red())
        em.set_footer(text=self.embed.footer.text, icon_url=self.embed.footer.icon_url)
        await ctx.send(file=self.file, embed=em, delete_after=15)

    @commands.slash_command(description='📝┃Sende die Liste der Server-Emojis')
    async def emojilist(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title='Emojis',
            description='',
            color=self.embed.color)
        embed.set_footer(text=self.embed.footer.text, icon_url=self.embed.footer.icon_url)

        if len(ctx.guild.emojis) > 50:
            embed.title = '❌ | Error | ❌',
            embed.description = 'Anscheinend gibt es zu viele Emojis auf diesem Server :( \nIch bin dadurch leider etwas eingeschränkt',
            embed.color = discord.Color.dark_red()
        else:
            for emoji in ctx.guild.emojis:
                embed.description += f'{emoji} - `{emoji}`\n'
        await ctx.respond(file=self.file, embed=embed, delete_after=120)

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
            em = discord.Embed(title=' ❌| Error | ❌',
                               description="Leider ist dies eine Admin Option.\nWenn du Hilfe brauchst, melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.send(file=self.file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /coming_soon auszuführen')


def setup(bot):
    bot.add_cog(Special(bot))