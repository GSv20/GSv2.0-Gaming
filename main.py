import discord
from discord.ext import commands
from Data.blacklist import db as blacklist_db
import aiosqlite
import pyfiglet
import os
import re

pyfiglet.print_figlet('GSV 2')

TOKEN = ''
bot = commands.Bot(command_prefix='!', debug_guilds=None, intents=discord.Intents.all())
conn: aiosqlite.Connection = None

category_id = 1216835850961162310
guild_id = 1038267876622221332
team_id = '<@&1216835597017153677>'

if __name__ == '__main__':
    for filename in os.listdir('commands'):
        if filename.endswith('.py'):
            bot.load_extension(f'commands.{filename[:-3]}')
            print(f'Load command: {filename[:-3]}')


@bot.event
async def on_ready():
    global conn
    bot.add_view(menu())
    bot.add_view(TutorialView())
    bot.add_view(Ticketweiterleitung())
    bot.add_view(Ticketmenu())
    await bot.change_presence(activity=discord.Game(name='GSv Gaming 💕'), status=discord.Status.dnd)
    print(f"Logged in as {bot.user}")


async def setup_database():
    global conn
    conn = await aiosqlite.connect("Data/tickets.db")
    await conn.execute(
        """CREATE TABLE IF NOT EXISTS tickets (
            channel_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                blocked INTEGER DEFAULT 0
        )"""
    )


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


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel) and not await has_ticket(message.author.id):
        if await blacklist_db.get_blacklist(message.author.id) is not None:
            embed = discord.Embed(title='<:no:1239566473165537301> Error', description='Du wurdest Blockiert und kannst kein Ticket erstellen.', color=discord.Color.dark_gold())
            embed.set_footer(text='Powered by GSv ⚡', icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
            await message.channel.send(embed=embed)
            return
        guild = bot.get_guild(guild_id)
        category = guild.get_channel(category_id)
        teamping = '<@&1216835597017153677>'

        channel = await category.create_text_channel(f"ticket-{message.author.name}")

        await conn.execute("INSERT INTO tickets (user_id, channel_id) VALUES (?, ?)", (message.author.id, channel.id))
        await conn.commit()
        embed = discord.Embed(title="WILLKOMMEN IM TICKET-SUPPORT!",
                              description="""
Ich habe deine Support-Anfrage erstellt und das Server-Team über dein Anliegen informiert.
                              """, color=discord.Color.green())
        embed.set_footer(text=f"Powered by GSv ⚡",
                         icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")

        team_embed = discord.Embed(title="Neues Ticket!",
                                   description=f"Neues Ticket von: {message.author.mention}.",
                                   color=discord.Color.green())
        team_embed.set_footer(text="Powered by GSv ⚡",
                              icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
        await message.channel.send(embed=embed)
        await channel.send(teamping)
        await channel.send(embed=team_embed, view=TutorialView())

    elif isinstance(message.channel, discord.DMChannel) and await has_ticket(message.author.id):
        cursor = await conn.execute("SELECT channel_id FROM tickets WHERE user_id = ?", (message.author.id,))
        row = await cursor.fetchone()

        if row:
            channel_id = row[0]
            channel = bot.get_channel(channel_id)

            embed = discord.Embed(description=f"{message.content}", color=discord.Color.green())
            embed.set_author(name=message.author,
                             url=message.author.jump_url,
                             icon_url=message.author.avatar.url
                             )
            embed.set_footer(text="Powered by GSv ⚡",
                             icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")

            await channel.send(embed=embed)
            await message.add_reaction("✅")

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
                embedt = discord.Embed(description=f"{message.content}\n", color=discord.Color.dark_gold())
                embedt.set_author(name=f"{message.author} | {remove_emojis(highest_role.name)}",
                                 url=message.author.jump_url,
                                 icon_url=message.author.avatar.url
                                 )
                embedt.set_footer(text=f"Powered by GSv ⚡",
                                 icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")

                await user.send(embed=embedt)
                await message.add_reaction("✅")

        await bot.process_commands(message)


class Ticketweiterleitung(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(
            label="Admin Weiterleitung",
            description="Leite das Ticket an einen Admin weiter",
            value="admin"
        ),
        discord.SelectOption(
            label="Developer Weiterleitung",
            description="Leite das Ticket an einen Developer weiter",
            value="developer"
        ),
        discord.SelectOption(
            label="Moderator Weiterleitung",
            description="Leite das Ticket an einen Moderator weiter",
            value="moderator"
        ),
        discord.SelectOption(
            label="management Weiterleitung",
            description="Leite das Ticket an das Management weiter",
            value="management"
        ),

    ]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Was möchtest du tun?",
        options=options,
        custom_id="select",
    )
    async def select_callback(self, select, interaction):
        if select.values[0] == "admin":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            teamping = '<@&1216835597017153677>'
            if user is None:
                user = await bot.fetch_user(user_id)
            embed = discord.Embed(
                title="Ticket wurde an Admin weitergeleitet!",
                description=f"Ich habe dein Ticket an einen Admin weitergeleitet. Bitte habe etwas Geduld.",)
            embed.set_footer(text='Powered by GSv ⚡', icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')

            await user.send(embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an einen Admin weitergeleitet!")

        if select.values[0] == "moderator":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            teamping = '<@&1216835597017153677>'
            if user is None:
                user = await bot.fetch_user(user_id)
            embed = discord.Embed(
                title="Ticket wurde an Moderator weitergeleitet!",
                description=f"Ich habe dein Ticket an einen Moderator weitergeleitet. Bitte habe etwas Geduld.",)
            embed.set_footer(text='Powered by GSv ⚡',
                             icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
            await user.send(embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an einen Moderator weitergeleitet!")

        if select.values[0] == "developer":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            teamping = '<@&1216835597017153677>'
            if user is None:
                user = await bot.fetch_user(user_id)
            embed = discord.Embed(
                title="Ticket wurde an Developer weitergeleitet!",
                description=f"Ich habe dein Ticket an einen Developer weitergeleitet. Bitte habe etwas Geduld.")
            embed.set_footer(text='Powered by GSv ⚡',
                             icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
            await user.send(embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an einen Developer weitergeleitet!")

        if select.values[0] == "management":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            teamping = '<@&1216835597017153677>'
            if user is None:
                user = await bot.fetch_user(user_id)
            embed = discord.Embed(
                title="Ticket wurde an das Management weitergeleitet!",
                description=f"Ich habe dein Ticket an das Management weitergeleitet. Bitte habe etwas Geduld.",)
            embed.set_footer(text='Powered by GSv ⚡',
                             icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
            await user.send(embed=embed)
            await interaction.message.channel.send(teamping)
            await interaction.response.send_message("Das Ticket wurde an das Management weitergeleitet!")


class menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(
            label="Ticket Regeln",
            description="Bitte lesen Sie die Ticket Regeln bevor Sie ein Ticket erstellen.",
            value="sonstiges"
        )

    ]

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
            embed = discord.Embed(
                title="Ticket Regeln",
                description="1. Bitte benutze das Ticket System nur für wichtige Anliegen.\n"
                            "2. Bitte sei respektvoll gegenüber dem Team und anderen Usern.\n"
                            "3. Bitte warte geduldig auf eine Antwort.\n"
                            "4. Bitte schreibe dein Anliegen möglichst genau.\n"
                            "5. Bitte beachte, dass das Team auch mal offline sein kann.\n"
                            "6. Bitte beachte, dass das Team auch mal offline sein kann.\n"
                            "7. Bitte beachte, dass das Team auch mal offline sein kann.\n",
                color=discord.Color.dark_gold())
            embed.set_footer(text='Powered by GSv ⚡',
                             icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
            await interaction.user.send(embed=embed)


class Ticketmenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(
            label="Ticket Schließen",
            description="Schließe das Ticket",
            value="close"
        ),
        discord.SelectOption(
            label="Claim",
            description="Beanspruche das Ticket",
            value="claim"
        )

    ]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Was möchtest du tun?",
        options=options,
        custom_id="select",
    )
    async def select_callback(self, select, interaction):
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
            embed = discord.Embed(
                title="Ticket geschlossen!",
                description=f"Das Ticket wurde von {interaction.user.mention} geschlossen.",
                color=discord.Color.red())
            embed.set_footer(text='Powered by GSv ⚡',
                             icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
            embed.set_author(name=f"{interaction.user}", icon_url=interaction.user.avatar.url)
            await user.send(embed=embed)
            await interaction.message.channel.delete()

        if select.values[0] == "claim":
            cursor = await conn.execute("SELECT user_id FROM tickets WHERE channel_id = ?", (interaction.channel.id,))
            user_id_tuple = await cursor.fetchone()
            user_id = user_id_tuple[0]
            user = bot.get_user(user_id)
            if user is None:
                user = await bot.fetch_user(user_id)
            embed = discord.Embed(
                title="Ticket wurde beansprucht!",
                description=f"Guten Tag ich bin {interaction.user.mention} und ich werde dir jetzt weiterhelfen!\n"
                            f"Wie kann ich dir helfen?",)
            embed.set_footer(text='Powered by GSv ⚡',
                             icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
            await user.send(embed=embed)
            await interaction.response.send_message("Das Ticket wurde beansprucht!, sende keine weiteren Nachrichten mehr bevor der User nicht Antwortet")


class TutorialView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Weiterleitung", style=discord.ButtonStyle.success, emoji="🍪", custom_id="keks", row=2)
    async def button_callback1(self, button, interaction):
        embed = discord.Embed(
            title="Weiterleitung",
            description="Bitte wähle aus an wen du das Ticket weiterleiten möchtest!\n"
                        "Sollte kein passender Teamler online sein, schreibe bitte in das Ticket das keiner da ist!",
            color=discord.Color.dark_gold())
        embed.set_footer(text='Powered by GSv ⚡',
                         icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
        await interaction.response.send_message(embed=embed, view=Ticketweiterleitung(), ephemeral=True)

    @discord.ui.button(label="Ticket Menü", style=discord.ButtonStyle.success, emoji="🍕", custom_id="pizza", row=1)
    async def button_callback2(self, button, interaction):
        button.disabled = False
        embed = discord.Embed(
            title="Ticket Menü",
            description="Bitte wähle aus was du tun möchtest!\n"
                        "Ticket erst schließen wenn das Problem gelöst wurde!\n\n"
                        "Ticket beanspruchen wenn du das Ticket bearbeiten möchtest!\n"
                        "Sollte das Ticket bereits beansprucht sein, schreibt nur der zugeteilte Supporter in das Ticket!",
            color=discord.Color.dark_gold())
        embed.set_footer(text='Powered by GSv ⚡',
                         icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
        await interaction.response.send_message(embed=embed, view=Ticketmenu(), ephemeral=True)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

@bot.slash_command(description='📝┃Sende die Liste der Server-Emojis')
async def emojilist(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Emojis',
        description='',
        color=discord.Color.green())
    embed.set_footer(text="Powered by GSV ⚡",
                     icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")

    if len(interaction.guild.emojis) > 50:
        embed_2 = discord.Embed(
            title='❌ | Error | ❌',
            description='Anscheind gibt es zu viele Emojis auf diesem Server :( \nIch bin dadurch leider etwas eingeschränkt',
            color=discord.Color.dark_red())
        embed_2.set_footer(text="Powered by GSV ⚡",
                         icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")

        await interaction.response.send_message(embed=embed_2, delete_after=120)
    else:
        for emoji in interaction.guild.emojis:
            embed.description += f'{emoji} - `{emoji}`\n'

        await interaction.response.send_message(embed=embed, delete_after=120)

@bot.slash_command(description='.')
@commands.has_permissions(administrator=True)
async def coming_soon(ctx):
    message = 'comming soon <a:Loading:1073700976000782396>'
    await ctx.respond(message)

@coming_soon.error
async def coming_soon_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title=' ❌| Error | ❌',
                           description="Leider ist dies eine Admin Option.\nWenn du Hilfe brauchst, melde dich gerne im Support:\n<#1073700885886152837>",
                           color=discord.Color.red())
        em.set_footer(text="Powered by GSV ⚡",
                      icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
        await ctx.send(embed=em, delete_after=15)
        print(f'{ctx.author.name} hat versucht /coming_soon auszuführen')

@bot.slash_command(description='.')
@commands.has_role(1044557317947019264)
@commands.cooldown(1, 3600)
async def deathchat(ctx):
    message = '<@&1014881120921321543>'
    embed = discord.Embed(title='💀| Deathchatping |🔔', description=f'{ctx.author.name} hat den ping ausgeführt\n'
                                                                   f'\n'
                                                                   f'Dieser ping ist abstellbar in den <#1073993336890871848>\n'
                                                                   f'PS wir nehmen uns das recht raus sollte dieser ping nix bringen, andere zu pingen\n'
                                                                   f'Hate etc wird schwerstens bestraft, (Keine Angst, wir sind Hard aber Fair)', colour=discord.Colour.dark_gold())
    embed.set_footer(text='Powered by GSV ⚡',
                     icon_url='https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&')
    await ctx.send(message)
    await ctx.respond(embed=embed)

@deathchat.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRole):
        em = discord.Embed(title=' ❌| Error | ❌',
                           description="Dies ist eine Teamfunktion, bewerbe dich gerne fürs Team unter: <#1073702332082172084>",
                           color=discord.Color.red())
        em.set_footer(text="Powered by GSV ⚡",
                      icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
        await ctx.send(embed=em, delete_after=15)
        print(f'{ctx.author.name} hat versucht /deathchat auszuführen')

@deathchat.error
async def error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=' ❌| Error | ❌',
                           description=f"Du musst noch {error.retry_after:.2f} warten bis du den Command neuausführen kannst",
                           color=discord.Color.red())
        em.set_footer(text="Powered by GSV ⚡",
                      icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
        await ctx.send(embed=em, delete_after=15)

bot.run(TOKEN)
