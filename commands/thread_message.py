import discord
from discord.ext import commands
from discord.ui import View, Button


class ForumCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1170464267808542853
        self.gsv = discord.Color.dark_gold()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(CustomView(timeout=None))

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id == self.channel_id:
            await self.post_custom_message(thread)

    async def post_custom_message(self, thread):
        embed = discord.Embed(title='Bug Report', description='Das Team bedankt sich für den Report.\nWir setzen uns unverzüglich an die Arbeit\n\nDanke das du die GSv Community so fleißig unterstützt.', colour=self.gsv)
        view = CustomView(timeout=None)
        await thread.send(embed=embed, view=view)


class CustomView(View):
    def __init__(self, timeout=None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label='Close', style=discord.ButtonStyle.red, custom_id='button_close')
    async def action_button_pressed(self, button: Button, interaction: discord.Interaction):
        embed_4 = discord.Embed(title='', description='', color=discord.Color.red())
        embed_4.set_footer(text="Powered by GSV ⚡", icon_url="https://cdn.discordapp.com/attachments/1073711669731151904/1218393384897740830/GSV_Logo_new_.png?ex=66078043&is=65f50b43&hm=522d323764bdb16890d3fb1f6d748de45d0f1fa51d3194485ef5804a25b25f25&")
        lock: bool = False
        if interaction.channel.permissions_for(interaction.user).manage_threads:
            if lock:
                embed_4.title = '📛| Gesperrt |📛'
                embed_4.description = "Dieser Thread wurde von einem Teammitglied gesperrt!"
            else:
                embed_4.title = '⛔| Archiviert |⛔'
                embed_4.description = "Dieser Thread wurde von einem Teammitglied archiviert!"
            await interaction.response.send_message(embed=embed_4)
            await interaction.channel.archive(locked=lock)
        elif interaction.user.id == interaction.channel.owner_id:
            embed_4.title = '⭕| Archiviert |⭕'
            embed_4.description = "Dieser Thread wurde von dem Author archiviert!"
            await interaction.response.send_message(embed=embed_4)
            await interaction.channel.archive()
        else:
            embed_4.title = '❌| Error |❌'
            embed_4.description = "Dieser Button kann nur von dem Thread Inhaber oder einem Teammiglied genutzt werden!"
            await interaction.response.send_message(embed=embed_4, ephemeral=True)


def setup(bot):
    bot.add_cog(ForumCog(bot))
