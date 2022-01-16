from nextcord import *
from nextcord.ext import commands
from cogs.structures.default import *
from cogs.structures.personal_roles import *


class Roles(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @slash_command()
    async def role(self, interaction):
        roles = self.db[str(interaction.guild_id)].find_one({'id': interaction.user.id})["own_roles"]
        embed, view = ChooseProfileEmbed(self.bot, interaction, roles, self.db, interaction.author)
        await interaction.response.send_message(embed=embed, view=view)

    @slash_command()
    async def create(self, interaction):
        pass

    @create.subcommand()
    async def role(self, interaction, name: str = SlashOption(name="name", description="название роли", required=True),
                   color: str = SlashOption(name="hex-color", description="hex-цвет роли", required=True)):
        if self.db[str(interaction.guild_id)].find_one({'id': interaction.user.id})["cash"] < 1000:
            embed, view = await NotEnoughMoneyEmbed(interaction, "Создание роли")
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        else:
            new = await interaction.guild.create_role(name=name,
                                                      colour=await commands.ColourConverter().convert(interaction,
                                                                                                      color),
                                                      position=0)
            self.db[str(interaction.guild_id)].update_one({'id': interaction.user.id}, {"$inc": {"cash": -1000}})
            await interaction.user.add_roles(new, atomic=True)
            await interaction.response.send_message(embed=Embed(title="Создание роли",
                                                                description=f"{interaction.user.mention},"
                                                                            f" роль **создана**"),
                                                    view=None, ephemeral=True)
