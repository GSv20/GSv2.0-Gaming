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
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be

        embed_successful = discord.Embed(title='<:yes:1073716074140414013> | Erfolgreich gesendet',
                                         description='Das Helpdesk wurde erfolgreich gesendet / aktualisiert',
                                         color=color)
        embed_successful.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        embed = discord.Embed(
            title='<a:5006_i_support:1075166049785364543> | Helpdesk | <:TA_Supporter:1075169298399633448> ',
            description='Willkommen im Helpdesk von GSv\n'
                        'Hier wirst du über deine Aufgaben informiert, und ebenso die Möglichkeiten welche sich dir hier bieten\n'
                        'Wähle weiter unten einfach deine Rolle aus um mehr über sie und ihre Rechte zu erfahren\n\n'
                        'Das Helpdesk steht dir BTW Immer zur Verfügung\n'
                        'jz lass uns rocken\n'
                        '<:G_:1158950908613361694><:S_:1158950928586657802><:v_:1158950963009310770>', color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.respond(file=file, embed=embed_successful, ephemeral=True)
        await channel.send(file=file, embed=embed, view=HelpdeskView())


def setup(bot):
    bot.add_cog(HelpdeskCog(bot))


class HelpdeskView(discord.ui.View):
    file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Community Manager", value="cm"),
        discord.SelectOption(label="Teamleitung", value="tl"),
        discord.SelectOption(label="Moderator", value="mod"),
        discord.SelectOption(label='Supporter', value="supp", emoji='<:TA_Supporter:1075169298399633448>'),
        discord.SelectOption(label='Leave', value='leave', emoji='🚧')]

    @discord.ui.select(
        placeholder="Helpdesk",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="Helpdesk")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        color = 0x2596be

        if selected_value == "cm":
            cm_embed = discord.Embed(title='Community Manager',
                                     description='Informationen und Rechte des Community Managers...', color=color)
            cm_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=self.file, embed=cm_embed, ephemeral=True)

        elif selected_value == "tl":
            tl_embed = discord.Embed(title='Teamleitung', description='Informationen und Rechte der Teamleitung...',
                                     color=color)
            tl_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=self.file, embed=tl_embed, ephemeral=True)

        elif selected_value == "mod":
            mod_embed = discord.Embed(title='Moderator', description='Du hast Moderator gewählt.', color=color)
            mod_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=self.file, embed=mod_embed, ephemeral=True)

        elif selected_value == "supp":
            supp_embed = discord.Embed(title='Supporter', description='Du hast Supporter gewählt.', color=color)
            supp_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=self.file, embed=supp_embed, ephemeral=True)

        elif selected_value == "leave":
            leave_embed = discord.Embed(title='Leave', description='Du hast Leave gewählt.', color=color)
            leave_embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.response.send_message(file=self.file, embed=leave_embed, ephemeral=True)