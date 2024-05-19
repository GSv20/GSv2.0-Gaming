import discord
import random
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        button1 = discord.ui.Button(label="Verify", url="https://discord.com/channels/913082943495344179/1176254800493555763")
        button2 = discord.ui.Button(label="Main Projekt", url="https://discord.gg/ufEjGrbYWw")
        view = discord.ui.View()
        view.add_item(button1)
        view.add_item(button2)

        message = f'{member.mention} Willkommen von uns allen <3'
        embed = discord.Embed(
            title="Willkommen",
            description=f"Hey {member.mention}, Willkommen auf dem Server!\n",
            color=discord.Color.dark_gold()
        )
        embed.add_field(name="Hilfe", value="Eine Einführung findest du hier: <#1073700811143647232>")

        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1073711672717488129/1216626262207107103/GSV_verify.gif?ex=66011280&is=65ee9d80&hm=39fe6e5e75340beb22147915f7014b8cbfd7a33964227d623f27bcd603818872&")
        embed.set_footer(text="Powered by GSV ⚡",
                         icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")

        role_ids = [1216629193090007071, 1014881097064132649, 1014881106018979870, 1014881110695616673,
                    1017133211215745135, 1205647946503290930, 1072233630019113060, 1014881114491461632,
                    1014881119990190122, 1014881120921321543, 1052621721296969828]  # Liste der Rollen-IDs

        for role_id in role_ids:
            role = member.guild.get_role(role_id)
            if role:
                await member.add_roles(role)
            else:
                print(f"Rolle mit ID {role_id} nicht gefunden.")

        channel = await self.bot.fetch_channel(1073701634863009933)  # Channel ID vom Willkommenschat
        await channel.send(embed=embed, view=view)
        print(f"{member} joined the Server")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        user = member.name
        guild_name = member.guild.name
        channel = self.bot.get_channel(1217109251395158127)  # Ersetze YOUR_CHANNEL_ID durch die ID des gewünschten Kanals

        await channel.send(f"{user} hat den Server {guild_name} leider verlassen... Ihr/Sein Pech.")

        try:
            dm_channel = await member.create_dm()
            await dm_channel.send(
                'Hey hey\nmich hast du save schon gesehen, Entschuldige das ich dich einfach so anschreibe\ndu hast unseren Gaming Server verlassen, unser Team interessiert sich persönlich dafür\nund wäre dir mehr als Dankbar wenn du hier ein Feedback hinterlässt\n<3\nhttps://discord.gg/xexvmgp6qu\n\nAnsonnsten nochmal SRY für die Störung und danke fürs lesen')
            print(f'DM erfolgreich an {user} gesendet')
        except discord.Forbidden:
            print(f'Konnte keine Direktnachricht an {user} senden.')

def setup(bot):
    bot.add_cog(Welcome(bot))