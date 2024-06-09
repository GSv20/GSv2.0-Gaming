from discord.ext import commands
from discord.commands import slash_command
import discord
import asyncio
from discord.ui import Button


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(VIEWNAME())

    @slash_command(description='sende die Ticket Nachricht')
    @commands.has_permissions(administrator=True)
    async def tickets(self, ctx):
        em = discord.Embed(
            title=f'{ctx.guild.name} | Tickets',
            description='Willkommen im Support, Klicke unten und wähle ein Thema für Support\nIch hoffe das Support dir bei deinem Anliegen helfen kann',
            color=discord.Color.dark_gold()
        )
        em.set_thumbnail(url=f"{ctx.guild.icon}")
        em.set_image(url='https://cdn.discordapp.com/attachments/1073711669731151904/1216637088611696690/1666017515339-Yz02aFUJGDLIsbeaKtOUhf1E.png?ex=66011c95&is=65eea795&hm=105c903b16fca8586a7b432feeb8753c7168ebc2a412aceaedbae9b08fa487fb&')
        em.set_footer(
            icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&",
            text="Powered by GSV ⚡")
        await ctx.respond('Ticket Message wurde gesendet', ephemeral=True)

        channel = self.bot.get_channel(1073700885886152837)  # füge die Channel ID ein, wo die Ticket Nachricht mit dem Dropdown Menu geschickt werden soll
        await channel.send(embed=em, view=VIEWNAME())

    @tickets.error
    async def tickets_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title='Support Anfrage',
                               description="Leider ist dies eine Admin Option\nWenn du Hilfe brauchst melde dich gerne im Support:\n<#1073700885886152837>",
                               color=discord.Color.red())
            em.set_footer(text="Powered by GSV ⚡",
                          icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
            await ctx.respond(embed=em, delete_after=15)
            print(f'{ctx.author.name} hat versucht /tickets auszuführen')


def setup(bot):
    bot.add_cog(Ticket(bot))


options = [
    discord.SelectOption(label='Allgemein Support', description='Allgemeiner Support für alle anderen Themen', emoji='📩', value='1'),
    discord.SelectOption(label='User Report', description='Wähle diese Option um eine Partnerschaft zu beantragen', emoji='💫', value='2'),
    discord.SelectOption(label='Coding Wünsche', description='Wähle diese Option wenn du einen Bug gefunden hast', emoji='👩‍💻', value='3')
]


class VIEWNAME(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder='Wähle hier die Art des Tickets',
        options=options,
        custom_id='Ticket'
    )
    async def select_callback(self, select, interaction):
        member = interaction.user
        bot = interaction.bot

        if '1' in interaction.data['values']:
            cat = bot.get_channel(1073702320870793328)  # füge die Categorie ID ein, wo die Tickets erstellt werden sollen

            ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}',
                                                                         category=cat,
                                                                         topic=f'Ticket by {interaction.user} \nbot-ID: {interaction.user.id}')
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                 view_channel=True)
            await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
            try:
                em1 = discord.Embed(
                    title='📬 Ticket open!',
                    description=f'{member.mention}, Ich habe dein Ticket erstellt\nHier findest du es: {ticket_channel.mention}',
                    color=discord.Color.green()
                )
                em1.set_footer(text="Powered by GSV ⚡",
                              icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
                await interaction.response.send_message(embed=em1, ephemeral=True)

            except:
                em1E = discord.Embed(
                    title='❌ Error!',
                    description=f'{member.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>',
                    color=discord.Color.red()
                )
                em1E.set_footer(text="Powered by GSV ⚡",
                              icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
                await interaction.response.send_message(embed=em1E, ephemeral=True)

            try:
                CloseButton = Button(label='Close Ticket', style=discord.ButtonStyle.red, custom_id='close')
                view = discord.ui.View(timeout=None)
                view.add_item(CloseButton)
                teamping = '<@&1044557317947019264>'

                em2 = discord.Embed(
                    title=f'Willkommen in deinem Ticket, {interaction.user.name}',
                    description='*Möchtest du dieses schließen, verwende bitte den Button unten*\n\n\n'
                                '**Bevor wir starten hat das Team noch einige Fragen an dich**\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                                '**↬** Wie können wir dir helfen\n'
                                '**↬** Was ist der Grund für die Ticket eröffnung\n'
                                '**↬** bei beantworteten Fragen wird sich ein Teammitglied sehr gerne um dich kümmern\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                    color=discord.Color.green()
                )
                em2.set_footer(text="Powered by GSV ⚡",
                                 icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
                message = '<@&989913773898891365>\n<@&1104810262269284392>\n<@&1106948915783291001>\n<@&1106949164379672586>'
                await ticket_channel.send(teamping)
                await ticket_channel.send(embed=em2, view=view)
                await asyncio.sleep(0.1)
                await ticket_channel.send(message, delete_after=0.1)

                async def button_callback(interaction):

                    CloseTicket = discord.Embed(
                        title=f"GSV Ticket System",
                        description=f"Dein Ticket wird in 3 Sekunden geschlossen und der Channel gelöscht",
                        color=discord.Color.red()
                    )
                    CloseTicket.set_footer(text="Powered by GSV ⚡",
                                  icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")

                    await interaction.response.send_message(embed=CloseTicket)
                    await asyncio.sleep(3)
                    await interaction.channel.delete()

                    TicketClosed = discord.Embed(
                        title=f"GSV Ticket System",
                        description=f"{interaction.user.mention}, Dein Ticket auf **{interaction.guild.name}** wurde geschlossen!\n",
                        color=discord.Color.dark_gold()
                    )

                    TicketClosed.add_field(name="\nDas könnten die Gründe sein:",
                                           value="**↬** Du hast nicht mehr geantwortet\n**↬** Deine Support anfrage wurde erfolreich bearbeitet\n\n**✺ Wenn du weitere Hilfe brauchst zögere nicht in <#1073700885886152837> ein weiteres Ticket zu eröffnen ✺**\n",
                                           inline=False)
                    TicketClosed.add_field(name="Ticket Owner", value=f"{interaction.user.mention}", inline=True)
                    TicketClosed.add_field(name="Ticket Name", value=f"{ticket_channel}", inline=True)
                    TicketClosed.set_thumbnail(
                        url="https://cdn.discordapp.com/attachments/1073711669731151904/1107462738692816956/tenor.gif"
                    )
                    TicketClosed.set_footer(text="Powered by GSV ⚡",
                                           icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
                    await member.send(embed=TicketClosed)

                CloseButton.callback = button_callback
                return


            except:
                em2E = discord.Embed(
                    title='❌ Error!',
                    description=f'{member.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>',
                    color=discord.Color.red()
                )
                em2E.set_footer(text="Powered by GSV ⚡",
                                       icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")

                await ticket_channel.send(embed=em2E)

        if '2' in interaction.data['values']:
            cat = bot.get_channel(1073702320870793328)  # füge die Categorie ID ein, wo die Tickets erstellt werden sollen

            ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}',
                                                                         category=cat,
                                                                         topic=f'Ticket by {interaction.user} \nbot-ID: {interaction.user.id}')
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                 view_channel=True)
            await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
            try:
                em1 = discord.Embed(
                    title='📬 Ticket open!',
                    description=f'{member.mention}, Ich habe dein Ticket erstellt\nHier findest du es: {ticket_channel.mention}',
                    color=discord.Color.green()
                )
                em1.set_footer(text="Powered by GSV ⚡",
                               icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
                await interaction.response.send_message(embed=em1, ephemeral=True)

            except:
                em1E = discord.Embed(
                    title='❌ Error!',
                    description=f'{member.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>',
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=em1E, ephemeral=True)

            try:
                CloseButton = Button(label='Close Ticket', style=discord.ButtonStyle.red, custom_id='close')
                view = discord.ui.View(timeout=None)
                view.add_item(CloseButton)
                teamping = '<@&1044557317947019264>'

                em2 = discord.Embed(
                    title=f'Willkommen in deinem Ticket, {interaction.user.name}',
                    description='*Möchtest du dieses schließen, verwende bitte den Button unten*\n\n\n'
                                '**Bevor wir starten hat das Team noch einige Fragen an dich**\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                                '**↬** Gründe warum du eine Partnerschaft möchest\n'
                                '**↬** Anzahl der User deines Servers\n'
                                '**↬** Link zu deinem Server\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                    color=discord.Color.green()
                )
                em2.set_footer(text="Powered by GSV ⚡",
                               icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
                message = '<@&989913773898891365>\n<@&1104810262269284392>\n<@&1106948915783291001>\n<@&1106949164379672586>'
                await ticket_channel.send(teamping)
                await ticket_channel.send(embed=em2, view=view)
                await asyncio.sleep(0.1)
                await ticket_channel.send(message, delete_after=0.1)

                async def button_callback(interaction):

                    CloseTicket = discord.Embed(
                        title="GSV Ticket System",
                        description="Dein Ticket wird in 3 Sekunden geschlossen und der Kanal gelöscht",
                        color=discord.Color.red()
                    )

                    await interaction.response.send_message(embed=CloseTicket)
                    await asyncio.sleep(3)
                    await interaction.channel.delete()

                    TicketClosed = discord.Embed(
                        title=f"GSV Ticket System",
                        description=f"{interaction.user.mention}, Dein Ticket auf **{interaction.guild.name}** wurde geschlossen!\n",
                        color=discord.Color.dark_gold()
                    )

                    TicketClosed.add_field(name="\nDas könnten die Gründe sein:",
                                           value="**↬** Du hast nicht mehr geantwortet\n**↬** Deine Support anfrage wurde erfolreich bearbeitet\n\n**✺ Wenn du weitere Hilfe brauchst zögere nicht in <#1073700885886152837> ein weiteres Ticket zu eröffnen ✺**\n",
                                           inline=False)
                    TicketClosed.add_field(name="Ticket Owner", value=f"{interaction.user.mention}", inline=True)
                    TicketClosed.add_field(name="Ticket Name", value=f"{ticket_channel}", inline=True)
                    TicketClosed.set_thumbnail(
                        url="https://cdn.discordapp.com/attachments/1073711669731151904/1107462738692816956/tenor.gif"
                    )
                    TicketClosed.set_footer(text="Powered by GSV ⚡",
                                            icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
                    await member.send(embed=TicketClosed)

                CloseButton.callback = button_callback
                return


            except:
                em2E = discord.Embed(
                    title='❌ Error!',
                    description=f'{member.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>',
                    color=discord.Color.red()
                )
                await ticket_channel.send(embed=em2E)

        if '3' in interaction.data['values']:
            cat = bot.get_channel(1073702320870793328)  # füge die Categorie ID ein, wo die Tickets erstellt werden sollen

            ticket_channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}',
                                                                         category=cat,
                                                                         topic=f'Ticket by {interaction.user} \nbot-ID: {interaction.user.id}')
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                 view_channel=True)
            await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
            try:
                em1 = discord.Embed(
                    title='📬 Ticket open!',
                    description=f'{member.mention}, Ich habe dein Ticket erstellt\nHier findest du es: {ticket_channel.mention}',
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=em1, ephemeral=True)

            except:
                em1E = discord.Embed(
                    title='❌ Error!',
                    description=f'{member.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>',
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=em1E, ephemeral=True)

            try:
                CloseButton = Button(label='Close Ticket', style=discord.ButtonStyle.red, custom_id='close')
                view = discord.ui.View(timeout=None)
                view.add_item(CloseButton)
                teamping = '<@&1044557317947019264>'

                em2 = discord.Embed(
                    title=f'Willkommen in deinem Ticket, {interaction.user.name}',
                    description='*Möchtest du dieses schließen, verwende bitte den Button unten*\n\n\n'
                                '**Bevor wir starten hat das Team noch einige Fragen an dich**\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n'
                                '**↬** Welchen Bug möchtest du reporten\n'
                                '**↬** Was für auswirkungen hat dieser auf den Server?\n'
                                '▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬',
                    color=discord.Color.green()
                )
                em2.set_footer(text="Powered by GSV ⚡",
                               icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
                message = '<@&989913773898891365>\n<@&1104810262269284392>\n<@&1106948915783291001>\n<@&1106949164379672586>'
                await ticket_channel.send(teamping)
                await ticket_channel.send(embed=em2, view=view)
                await asyncio.sleep(0.1)
                await ticket_channel.send(message, delete_after=0.1)

                async def button_callback(interaction):

                    CloseTicket = discord.Embed(
                        title="GSV Ticket System",
                        description="Dein Ticket wird in 3 Sekunden geschlossen und der Kanal gelöscht",
                        color=discord.Color.red()
                    )

                    await interaction.response.send_message(embed=CloseTicket)
                    await asyncio.sleep(3)
                    await interaction.channel.delete()

                    TicketClosed = discord.Embed(
                        title=f"GSV Ticket System",
                        description=f"{interaction.user.mention}, Dein Ticket auf **{interaction.guild.name}** wurde geschlossen!\n",
                        color=0xffffff
                    )

                    TicketClosed.add_field(name="\nDas könnten die Gründe sein:",
                                           value="**↬** Du hast nicht mehr geantwortet\n**↬** Deine Support anfrage wurde erfolreich bearbeitet\n\n**✺ Wenn du weitere Hilfe brauchst zögere nicht in <#1073700885886152837> ein weiteres Ticket zu eröffnen ✺**\n",
                                           inline=False)
                    TicketClosed.add_field(name="Ticket Owner", value=f"{interaction.user.mention}", inline=True)
                    TicketClosed.add_field(name="Ticket Name", value=f"{ticket_channel}", inline=True)
                    TicketClosed.set_thumbnail(
                        url="https://cdn.discordapp.com/attachments/1073711669731151904/1107462738692816956/tenor.gif"
                    )
                    TicketClosed.set_footer(text="Powered by GSV ⚡",
                                            icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
                    await member.send(embed=TicketClosed)

                CloseButton.callback = button_callback
                return


            except:
                em2E = discord.Embed(
                    title='📬 Error!',
                    description=f'{member.mention}, Leider konnte ich dein Ticket nicht erstellen\nMelde dies bitte: <@696282645100888086>',
                    color=discord.Color.red()
                )
                await ticket_channel.send(embed=em2E)