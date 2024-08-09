from discord.ext import commands
from discord.commands import slash_command
import discord
import asyncio
from discord.ui import Button

class ApplicationCog(commands.Cog):
    file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
    color = 0x2596be

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ApplicationView())

    @slash_command(description='Sende den Bewerbungstext')
    @commands.has_permissions(administrator=True)
    async def apptextsend(self, ctx):
        em = discord.Embed(
            title=f'{ctx.guild.name} | Tickets',
            description='Willkommen im Support, Klicke unten und wähle ein Thema für Support\nIch hoffe das Support dir bei deinem Anliegen helfen kann',
            color=self.color
        )
        em.set_thumbnail(url=f"{ctx.guild.icon}")
        em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.respond('Ticket Message wurde gesendet', ephemeral=True)

        channel = self.bot.get_channel(1073702332082172084)
        await channel.send(file=self.file, embed=em, view=ApplicationView())  # Hier wird ApplicationView korrekt instanziiert.

    @apptextsend.error
    async def apptextsend_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title='Support Anfrage',
                               description="Leider ist dies eine Admin Option\nWenn du Hilfe brauchst melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=self.file, embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /apptextsend auszuführen')


def setup(bot):
    bot.add_cog(ApplicationCog(bot))


class ApplicationView(discord.ui.View):
    file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
    color = 0x2596be

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Bewerben", style=discord.ButtonStyle.success, custom_id='button:Appbutton')
    async def button_callback(self, button, interaction):
        cat = interaction.guild.get_channel(1073702320870793328)  # füge die Kategorie ID ein, wo die Tickets erstellt werden sollen

        ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}',
                                                                     category=cat,
                                                                     topic=f'Ticket by {interaction.user} \nUser-ID: {interaction.user.id}')
        await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, view_channel=True)
        await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
        try:
            em1 = discord.Embed(
                title='📬 Ticket open!',
                description=f'{interaction.user.mention}, Ich habe dein Ticket erstellt\nHier findest du es: {ticket_channel.mention}',
                color=discord.Color.green())
            em1.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=self.file, embed=em1, ephemeral=True)
        except:
            em1E = discord.Embed(
                title='❌ Error!',
                description=f'{interaction.user.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>',
                color=discord.Color.red())
            em1E.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=self.file, embed=em1E, ephemeral=True)
        try:
            em2 = discord.Embed(
                title=f'Willkommen in deinem Bewerbungsgespräch, {interaction.user.name}',
                description='*Möchtest du dieses schließen, verwende bitte den Button unten*\n\n\n'
                            '**Bevor wir starten hat das Team noch einige Fragen an dich**\n'
                            '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                            '**↬** auf welche Stelle möchtest du dich bewerben?\n'
                            '**↬** warum sollten wir dich nehmen\n'
                            '**↬** was erwartest du von uns\n'
                            '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                color=self.color)
            em2.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            teamping = '<@&1044557317947019264>'
            message = '<@&989913773898891365>\n<@&1104810262269284392>\n<@&1106948915783291001>\n<@&1106949164379672586>'
            await ticket_channel.send(teamping)
            await ticket_channel.send(file=self.file, embed=em2, view=CloseButtonView())
            await asyncio.sleep(0.1)
            await ticket_channel.send(message, delete_after=0.1)
        except:
            em2E = discord.Embed(
                title='❌ Error!',
                description=f'{interaction.user.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>',
                color=discord.Color.red())
            em2E.set_footer(text="Powered by GSV ⚡",
                            icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
            await ticket_channel.send(embed=em2E)


class CloseButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Close Ticket', style=discord.ButtonStyle.red, custom_id='Button:Close')
    async def closebutton(self, button: discord.ui.Button, interaction: discord.Interaction):
        closeticket = discord.Embed(
            title="GSV Ticket System",
            description="Dein Ticket wird in 3 Sekunden geschlossen und der Kanal gelöscht",
            color=discord.Color.red()
        )

        await interaction.response.send_message(embed=closeticket)
        await asyncio.sleep(3)
        await interaction.channel.delete()

        ticketclosed = discord.Embed(
            title=f"GSV Ticket System",
            description=f"{interaction.user.mention}, Dein Ticket auf **{interaction.guild.name}** wurde geschlossen!\n",
            color=0xffffff
        )

        ticketclosed.add_field(name="\nDas könnten die Gründe sein:",
                               value="**↬** Du hast nicht mehr geantwortet\n**↬** Deine Support Anfrage wurde erfolgreich bearbeitet\n\n**✺ Wenn du weitere Hilfe brauchst, zögere nicht in <#1073700885886152837> ein weiteres Ticket zu eröffnen ✺**\n",
                               inline=False)
        ticketclosed.add_field(name="Ticket Owner", value=f"{interaction.user.mention}", inline=True)
        ticketclosed.add_field(name="Ticket Name", value=f"{interaction.channel.name}", inline=True)
        ticketclosed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1073711669731151904/1107462738692816956/tenor.gif"
        )
        ticketclosed.set_footer(text="Powered by GSV ⚡",
                                icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
        await interaction.user.send(embed=ticketclosed)