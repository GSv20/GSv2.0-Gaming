import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import asyncio


class role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(plattformen())
        self.bot.add_view(geschlechtsauswahl())
        self.bot.add_view(sexualitat())
        self.bot.add_view(beziehungsstatus())
        self.bot.add_view(alter())
        self.bot.add_view(Extras())
        self.bot.add_view(farbenauswahl())
        self.bot.add_view(pingrollen())

    @slash_command(description="Schicke eine Event-Nachricht ab")
    @commands.has_permissions(administrator=True)
    async def selfrole(self, ctx,
                       text: Option(str, "Wähle einen Text aus", choices=[
                           "Sexualität",
                           "Beziehungsstatus",
                           "Geschlechtsauswahl",
                           "Alter",
                           "Extras",
                           "Farbenauswahl",
                           "Pingrollen",
                           "Plattformen"], required=True),
                       channel: Option(discord.TextChannel, "Der Channel, in dem das Menü gesendet werden soll", required=False)):

        if channel is None:
            channel = ctx.channel
        if text == "Sexualität":
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
                title="Sexualität",
                description="Freiwillige Angabe\nWenn du nicht willst, musst du nicht",
                color=color)
            embed.set_image(
                url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031717015420938/sexualitat.png')
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            view = sexualitat()
            await ctx.respond("Nachricht geschickt", ephemeral=True)
            await channel.send(file=file, embed=embed, view=view)

        elif text == "Beziehungsstatus":
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
                title="Beziehungsstatus",
                description="Angaben sind freiwillig",
                color=color)
            embed.set_image(
                url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031757754433657/beziehungsstatus.jpeg')
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            view = beziehungsstatus()
            await ctx.respond("Nachricht geschickt", ephemeral=True)
            await channel.send(file=file, embed=embed, view=view)

        elif text == "Extras":
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
                title="Extras",
                description="",
                color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            view = Extras()
            await ctx.respond("Nachricht geschickt", ephemeral=True)
            await channel.send(file=file, embed=embed, view=view)

        elif text == "Geschlechtsauswahl":
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
                title="Geschlechtsauswahl",
                description="Angaben sind freiwillig",
                color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            view = geschlechtsauswahl()
            await ctx.respond("Nachricht geschickt", ephemeral=True)
            await channel.send(file=file, embed=embed, view=view)

        elif text == "Alter":
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
                title="Alter",
                description="Gebe hier dein Alter an",
                color=color)
            embed.set_image(
                url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031776511623188/Alter.jpeg')
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            view = alter()
            await ctx.respond("Nachricht geschickt", ephemeral=True)
            await channel.send(file=file, embed=embed, view=view)

        elif text == "Farbenauswahl":
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
                title="Farbenauswahl",
                description="Wähle unten im Menü die Rolle aus",
                color=color)
            embed.set_image(
                url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031796535099462/Farbenauswahl.jpeg')
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            view = farbenauswahl()
            await ctx.respond("Nachricht geschickt", ephemeral=True)
            await channel.send(file=file, embed=embed, view=view)

        elif text == "Pingrollen":
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
                title="Pingrollen",
                description="Drücke [hier](https://discord.com/channels/913082943495344179/1073993336890871848/1249873609091190868), "
                            "um zum anfang der Selfrols zu gelangen",
                color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            view = pingrollen()
            await ctx.respond("Nachricht geschickt", ephemeral=True)
            await channel.send(file=file, embed=embed, view=view)

        elif text == "Plattformen":
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
                title="Plattformen",
                description='Wähle deine Plattform bzw. Plattformen\n- Damit die anderen User Bescheid wissen, wie sie mit dir spielen können',
                color=color)
            embed.set_image(
                url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031589357588500/Plattformen.png')
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            view = plattformen()
            await ctx.respond("Nachricht geschickt", ephemeral=True)
            await channel.send(file=file, embed=embed, view=view)


def setup(bot):
    bot.add_cog(role(bot))


class plattformen(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="PC", value="pc"),
        discord.SelectOption(label="Playstation", value="playstation"),
        discord.SelectOption(label="Xbox", value="xbox"),
        discord.SelectOption(label="Switch", value="switch"),
        discord.SelectOption(label="Handy", value="handy")]

    @discord.ui.select(
        placeholder="Wähle deine Plattform aus",
        min_values=1,
        max_values=5,
        options=options,
        custom_id="plattform_select")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        roles = {
            "pc": 1014881098884456508,
            "playstation": 1014881100490883072,
            "xbox": 1014881101740781599,
            "switch": 1014881103204597800,
            "handy": 1014881104429326356}
        role_id = roles[selected_value]
        role = interaction.guild.get_role(role_id)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            message = f"Dir wurde die Rolle {role.mention} entfernt"
        else:
            await interaction.user.add_roles(role)
            message = f"Dir wurde {role.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


class geschlechtsauswahl(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Männlich ", value="mann"),
        discord.SelectOption(label="Weiblich ", value="weiblich"),
        discord.SelectOption(label="Divers ", value="divers")]

    @discord.ui.select(
        placeholder="Wähle dein Geschlecht aus",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="geschlecht_select")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        roles = {
            "mann": 1014881107461799966,
            "weiblich": 1014881108195807403,
            "divers": 1014881109596708955}
        role_id = roles.get(selected_value)
        role = interaction.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message("Die Rolle existiert nicht.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            message = f"Dir wurde die Rolle {role.mention} entfernt"
        else:
            await interaction.user.add_roles(role)
            message = f"Dir wurde {role.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


class sexualitat(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Hetero ", value="hetero"),
        discord.SelectOption(label="Lesbisch ", value="lesbisch"),
        discord.SelectOption(label="Schwul ", value="schwul"),
        discord.SelectOption(label="Bisexuell ", value="bisexuell"),
        discord.SelectOption(label="Queer ", value="queer"),
        discord.SelectOption(label="Transsexuell/Transgender ", value="t/t"),
        discord.SelectOption(label="Intersexuell ", value="intersexuell"),
        discord.SelectOption(label="Two-Spirits/Double Soul ", value="tsd"),
        discord.SelectOption(label="Pan Sexuell ", value="pan"),
        discord.SelectOption(label="Asexuell ", value="asexuell")]

    @discord.ui.select(
        placeholder="Wähle deine Sexualität aus",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="sexualitat_select")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        roles = {
            "hetero": 1074021595624001606,
            "lesbisch": 1052166815394041906,
            "schwul": 1052166937523793982,
            "bisexuell": 1052167193502158862,
            "queer": 1052167251593269249,
            "t/t": 1052167260611026995,
            "intersexuell": 1052167367905513572,
            "tsd": 1052167940721614890,
            "pan": 1069675619060813894,
            "asexuell": 1052167858051874816}
        role_id = roles.get(selected_value)
        role = interaction.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message("Die Rolle existiert nicht.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            message = f"Dir wurde die Rolle {role.mention} entfernt"
        else:
            await interaction.user.add_roles(role)
            message = f"Dir wurde {role.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


class beziehungsstatus(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Verliebt ", value="verliebt"),
        discord.SelectOption(label="Vergeben  ", value="vergeben "),
        discord.SelectOption(label="Verlobt ", value="verlobt"),
        discord.SelectOption(label="Verheiratet ", value="verheiratet"),
        discord.SelectOption(label="Single", value="Single"),
        discord.SelectOption(label="Kompliziert ", value="kompliziert")]

    @discord.ui.select(
        placeholder="Wähle dein beziehungsstatus aus",
        min_values=1,
        max_values=2,
        options=options,
        custom_id="beziehungsstatus_select")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        roles = {
            "verliebt": 1097841875550994573,
            "vergeben": 1014881111677079603,
            "verlobt": 1097875012595224576,
            "verheiratet": 1097874957188464810,
            "Single": 1014881112339787808,
            "kompliziert": 1014881113619038359}
        role_id = roles.get(selected_value)
        role = interaction.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message("Die Rolle existiert nicht.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            message = f"Dir wurde die Rolle {role.mention} entfernt"
        else:
            await interaction.user.add_roles(role)
            message = f"Dir wurde {role.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


class alter(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Unter 18 ", value="18-"),
        discord.SelectOption(label="18-20  ", value="18"),
        discord.SelectOption(label="Über 20 ", value="20+"),
        discord.SelectOption(label="Über 30 ", value="30+"),
        discord.SelectOption(label="Über 40", value="40+"),
        discord.SelectOption(label="Mehr als 50 ", value="50+")]

    @discord.ui.select(
        placeholder="Wähle dein Alter aus",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="alter_select")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        roles = {
            "18-": 1205648088832679966,
            "18": 1205648589980704788,
            "20+": 1205648736504512523,
            "30+": 1205648809481212054,
            "40+": 1205648843044159508,
            "50+": 1205648884135624704,}
        role_id = roles.get(selected_value)
        role = interaction.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message("Die Rolle existiert nicht.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            message = f"Dir wurde die Rolle {role.mention} entfernt"
        else:
            await interaction.user.add_roles(role)
            message = f"Dir wurde {role.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


class farbenauswahl(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Schwarz ", value="schwarz"),
        discord.SelectOption(label="Weiß", value="weiß"),
        discord.SelectOption(label="Grau", value="grau"),
        discord.SelectOption(label="Neon Blau", value="nblau"),
        discord.SelectOption(label="Lila", value="lila"),
        discord.SelectOption(label="Dunkel Lila", value="dlila"),
        discord.SelectOption(label="Pink", value="pink"),
        discord.SelectOption(label="Neon Pink", value="npink"),
        discord.SelectOption(label="Braun", value="braun"),
        discord.SelectOption(label="Gelb", value="gelb"),
        discord.SelectOption(label="Hellbraun", value="hbraun"),
        discord.SelectOption(label="Orange", value="orange"),
        discord.SelectOption(label="Rot", value="rot"),
        discord.SelectOption(label="Blau", value="blau"),
        discord.SelectOption(label="Dunkel Blau", value="dblau"),
        discord.SelectOption(label="Neon Grün", value="ngrün"),
        discord.SelectOption(label="Türkis", value="türkis"),
        discord.SelectOption(label="Dunkelgrün", value="dgrün")]

    @discord.ui.select(
        placeholder="Wähle deine Lieblingsfarbe aus",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="farbenauswahl_select")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        roles = {
            "schwarz": 1013601269828550666,
            "weiß": 1013601430533320785,
            "grau": 1013601666030903347,
            "nblau": 1013601113519439954,
            "lila": 1018236009382678618,
            "dlila": 1248605320503230505,
            "pink": 1013601424061517845,
            "npink": 1018273857355927552,
            "braun": 1013602130952720394,
            "gelb": 1013600724019593246,
            "hbraun": 1013602047150526505,
            "orange": 1013600724023791666,
            "rot": 1000149758175891486,
            "blau": 1013607823717969980,
            "dblau": 1013601776945074228,
            "ngrün": 1018473322796822540,
            "türkis": 1013600625973538816,
            "dgrün": 1028000709414752398,}
        role_id = roles.get(selected_value)
        role = interaction.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message("Die Rolle existiert nicht.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            message = f"Dir wurde die Rolle {role.mention} entfernt"
        else:
            await interaction.user.add_roles(role)
            message = f"Dir wurde {role.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


import discord


class Extras(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Dev Programm", value="dev")]

    @discord.ui.select(
        placeholder="Wähle hier Extras aus",
        min_values=1,
        max_values=1,
        options=options,
        custom_id="farbenauswahl_select")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        roles_dict = {
            "dev": 1224020966309498900,
        }
        role_id = roles_dict.get(selected_value)

        selected_role = interaction.guild.get_role(role_id)

        # Debug: Check if the role is found
        if selected_role is None:
            await interaction.response.send_message(f"Die Rolle mit der ID {role_id} existiert nicht.", ephemeral=True)
            return

        if selected_role in interaction.user.roles:
            await interaction.user.remove_roles(selected_role)
            message = f"Dir wurde die Rolle {selected_role.mention} entfernt"
        else:
            await interaction.user.add_roles(selected_role)
            message = f"Dir wurde {selected_role.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


class pingrollen(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Night Ping ", value="nping"),
        discord.SelectOption(label="Death Chat ping", value="dcp"),
        discord.SelectOption(label="News Ping", value="np"),
        discord.SelectOption(label="Voice Ping", value="voice"),
        discord.SelectOption(label="YouTube Ping", value="yt")]

    @discord.ui.select(
        placeholder="Wähle deine Pingrollen aus",
        min_values=1,
        max_values=5,
        options=options,
        custom_id="farbenauswahl_select")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        roles = {
            "nping": 1175593418475454534,
            "dcp": 1014881120921321543,
            "np": 1014881119990190122,
            "voice": 1248706499539238956,
            "yt": 1109457019037036684}
        role_id = roles.get(selected_value)
        role = interaction.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message("Die Rolle existiert nicht.", ephemeral=True)
            return

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            message = f"Dir wurde die Rolle {role.mention} entfernt"
        else:
            await interaction.user.add_roles(role)
            message = f"Dir wurde {role.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)