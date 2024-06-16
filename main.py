import discord
from discord.ext import commands
from Data.blacklist import db as blacklist_db
import aiosqlite
import pyfiglet
import asyncio
import os
import re

pyfiglet.print_figlet('GSV 2')

bot = commands.Bot(command_prefix='/', debug_guilds=None, intents=discord.Intents.all())
conn: aiosqlite.Connection = None

category_id = 1216835850961162310
guild_id = 1038267876622221332
team_id = '<@&1216835597017153677>'

if __name__ == '__main__':
    for filename in os.listdir('Team'):
        if filename.endswith('.py'):
            bot.load_extension(f'Team.{filename[:-3]}')
            print(f'Load Team_command: {filename[:-3]}')

if __name__ == '__main__':
    for filename in os.listdir('Community'):
        if filename.endswith('.py'):
            bot.load_extension(f'Community.{filename[:-3]}')
            print(f'Load command: {filename[:-3]}')

async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game('/help to see all commands'), status=discord.Status.dnd)
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game('Developed by gsv2.dev'), status=discord.Status.dnd)
        await asyncio.sleep(15)


@bot.event
async def on_ready():
    global conn
    bot.add_view(menu())
    bot.add_view(TutorialView())
    bot.add_view(Ticketweiterleitung())
    bot.add_view(Ticketmenu())
    print(f"Logged in as {bot.user}")


async def setup_database():
    global conn
    conn = await aiosqlite.connect("Data/tickets.db")
    await conn.execute("""CREATE TABLE IF NOT EXISTS tickets (
            channel_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            blocked INTEGER DEFAULT 0,
            priority INTEGER DEFAULT 0)""")


async def has_ticket(user_id):
    cursor = await conn.execute("SELECT * FROM tickets WHERE user_id = ?", (user_id,))
    row = await cursor.fetchone()
    return bool(row)


def remove_emojis(string):
    emoji_pattern = re.compile("["
                               u"\U0001F451-\U0001F4BB"
                               u"\U0001F334"
                               u"\U0001F4DA"
                               u"\U0001F4DD"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


#emoji = ("📝")
#unicode_codepoint = hex(ord(emoji))
#print(unicode_codepoint)

async def on_message(message: discord.Message):
    global next_team_member_index
    if message.author.bot:
        return
    if isinstance(message.channel, discord.DMChannel) and not await has_ticket(message.author.id):
        global next_team_member_index
        if await blacklist_db.get_blacklist(message.author.id) is not None:
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(title='<:nope:1073700944941957291> | Blocked', description='Du bist blockiert und kannst kein Ticket erstellen!', color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await message.channel.send(file=file, embed=embed)
            return
        if message.attachments or message.content:
            guild = bot.get_guild(guild_id)
            category = guild.get_channel(category_id)
            teamping = '<@&1216835597017153677>'  # hier teamping definieren !!!
            channel = await category.create_text_channel(f"ticket-{message.author.name}")

            await conn.execute("INSERT INTO tickets (user_id, channel_id) VALUES (?, ?)", (message.author.id, channel.id))
            await conn.commit()

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        embed = discord.Embed(title="WILLKOMMEN IM TICKET-SUPPORT!",
                              description="""
Ich habe deine Support-Anfrage erstellt und das Server-Team über dein Anliegen informiert.
                              """, color=discord.Color.green())
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        team_embed = discord.Embed(title="Neues Ticket!",
                                   description=f"Neues Ticket von: {message.author.mention}.",
                                   color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await message.channel.send(file=file, embed=embed)
        await channel.send(teamping)
        await channel.send(file=file, embed=team_embed, view=TutorialView())

    if isinstance(message.channel, discord.DMChannel) and await has_ticket(message.author.id):
        cursor = await conn.execute("SELECT channel_id FROM tickets WHERE user_id = ?", (message.author.id,))
        row = await cursor.fetchone()

        if row:
            channel_id = row[0]
            channel = bot.get_channel(channel_id)

            embed = discord.Embed(description=f"{message.content}", color=discord.Color.green())
            embed.set_author(name=message.author,
                             url=message.author.jump_url,
                             icon_url=message.author.avatar.url)

            if message.attachments:
                embed.set_image(url=message.attachments[0].url)

            await channel.send(embed=embed)
            await message.add_reaction("<:yes:1073716074140414013>")


    elif message.channel.category_id == category_id and not isinstance(message.channel, discord.DMChannel):
        cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (message.channel.id,))
        row = await cursor.fetchone()
        if row:
            user_id = row[0]
            user = bot.get_user(user_id)
            if user is None:
                user = await bot.fetch_user(user_id)
            member = message.guild.get_member(message.author.id)
            ignore_roles = []

            highest_role = next((role for role in sorted(member.roles, key=lambda role: role.position, reverse=True) if
                                 role.name not in ignore_roles), None)
            if highest_role is None:
                print("All roles are in the ignore_roles list.")
            else:
                file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                color = 0x2596be
                embedt = discord.Embed(description=f"{message.content}\n", color=color)
                embedt.set_author(name=f"{message.author} | {remove_emojis(highest_role.name)}",
                                  url=message.author.jump_url,
                                  icon_url=message.author.avatar.url)
                embedt.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
                if message.attachments:
                    embedt.set_image(url=message.attachments[0].url)
                await user.send(file=file, embed=embedt)
                await message.add_reaction("<:yes:1073716074140414013>")
        await bot.process_commands(message)


class Ticketweiterleitung(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(
            label="Admin Weiterleitung",
            description="Leite das Ticket an einen Admin weiter",
            value="admin"),
        discord.SelectOption(
            label="Developer Weiterleitung",
            description="Leite das Ticket an einen Developer weiter",
            value="developer"),
        discord.SelectOption(
            label="Moderator Weiterleitung",
            description="Leite das Ticket an einen Moderator weiter",
            value="moderator"),
        discord.SelectOption(
            label="management Weiterleitung",
            description="Leite das Ticket an das Management weiter",
            value="management")]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Was möchtest du tun?",
        options=options,
        custom_id="select")
    async def select_callback(self, select, interaction):
        if select.values[0] == "admin":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            teamping = '<@&1216835574510522438>'  # hier teamping definieren !!!
            if user is None:
                user = await bot.fetch_user(user_id)
                file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                color = 0x2596be
            embed = discord.Embed(
                title="Ticket wurde an Admin weitergeleitet!",
                description=f"Ich habe dein Ticket an einen Admin weitergeleitet. Bitte habe etwas Geduld.",
                color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")

            await user.send(file=file, embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an einen Admin weitergeleitet!")


        if select.values[0] == "moderator":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            teamping = '<@&1216835586229534830>'
            if user is None:
                user = await bot.fetch_user(user_id)
                file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                color = 0x2596be
            embed = discord.Embed(
                title="Ticket wurde an Moderator weitergeleitet!",
                description=f"Ich habe dein Ticket an einen Moderator weitergeleitet. Bitte habe etwas Geduld.",
                color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await user.send(file=file, embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an einen Moderator weitergeleitet!")

        if select.values[0] == "developer":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            teamping = '<@&1216835580982202460>'
            if user is None:
                user = await bot.fetch_user(user_id)
                file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                color = 0x2596be
            embed = discord.Embed(
                title="Ticket wurde an Developer weitergeleitet!",
                description=f"Ich habe dein Ticket an einen Developer weitergeleitet. Bitte habe etwas Geduld.",
                color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await user.send(file=file, embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an einen Developer weitergeleitet!")

        if select.values[0] == "management":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            teamping = '<@&1216835578373607444>'
            if user is None:
                user = await bot.fetch_user(user_id)
                file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                color = 0x2596be
            embed = discord.Embed(
                title="Ticket wurde an das Management weitergeleitet!",
                description=f"Ich habe dein Ticket an das Management weitergeleitet. Bitte habe etwas Geduld.",
                color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await user.send(file=file, embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an das Management weitergeleitet!")



class menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(
            label="Ticket Regeln",
            description="Bitte lesen Sie die Ticket Regeln bevor Sie ein Ticket erstellen.",
            value="sonstiges")]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Schau dir Nützliche Informationen an!",
        options=options,
        custom_id="select",
    )
    async def select_callback(self, select, interaction):
        auswahl = select.values[0]

        if auswahl == "sonstiges":
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
                title="Ticket Regeln",
                description="1. Bitte benutze das Ticket System nur für wichtige Anliegen.\n"
                            "2. Bitte sei respektvoll gegenüber dem Team und anderen Usern.\n"
                            "3. Bitte warte geduldig auf eine Antwort.\n"
                            "4. Bitte schreibe dein Anliegen möglichst genau.\n"
                            "5. Bitte beachte, dass das Team auch mal offline sein kann.\n",
                color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await interaction.user.send(file=file, embed=embed)




class Ticketmenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(
            label="Ticket Schließen",
            description="Schließe das Ticket",
            value="close"),
        discord.SelectOption(
            label="Claim",
            description="Beanspruche das Ticket",
            value="claim"),
        discord.SelectOption(
            label="User Blockieren",
            description="Blockiere den User",
            value="block")]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Was möchtest du tun?",
        options=options,
        custom_id="select")
    async def select_callback(self, select, interaction):

        if select.values[0] == "block":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            if user is None:
                user = await bot.fetch_user(user_id)
            await blacklist_db.add_blacklist(user_id)
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            color = 0x2596be
            embed = discord.Embed(
            title="Du wurdest ausgeschlossen!",
            description=f"Du wurdest von support ausgeschlossen!\n"
                        f"du kannst dich [hier](https://discord.gg/jb2bBFJDsC) entbannen lassen",
                        color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await user.send(file=file, embed=embed)
            await interaction.response.send_message("Der User wurde blockiert!")
            await conn.execute("DELETE FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            await conn.commit()
            await asyncio.sleep(5)
            await interaction.message.channel.delete()

        if select.values[0] == "close":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            if user_id_tuple is None:
                await interaction.response.send_message("No matching ticket found.")
                return
            user_id = user_id_tuple[0]

            await conn.execute("DELETE FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            await conn.commit()

            user = bot.get_user(user_id)
            if user is None:
                user = await bot.fetch_user(user_id)

            await interaction.response.send_message("Ticket wird geschlossen!")
            file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
            embed = discord.Embed(
                title="Ticket geschlossen!",
                description=f"Das Ticket wurde von {interaction.user.mention} geschlossen.",
                color=discord.Color.red())
            embed.set_author(name=f"{interaction.user}", icon_url=interaction.user.avatar.url)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await user.send(file=file, embed=embed)
            await interaction.message.channel.delete()

        if select.values[0] == "claim":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            if user is None:
                user = await bot.fetch_user(user_id)
                file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
                color = 0x2596be
            embed = discord.Embed(
                title="Ticket wurde beansprucht!",
                description=f"Guten Tag ich bin {interaction.user.mention} und ich werde dir jetzt weiterhelfen!\n"
                            f"Wie kann ich dir helfen?",
                color=color)
            embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
            await user.send(file=file, embed=embed)
            await interaction.response.send_message("Das Ticket wurde beansprucht!")


class TutorialView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Weiterleitung", style=discord.ButtonStyle.success, emoji="🍪", custom_id="keks", row=2)
    async def button_callback1(self, button, interaction):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        color = 0x2596be
        embed = discord.Embed(
            title="Weiterleitung",
            description="Bitte wähle aus an wen du das Ticket weiterleiten möchtest!\n"
                        "Sollte kein passender Teamler online sein, schreibe bitte in das Ticket das keiner da ist!",
            color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await interaction.response.send_message(file=file, embed=embed, view=Ticketweiterleitung(), ephemeral=True)


    @discord.ui.button(label="Ticket Menü", style=discord.ButtonStyle.success, emoji="🍕", custom_id="pizza", row=1)
    async def button_callback2(self, button, interaction):
        file = discord.File("img/GSv_Logo_ai.png", filename='GSv_Logo.png')
        button.disabled = False
        color = 0x2596be
        embed = discord.Embed(
            title="Ticket Menü",
            description="Bitte wähle aus was du tun möchtest!\n"
                        "Ticket erst schließen wenn das Problem gelöst wurde!\n\n"
                        "Ticket beanspruchen wenn du das Ticket bearbeiten möchtest!\n"
                        "Sollte das Ticket bereits beansprucht sein, schreibt nur der zugeteilte Supporter in das Ticket!",
            color=color)
        embed.set_footer(text="Powered by gsv2.dev ⚡", icon_url="attachment://GSv_Logo.png")
        await interaction.response.send_message(file=file, embed=embed, view=Ticketmenu(), ephemeral=True)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

bot.run(TOKEN)
