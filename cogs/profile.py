from nextcord import *
from nextcord.ext import commands
from cogs.structures.profile import *


class Profile(commands.Cog):

    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @slash_command()
    async def profile(self, interaction):
        donate = self.db[str(interaction.guild_id)].find_one()["donate_url"]
        embed, view = await ProfileEmbed(self.bot, interaction.user, interaction, self.db, donate)
        await interaction.response.send_message(embed=embed, view=view)
