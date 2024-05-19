from typing import Optional

import discord
from discord.ext import commands, tasks



def get_channel_containing_name(guild: discord.Guild, target: str) -> Optional[discord.abc.GuildChannel]:
    for channel in guild.channels:
        if target in channel.name:
            return channel


class MemberCount(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.member_count.start(),
        self.bot = bot
        self.target_name = '👤| 𝑀𝑖𝑡𝑔𝑙𝑖𝑒𝑑𝑒𝑟:'
        self.target_guild = None

    @tasks.loop(minutes=10)
    async def member_count(self) -> None:
        if self.target_guild is not None:
            guild = self.bot.get_guild(self.target_guild)
            if guild is not None:
                await self._update_member_count(guild)
                return

        for guild in self.bot.guilds:
            await self._update_member_count(guild)

    async def _update_member_count(self, guild: discord.Guild) -> Optional[discord.VoiceChannel]:
        channel = get_channel_containing_name(guild, self.target_name)
        if not isinstance(channel, discord.VoiceChannel):
            channel = await self._create_target_channel(guild)
            return

        return await channel.edit(name=self._make_member_count_name(guild))

    def _make_member_count_name(self, guild: discord.Guild):
        return f'{self.target_name}: {guild.member_count}'

    async def _create_target_channel(self, guild: discord.Guild) -> discord.VoiceChannel:
        return await guild.create_voice_channel(
            self._make_member_count_name(guild),
            position=0,
            overwrites={
                guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False),
            }
        )

    @member_count.before_loop
    async def _before_member_count(self):
        await self.bot.wait_until_ready()


def setup(bot: discord.Bot):
    bot.add_cog(MemberCount(bot))