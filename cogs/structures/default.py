from nextcord import *
from nextcord.ext import commands


# --------------
# Default Embeds
# --------------


async def NotYourButtonEmbed(interaction):
    view = ui.View()
    embed = Embed(title=interaction.user,
                  description=f"{interaction.user.mention}, "
                              f"кнопка **не предназначена** для Вас")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    return embed, view


async def NotEnoughMoneyEmbed(interaction, title):
    view = ui.View()
    embed = Embed(title=title, description=f"{interaction.user.mention}, у Вас **недостаточно средств**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    return embed, view
