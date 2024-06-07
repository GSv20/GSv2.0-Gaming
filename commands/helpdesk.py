from discord.ext import commands
import discord
import asyncio

class helpdesk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(helpdesk_View())

    @commands.slash_command(description="Schicke das Rollenmenü in einen Channel")
    @commands.has_permissions(administrator=True)
    async def helpdesk(self, ctx):
        channel = self.bot.get_channel(1120360814331838514)
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be

        embed_sucefull = discord.Embed(title='.', description='', color=color)
        embed_sucefull.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        embed = discord.Embed(title='.', description='', color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await ctx.respond(file=file, embed=embed_sucefull)
        await channel.send(file=file, embed=embed, view=helpdesk_View())

def setup(bot):
    bot.add_cog(helpdesk(bot))

class helpdesk_View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Community Manager", value="cm"),
        discord.SelectOption(label="Teamleitung", value="tl"),
        discord.SelectOption(label="Moderator", value="mod"),
        discord.SelectOption(label='Supporter', value="supp"),
        discord.SelectOption(label='Leave', value='leave')]

    @discord.ui.select(
        placeholder="Helpdesk",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="Helpdesk")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        message = ""

        if selected_value == "cm":
            message = "Du hast Community Manager gewählt."
        elif selected_value == "tl":
            message = "Du hast Teamleitung gewählt."
        elif selected_value == "mod":
            message = "Du hast Moderator gewählt."
        elif selected_value == "supp":
            message = "Du hast Supporter gewählt."
        elif selected_value == "leave":
            message = "Du hast Leave gewählt."

        color = 0x2596be
        embed = discord.Embed(title='Plattform Auswahl', description=message, color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        await interaction.response.send_message(embed=embed, ephemeral=True)