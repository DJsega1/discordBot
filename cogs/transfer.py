from nextcord.ext import commands
from nextcord import *


class Transfer(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @slash_command()
    async def transfer(self, interaction,
                       user: User = SlashOption(name="user", description="Пользователь", required=True),
                       amount: int = SlashOption(name="amount", description="Количество", required=True)):
        guild_info = self.db[str(interaction.guild_id)].find_one()
        if user == interaction.user:
            embed = Embed(title="Передача валюты",
                          description=f"{interaction.user.mention}, Вы не можете передавать **самому себе**")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        if amount < 50:
            embed = Embed(title="Передача валюты",
                          description=f"{interaction.user.mention}, количество не может быть менее **50**")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        if self.db[str(interaction.guild_id)].find_one({'id': interaction.user.id})["cash"] < amount:
            embed = Embed(title="Передача валюты",
                          description=f"{interaction.user.mention}, у Вас **недостаточно средств**")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            commission = guild_info['commission']
            value = int(amount * (1 - (commission / 100)))
            view = ui.View()
            view.add_item(ui.Button(label="Хотите переводить коины с меньшей комиссией?",
                                    style=ButtonStyle.link, url=guild_info["donate_url"]))
            embed = Embed(title="Передача валюты",
                          description=f"{interaction.user.mention}, Вы **передали** пользователю {user.mention} "
                                      f"**{value}**, включая коммиссию **{commission}%**")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            self.db[str(interaction.guild_id)].update_one({'id': interaction.user.id}, {"$inc": {"cash": -amount}})
            self.db[str(interaction.guild_id)].update_one({'id': user.id}, {"$inc": {"cash": value}})
            await interaction.response.send_message(embed=embed, view=view)
