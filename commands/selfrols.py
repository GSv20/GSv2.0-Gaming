import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import asyncio
#embeds anpassen bei den hinzugefügten rollen

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
        self.bot.add_view(farbenauswahl())
        self.bot.add_view(pingrollen())
        self.bot.add_view(extras())

    @slash_command(discription="Schicke das rollen menü in einen channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def selfrols(self, ctx, channel: Option(discord.TextChannel, "Der Channel in dem das Menü gesendet werden soll", required=True)):
        link = 'https://discord.com/channels/913082943495344179/1073993336890871848/1241777968783818854'
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(title="Plattformen", description='Wähle deine Plattform bzw. Plattformen\n'
                                                                '- Damit die anderen User bescheid wissen wie sie mit dir spielen können', color=color)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031589357588500/Plattformen.png?ex=661c0340&is=66098e40&hm=562fdcc3d363a13b07e2557e81a8a75b78be87b0443da2643f88f894ad687785&')
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        embed2 = discord.Embed(title="Geschlechtsauswahl", description='Du musst dies nicht auswählen\n'
                                                                        'Es ist Freiwillig!', color=color)
        embed2.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031651089354782/Geschlechtsauswahl.png?ex=661c034f&is=66098e4f&hm=5e4de732423c9e266495ae32a3856c78298cb59d6ddbd8a1ee280e87f3b9fc46&')
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        embed3 = discord.Embed(title="Sexualität", description='Freiwillige Angabe\n'
                                                                'Wenn du nicht willst musst du nicht', color=color)
        embed3.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031717015420938/sexualitat.png?ex=661c035e&is=66098e5e&hm=68903262ac86613f459ce8c4ab4840aaa1ceccd444cee0bfc3ef083b44c067af&')
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        embed4 = discord.Embed(title="Beziehungsstatus", description="Angaben sind Freiwillig", color=color)
        embed4.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031757754433657/beziehungsstatus.jpeg?ex=661c0368&is=66098e68&hm=1a31554d71e4c23e5e59b7cf064a1b7a12006166775150d4dd98613bcc6d646d&')
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        embed5 = discord.Embed(title="Alter", description="Gebe hier dein Alter an", color=color)
        embed5.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031776511623188/Alter.jpeg?ex=661c036c&is=66098e6c&hm=154fa81a46eccf2dabbab9432a023e573dec81b2434c05ff809d2332951f34f8&')
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        embed6 = discord.Embed(title="Farbenauswahl", description="Wähle unten im menü die rolle aus", color=color)
        embed6.set_image(url='https://cdn.discordapp.com/attachments/1073711672717488129/1224031796535099462/Farbenauswahl.jpeg?ex=661c0371&is=66098e71&hm=4c41fc30603056ac318fb2a45f2c8ea372b3b91a9eaa6de3c7e4d2a3130f138e&')
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        embed7 = (discord.Embed(title='Pingrollen', description='', colour=color))
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        embed8 = (discord.Embed(title='Extras', description='Unten findest du noch ein paar coole Extras\n'
                                                            f'klicke [hier]({link})'
                                                            '', colour=color))
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        channel_id = self.bot.get_channel(channel)
        await ctx.respond("Selfrols sind Aktiv", ephemeral=True)
        await asyncio.sleep(2)
        await ctx.channel.send(file=file, embed=embed, view=plattformen())
        await asyncio.sleep(2)
        await ctx.channel.send(file=file, embed=embed2, view=geschlechtsauswahl())
        await asyncio.sleep(2)
        await ctx.channel.send(file=file, embed=embed3, view=())
        await asyncio.sleep(2)
        await ctx.channel.send(file=file, embed=embed4, view=())
        await asyncio.sleep(2)
        await ctx.channel.send(file=file, embed=embed5, view=())
        await asyncio.sleep(2)
        await ctx.channel.send(file=file, embed=embed6, view=())
        await asyncio.sleep(2)
        await ctx.channel.send(file=file, embed=embed7, view=())
        await asyncio.sleep(2)
        await ctx.channel.send(file=file, embed=embed8, view=())

    @selfrols.error
    async def selfrols_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            em = discord.Embed(title='<:nope:1073700944941957291> | Error',
                description="Du bist nicht berechtigt, diesen command auszuführen\n\nMissing Permissions: Administrator",
                color=color)
            em.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await ctx.respond(file=file, embed=em)
            print(f'{ctx.author} hat versucht /selfrols auszuführen')


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
        discord.SelectOption(label='Handy', value='handy')]

    @discord.ui.select(
        placeholder="Wähle deine Plattform aus",
        min_values=1,
        max_values=5,
        options=options,
        custom_id="role_select")
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        role_id = 1014881098884456508
        role_id2 = 1014881100490883072
        role_id3 = 1014881101740781599
        role_id4 = 1014881103204597800
        role_id5 = 1014881104429326356
        role = interaction.guild.get_role(role_id)
        role2 = interaction.guild.get_role(role_id2)
        role3 = interaction.guild.get_role(role_id3)
        role4 = interaction.guild.get_role(role_id4)
        role5 = interaction.guild.get_role(role_id5)

        message = ""
        if selected_value == "pc":
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                message = f"Dir wurde die Rolle {role.mention} entfernt"
            else:
                await interaction.user.add_roles(role)
                message = f"Dir wurde {role.mention} hinzugefügt"
        elif selected_value == "playstation":
            if role2 in interaction.user.roles:
                await interaction.user.remove_roles(role2)
                message = f"Dir wurde die Rolle {role2.mention} entfernt"
            else:
                await interaction.user.add_roles(role2)
                message = f"Dir wurde {role2.mention} hinzugefügt"
        elif selected_value == "xbox":
            if role3 in interaction.user.roles:
                await interaction.user.remove_roles(role3)
                message = f"Dir wurde die Rolle {role3.mention} entfernt"
            else:
                await interaction.user.add_roles(role3)
                message = f"Dir wurde {role3.mention} hinzugefügt"
        elif selected_value == "switch":
            if role3 in interaction.user.roles:
                await interaction.user.remove_roles(role4)
                message = f"Dir wurde die Rolle {role4.mention} entfernt"
            else:
                await interaction.user.add_roles(role4)
                message = f"Dir wurde {role4.mention} hinzugefügt"
        elif selected_value == "handy":
            if role4 in interaction.user.roles:
                await interaction.user.remove_roles(role5)
                message = f"Dir wurde die Rolle {role4.mention} entfernt"
            else:
                await interaction.user.add_roles(role5)
                message = f"Dir wurde {role5.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


class geschlechtsauswahl(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Männlich", value="männlich"),
        discord.SelectOption(label="Weiblich", value="weiblich"),
        discord.SelectOption(label="Divers", value="divers")
    ]

    @discord.ui.select(
        placeholder="Wähle dein Geschlecht aus",
        min_values=1,
        max_values=3,
        options=options,
        custom_id="role_select"
    )
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        role_id = 1014881107461799966
        role_id2 = 1014881108195807403
        role_id3 = 1014881109596708955
        role = interaction.guild.get_role(role_id)
        role2 = interaction.guild.get_role(role_id2)
        role3 = interaction.guild.get_role(role_id3)

        message = ""

        if selected_value == "männlich":
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                message = f"Dir wurde die Rolle {role.mention} entfernt"
            else:
                await interaction.user.add_roles(role)
                message = f"Dir wurde {role.mention} hinzugefügt"
        elif selected_value == "weiblich":
            if role2 in interaction.user.roles:
                await interaction.user.remove_roles(role2)
                message = f"Dir wurde die Rolle {role2.mention} entfernt"
            else:
                await interaction.user.add_roles(role2)
                message = f"Dir wurde {role2.mention} hinzugefügt"
        elif selected_value == "divers":
            if role3 in interaction.user.roles:
                await interaction.user.remove_roles(role3)
                message = f"Dir wurde die Rolle {role3.mention} entfernt"
            else:
                await interaction.user.add_roles(role3)
                message = f"Dir wurde {role3.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


class sexualitat(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Männlich", value="männlich"),
        discord.SelectOption(label="Weiblich", value="weiblich"),
        discord.SelectOption(label="Divers", value="divers")
    ]

    @discord.ui.select(
        placeholder="Wähle dein Geschlecht aus",
        min_values=1,
        max_values=3,
        options=options,
        custom_id="role_select"
    )
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        role_id = 1014881107461799966
        role_id2 = 1014881108195807403
        role_id3 = 1014881109596708955
        role = interaction.guild.get_role(role_id)
        role2 = interaction.guild.get_role(role_id2)
        role3 = interaction.guild.get_role(role_id3)

        message = ""

        if selected_value == "männlich":
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                message = f"Dir wurde die Rolle {role.mention} entfernt"
            else:
                await interaction.user.add_roles(role)
                message = f"Dir wurde {role.mention} hinzugefügt"
        elif selected_value == "weiblich":
            if role2 in interaction.user.roles:
                await interaction.user.remove_roles(role2)
                message = f"Dir wurde die Rolle {role2.mention} entfernt"
            else:
                await interaction.user.add_roles(role2)
                message = f"Dir wurde {role2.mention} hinzugefügt"
        elif selected_value == "divers":
            if role3 in interaction.user.roles:
                await interaction.user.remove_roles(role3)
                message = f"Dir wurde die Rolle {role3.mention} entfernt"
            else:
                await interaction.user.add_roles(role3)
                message = f"Dir wurde {role3.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)


class beziehungsstatus(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Männlich", value="männlich"),
        discord.SelectOption(label="Weiblich", value="weiblich"),
        discord.SelectOption(label="Divers", value="divers")
    ]

    @discord.ui.select(
        placeholder="Wähle dein Geschlecht aus",
        min_values=1,
        max_values=3,
        options=options,
        custom_id="role_select"
    )
    async def callback(self, select, interaction: discord.Interaction):
        selected_value = select.values[0]
        role_id = 1014881107461799966
        role_id2 = 1014881108195807403
        role_id3 = 1014881109596708955
        role = interaction.guild.get_role(role_id)
        role2 = interaction.guild.get_role(role_id2)
        role3 = interaction.guild.get_role(role_id3)

        message = ""

        if selected_value == "männlich":
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                message = f"Dir wurde die Rolle {role.mention} entfernt"
            else:
                await interaction.user.add_roles(role)
                message = f"Dir wurde {role.mention} hinzugefügt"
        elif selected_value == "weiblich":
            if role2 in interaction.user.roles:
                await interaction.user.remove_roles(role2)
                message = f"Dir wurde die Rolle {role2.mention} entfernt"
            else:
                await interaction.user.add_roles(role2)
                message = f"Dir wurde {role2.mention} hinzugefügt"
        elif selected_value == "divers":
            if role3 in interaction.user.roles:
                await interaction.user.remove_roles(role3)
                message = f"Dir wurde die Rolle {role3.mention} entfernt"
            else:
                await interaction.user.add_roles(role3)
                message = f"Dir wurde {role3.mention} hinzugefügt"

        await interaction.response.send_message(message, ephemeral=True)