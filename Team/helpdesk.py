from discord.ext import commands
import discord
import asyncio


class HelpdeskCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(HelpdeskView())
        print('Helpdesk wurde geladen')

    @commands.slash_command(description="Aktualisiere das Helpdesk menü")
    @commands.has_permissions(administrator=True)
    async def helpdesk(self, ctx):
        channel = self.bot.get_channel(1120360814331838514)
        file1 = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be

        embed_successful = discord.Embed(title='<:yes:1073716074140414013> | Erfolgreich gesendet',
                                         description='Das Helpdesk wurde erfolgreich gesendet / aktualisiert',
                                         color=color)
        embed_successful.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        file2 = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        embed = discord.Embed(
            title='<a:5006_i_support:1075166049785364543> | Helpdesk | <:TA_Supporter:1075169298399633448> ',
            description='Willkommen im Helpdesk von GSv\n'
                        'Hier wirst du über deine Aufgaben informiert, und ebenso die Möglichkeiten welche sich dir hier bieten\n'
                        'Wähle weiter unten einfach deine Rolle aus um mehr über sie und ihre Rechte zu erfahren\n\n'
                        'Das Helpdesk steht dir BTW Immer zur Verfügung\n'
                        'jz lass uns rocken\n'
                        '<:G_:1158950908613361694><:S_:1158950928586657802><:v_:1158950963009310770>', color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.respond(file=file1, embed=embed_successful, ephemeral=True)
        await channel.send(file=file2, embed=embed, view=HelpdeskView())


def setup(bot):
    bot.add_cog(HelpdeskCog(bot))


class HelpdeskView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Official Dev", value="dev"),
        discord.SelectOption(label="Teamleitung", value="tl"),
        discord.SelectOption(label="Community Manager", value="cm"),
        discord.SelectOption(label="Test Moderator", value="tm"),
        discord.SelectOption(label="Supporter", value="supp"),
        discord.SelectOption(label="Test Supporter", value="tsupp"),
        discord.SelectOption(label="Leave", value="leave", emoji='🚧')]

    @discord.ui.select(
        placeholder="Wähle eine Option aus",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="helpdesk_select")
    async def callback(self, select, interaction: discord.Interaction):
        auswahl = select.values[0]

        if auswahl == "dev":
            embedd = discord.Embed(
                title="Aufgaben von einem Dev",
                description="1. Bot-Entwicklung und -Wartung 🤖:\n"
                            "- Entwickeln und Implementieren von Discord-Bots.\n"
                            "- Regelmäßige Aktualisierungen und Wartung der Bots, um sicherzustellen, dass sie reibungslos laufen und auf dem neuesten Stand sind.\n\n"
                            "2. Server-Management und -Optimierung 🔧:\n"
                            "- Einrichten und Konfigurieren von Server-Einstellungen, Rollen und Berechtigungen.\n"
                            "- Optimieren des Servers für eine bessere Benutzererfahrung, z.B. durch die Implementierung von Bots, die den Server organisieren und moderieren.\n\n"
                            "3. Implementierung neuer Funktionen 🚀:\n"
                            "- Hinzufügen neuer Features und Integrationen, um den Server attraktiver und benutzerfreundlicher zu gestalten.\n"
                            "- Integration von APIs und externen Diensten, um die Funktionalität des Servers zu erweitern."
            )
        elif auswahl == "tl":
            embedd = discord.Embed(
                title="Aufgaben der Teamleitung",
                description="**1. Leitung und Koordination des Teams 🧑‍💼:**\n"
                            "- Führen und Motivieren des Teams.\n"
                            "- Planen und Verteilen von Aufgaben.\n"
                            "- Sicherstellen einer reibungslosen Zusammenarbeit.\n\n"
                            "**2. Strategie und Planung 📈:**\n"
                            "- Entwickeln von Strategien zur Verbesserung des Servers.\n"
                            "- Planen und Durchführen von Projekten.\n"
                            "- Evaluieren und Anpassen von Maßnahmen.\n\n"
                            "**3. Kommunikation und Feedback 💬:**\n"
                            "- Regelmäßige Kommunikation mit dem Team.\n"
                            "- Einholen und Geben von Feedback.\n"
                            "- Vermitteln zwischen Teammitgliedern und der Community."
            )
        elif auswahl == "cm":
            embedd = discord.Embed(
                title="Aufgaben eines Community Managers",
                description="**1. Community-Engagement 🌐:**\n"
                            "- Interaktion mit den Mitgliedern.\n"
                            "- Organisieren von Events und Aktivitäten.\n"
                            "- Förderung einer positiven und aktiven Community.\n\n"
                            "**2. Moderation und Support 🛠️:**\n"
                            "- Überwachen von Diskussionen.\n"
                            "- Beantworten von Fragen und Anfragen.\n"
                            "- Behandeln von Konflikten und Problemen.\n\n"
                            "**3. Content-Erstellung und -Verwaltung 📋:**\n"
                            "- Erstellen und Teilen von Inhalten.\n"
                            "- Aktualisieren und Pflegen der Server-Ressourcen.\n"
                            "- Entwickeln neuer Ideen zur Mitgliederbindung."
            )
        elif auswahl == "tm":
            embedd = discord.Embed(
                title="Aufgaben eines Test Moderators",
                description="**1. Unterstützung bei der Moderation 👀:**\n"
                            "- Überwachen von Chats und Aktivitäten.\n"
                            "- Durchsetzen der Server-Regeln.\n"
                            "- Melden von Verstößen an höheres Personal.\n\n"
                            "**2. Sammeln von Feedback 📝:**\n"
                            "- Einholen von Rückmeldungen der Community.\n"
                            "- Weitergeben von Verbesserungsvorschlägen.\n"
                            "- Teilnahme an Moderatoren-Besprechungen.\n\n"
                            "**3. Ausbildung und Training 📚:**\n"
                            "- Lernen der Moderationsrichtlinien und -tools.\n"
                            "- Üben und Anwenden neuer Moderationstechniken."
            )
        elif auswahl == "supp":
            embedd = discord.Embed(
                title="Aufgaben eines Supporters",
                description="**1. Hilfe und Unterstützung 🙋:**\n"
                            "- Beantworten von Fragen und Anliegen der Mitglieder.\n"
                            "- Bereitstellen von Anleitungen und Lösungen.\n"
                            "- Unterstützung bei technischen Problemen.\n\n"
                            "**2. Betreuung neuer Mitglieder 👋:**\n"
                            "- Begrüßen und Einweisen neuer Mitglieder.\n"
                            "- Erklären der Server-Regeln und -Strukturen.\n"
                            "- Helfen beim Einstieg und der Nutzung des Servers.\n\n"
                            "**3. Feedback und Verbesserung 📈:**\n"
                            "- Sammeln von Rückmeldungen der Mitglieder.\n"
                            "- Weiterleiten von Vorschlägen und Beschwerden.\n"
                            "- Mitwirken an Verbesserungsmaßnahmen."
            )
        elif auswahl == "tsupp":
            embedd = discord.Embed(
                title="Aufgaben eines Test Supporters",
                description="**1. Unterstützung des Support-Teams 🛠️:**\n"
                            "- Beantworten einfacher Anfragen.\n"
                            "- Weiterleiten komplexer Probleme an erfahrene Supporter.\n"
                            "- Lernen der Support-Prozesse und -tools.\n\n"
                            "**2. Sammeln von Feedback 📝:**\n"
                            "- Einholen von Rückmeldungen der Nutzer.\n"
                            "- Weitergeben von Verbesserungsvorschlägen.\n"
                            "- Teilnahme an Support-Meetings.\n\n"
                            "**3. Ausbildung und Training 📚:**\n"
                            "- Lernen der Support-Richtlinien und -verfahren.\n"
                            "- Teilnahme an Schulungen und Workshops.\n"
                            "- Üben und Anwenden neuer Support-Techniken.")
        elif auswahl == "leave":
            leave_embed = discord.Embed(title='Leave', description='Du hast Leave gewählt.', color=discord.dark_red())
            leave_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=self.file, embed=leave_embed, ephemeral=True)
        else:
            embedd = discord.Embed(
                title="Unbekannte Auswahl",
                description="Die ausgewählte Option ist derzeit nicht definiert."
            )

        await interaction.response.send_message(embed=embedd, ephemeral=True)

class leave(discord.ui.View):
    def __init__(self):
        super().__init__()
        #leave logik