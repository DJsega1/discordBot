from nextcord import *
from nextcord.ext import commands
from cogs.structures.default import *


# --------------
# Profile Embeds
# ---------------

async def ProfileEmbed(bot, author, interaction, db, donate):
    info = db[str(interaction.guild_id)].find_one({"id": interaction.user.id})
    view = ui.View()
    embed = Embed(title=f"Профиль - {interaction.user}",
                  color=await commands.ColourConverter().convert(interaction, "#2f3136"))
    embed.add_field(name="> Статус", value=f"```{info['status']}```", inline=False)
    embed.add_field(name="> Баланс", value=f"```{info['cash']}```")
    online = f"{info['online_all'] // 3600} ч, {info['online_all'] % 3600 // 60} м, {info['online_all'] % 60} с"
    embed.add_field(name="> Голосовой онлайн:", value=f"```{online}```")
    embed.add_field(name="> Партнёр", value=f"```{info['marry']} ```")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view.add_item(item=OpenProfileManageButton(bot, author, db, donate))
    view.add_item(item=DonateButton(donate))
    if info['inst'] != "Не установлен":
        view.add_item(item=ui.Button(label="Instagram",
                                     style=ButtonStyle.link, url=f"https://{info['inst']}", row=1))
    if info['vk'] != "Не установлен":
        view.add_item(item=ui.Button(label="VK",
                                     style=ButtonStyle.link, url=f"https://{info['vk']}", row=1))
    if info['tg'] != "Не установлен":
        view.add_item(item=ui.Button(label="Telegram",
                                     style=ButtonStyle.link, url=f"https://{info['tg']}", row=1))
    return embed, view


async def ProfileManageEmbed(bot, author, interaction, db, donate):
    info = db[str(interaction.guild_id)].find_one({"id": interaction.user.id})
    view = ui.View()
    embed = Embed(title=f"Управление профилем - {interaction.user}")
    embed.add_field(name="Статус", value=f'```{info["status"]}```', inline=False)
    embed.add_field(name="Instagram", value=f'```{info["inst"]}```')
    embed.add_field(name="ВКонтакте", value=f'```{info["vk"]}```')
    embed.add_field(name="Telegram", value=f'```{info["tg"]}```')
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view.add_item(item=CloseProfileManageButton(bot, author, db, donate))
    view.add_item(item=DonateButton(donate))
    if info['status'] == "Не установлен":
        view.add_item(item=SetStatusButton(bot, author, db, donate))
    else:
        view.add_item(item=RemoveStatusButton(bot, author, db, donate))
    if info['inst'] == "Не установлен":
        view.add_item(item=SetInstButton(bot, author, db, donate))
    else:
        view.add_item(item=RemoveInstButton(bot, author, db, donate))
    if info['vk'] == "Не установлен":
        view.add_item(item=SetVKButton(bot, author, db, donate))
    else:
        view.add_item(item=RemoveVKButton(bot, author, db, donate))
    if info['tg'] == "Не установлен":
        view.add_item(item=SetTelegramButton(bot, author, db, donate))
    else:
        view.add_item(item=RemoveTelegramButton(bot, author, db, donate))
    return embed, view


async def SetStatusEmbed(bot, author, interaction, db, donate):
    view = ui.View()
    embed = Embed(title=f"Установить статус", description=f"{interaction.user.mention}, укажите свой **статус**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    await interaction.response.edit_message(embed=embed, view=view)
    msg = await bot.wait_for("message")
    while msg.author != interaction.user:
        msg = await bot.wait_for("message")
    await msg.delete()
    embed = Embed(title=f"Установить статус",
                  description=f"{interaction.user.mention}, Вы **установили** свой **статус**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    view.add_item(item=BackToProfileManageButton(bot, author, db, donate))
    db[str(interaction.guild_id)].update_one({"id": interaction.user.id}, {"$set": {"status": msg.content}})
    await interaction.message.edit(embed=embed, view=view)
    return embed, view


async def RemoveStatusEmbed(bot, author, interaction, db, donate):
    view = ui.View()
    embed = Embed(title=f"Удалить статус",
                  description=f"{interaction.user.mention}, Вы **удалили** свой **статус**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    view.add_item(item=BackToProfileManageButton(bot, author, db, donate))
    db[str(interaction.guild_id)].update_one({"id": interaction.user.id}, {"$set": {"status": "Не установлен"}})
    await interaction.message.edit(embed=embed, view=view)
    return embed, view


async def RemoveInstEmbed(bot, author, interaction, db, donate):
    view = ui.View()
    embed = Embed(title=f"Удалить Instagram",
                  description=f"{interaction.user.mention}, Вы **удалили** свой **Instagram**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    view.add_item(item=BackToProfileManageButton(bot, author, db, donate))
    db[str(interaction.guild_id)].update_one({"id": interaction.user.id}, {"$set": {"inst": "Не установлен"}})
    await interaction.message.edit(embed=embed, view=view)
    return embed, view


async def SetInstEmbed(bot, author, interaction, db, donate):
    view = ui.View()
    embed = Embed(title=f"Установить Instagram",
                  description=f"{interaction.user.mention}, "
                              f"укажите **имя пользователя Instagram**, например **djsega**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    await interaction.response.edit_message(embed=embed, view=view)
    msg = await bot.wait_for("message")
    while msg.author != interaction.user:
        msg = await bot.wait_for("message")
    await msg.delete()
    embed = Embed(title=f"Установить Instagram",
                  description=f"{interaction.user.mention}, Вы **установили** свой **Instagram**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    view.add_item(item=BackToProfileManageButton(bot, author, db, donate))
    db[str(interaction.guild_id)].update_one({"id": interaction.user.id},
                                             {"$set": {"inst": f"instagram.com/{msg.content}"}})
    await interaction.message.edit(embed=embed, view=view)
    return embed, view


async def RemoveVKEmbed(bot, author, interaction, db, donate):
    view = ui.View()
    embed = Embed(title=f"Удалить VK",
                  description=f"{interaction.user.mention}, Вы **удалили** свой **VK**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    view.add_item(item=BackToProfileManageButton(bot, author, db, donate))
    db[str(interaction.guild_id)].update_one({"id": interaction.user.id}, {"$set": {"vk": "Не установлен"}})
    await interaction.message.edit(embed=embed, view=view)
    return embed, view


async def SetVKEmbed(bot, author, interaction, db, donate):
    view = ui.View()
    embed = Embed(title=f"Установить VK",
                  description=f"{interaction.user.mention}, "
                              f"укажите **id/имя пользователя Instagram**, например **djsega** или **id132132**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    await interaction.response.edit_message(embed=embed, view=view)
    msg = await bot.wait_for("message")
    while msg.author != interaction.user:
        msg = await bot.wait_for("message")
    await msg.delete()
    embed = Embed(title=f"Установить VK",
                  description=f"{interaction.user.mention}, Вы **установили** свой **VK**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    view.add_item(item=BackToProfileManageButton(bot, author, db, donate))
    db[str(interaction.guild_id)].update_one({"id": interaction.user.id},
                                             {"$set": {"vk": f"vk.com/{msg.content}"}})
    await interaction.message.edit(embed=embed, view=view)
    return embed, view


async def RemoveTelegramEmbed(bot, author, interaction, db, donate):
    view = ui.View()
    embed = Embed(title=f"Удалить Telegram",
                  description=f"{interaction.user.mention}, Вы **удалили** свой **Telegram**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    view.add_item(item=BackToProfileManageButton(bot, author, db, donate))
    db[str(interaction.guild_id)].update_one({"id": interaction.user.id}, {"$set": {"tg": "Не установлен"}})
    await interaction.message.edit(embed=embed, view=view)
    return embed, view


async def SetTelegramEmbed(bot, author, interaction, db, donate):
    view = ui.View()
    embed = Embed(title=f"Установить Telegram",
                  description=f"{interaction.user.mention}, "
                              f"укажите **имя пользователя Telegram**, например **djsega**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    await interaction.response.edit_message(embed=embed, view=view)
    msg = await bot.wait_for("message")
    while msg.author != interaction.user:
        msg = await bot.wait_for("message")
    await msg.delete()
    embed = Embed(title=f"Установить Telegram",
                  description=f"{interaction.user.mention}, Вы **установили** свой **Telegram**")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    view = ui.View()
    view.add_item(item=BackToProfileManageButton(bot, author, db, donate))
    db[str(interaction.guild_id)].update_one({"id": interaction.user.id},
                                             {"$set": {"tg": f"t.me/{msg.content}"}})
    await interaction.message.edit(embed=embed, view=view)
    return embed, view


# ---------------
# Profile Buttons
# ---------------


class DonateButton(ui.Button):
    def __init__(self, donate):
        super().__init__(label="Купить привилегии", url=donate)


class RemoveStatusButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.red, label="Удалить статус", row=1)
        self.bot = bot
        self.db = db
        self.author = author
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await RemoveStatusEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class SetInstButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.green, label="Установить Instagram", row=2)
        self.bot = bot
        self.db = db
        self.author = author
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await SetInstEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class RemoveInstButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.red, label="Удалить Instagram", row=2)
        self.bot = bot
        self.author = author
        self.db = db
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await RemoveInstEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class SetVKButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.green, label="Установить VK", row=2)
        self.bot = bot
        self.db = db
        self.author = author
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await SetVKEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class RemoveVKButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.red, label="Удалить VK", row=2)
        self.bot = bot
        self.author = author
        self.db = db
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await RemoveVKEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class SetTelegramButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.green, label="Установить Telegram", row=2)
        self.bot = bot
        self.author = author
        self.db = db
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await SetTelegramEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class RemoveTelegramButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.red, label="Удалить Telegram", row=2)
        self.bot = bot
        self.author = author
        self.db = db
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await RemoveTelegramEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class BackToProfileManageButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.blurple, label="Вернуться к управлению профилем")
        self.bot = bot
        self.author = author
        self.db = db
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await ProfileManageEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class OpenProfileManageButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.green, label="Открыть управление профилем")
        self.bot = bot
        self.db = db
        self.author = author
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await ProfileManageEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class CloseProfileManageButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.red, label="Закрыть управление профилем")
        self.bot = bot
        self.db = db
        self.author = author
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await ProfileEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class SetStatusButton(ui.Button):
    def __init__(self, bot, author, db, donate):
        super().__init__(style=ButtonStyle.green, label="Установить статус", row=1)
        self.bot = bot
        self.db = db
        self.author = author
        self.donate = donate

    async def callback(self, interaction: Interaction):
        if interaction.user.id == self.author.id:
            embed, view = await SetStatusEmbed(self.bot, self.author, interaction, self.db, self.donate)
            await interaction.message.edit(embed=embed, view=view)
        else:
            embed, view = await NotYourButtonEmbed(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
