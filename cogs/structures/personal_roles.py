from nextcord import *
from nextcord.ext import commands
from cogs.structures.default import *


# ---------------------
# Personal Roles Embeds
# ---------------------
async def ChooseProfileEmbed(bot, interaction, roles, db, author):
    if roles:
        desc = f"{interaction.user.mention}, в **списке** только роли, где Вы **владелец**"
    else:
        desc = f"{interaction.user.mention}, Вы не владеете **личными ролями**"
    embed = Embed(title="Выберите роль для управления",
                  description=desc)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    for i in roles:
        view.add_item(ChooseButtons(bot, interaction.guild.get_role(i), db, author))
    return embed, view


async def ProfileManageEmbed(bot, interaction, roles, db, author):
    pass


async def ConfirmGiveRole(interaction, user, role):
    embed = Embed(title="Выдать пользователю личную роль",
                  description=f"{user.mention}, {interaction.user.mention} хочет выдать вам роль {role}")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    view.add_item(ui.Button(interaction.guild.get_role(i)))
    return embed, view


# ----------------------
# Personal Roles Buttons
# ----------------------
class ConfirmButton(ui.Button):
    def __init__(self, bot, role, db, author):
        super().__init__(label="Да", style=ButtonStyle.green)
        self.role = role
        self.db = db
        self.author = author

    async def callback(self, interaction):
        await interaction.user.add_roles(self.role)
        await interaction.message.edit(embed=ProfileManageEmbed(self.bot, self.interaction,
                                                                self.roles, self.db, self.author),
                                       view=ManageView(self.bot, self.role, self.db, self.author))


class RejectButton(ui.Button):
    def __init__(self, bot, role, db, author):
        super().__init__(label="Нет", style=ButtonStyle.red)
        self.role = role
        self.db = db
        self.author = author

    async def callback(self, interaction):
        await interaction.message.edit(embed=ProfileManageEmbed(self.bot, self.interaction,
                                                                self.roles, self.db, self.author),
                                       view=ManageView(self.bot, self.role, self.db, self.author))


class ChooseButtons(ui.Button):
    def __init__(self, bot, role, db, author):
        super().__init__(label=role.name, style=ButtonStyle.blurple, custom_id=role.id)
        self.role = role
        self.db = db
        self.author = author

    async def callback(self, interaction):
        embed, view = ProfileManageEmbed()
        await interaction.message.edit(embed=embed, view=view)


# --------------------
# Personal Roles Views
# --------------------
class ManageView(ui.View):
    def __init__(self, bot, role, db, author):
        super().__init__()
        self.role = role
        self.db = db
        self.author = author

    @ui.button(label="Выдать роль")
    async def give(self, interaction):
        embed, view = await ConfirmGiveRole(interaction, self.user, self.role)
        await interaction.response.send_message(embed=embed, view=view)
