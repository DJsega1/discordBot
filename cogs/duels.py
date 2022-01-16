from nextcord.ext import commands
from nextcord import *
from random import randint


class FightButton(ui.Button):
    def __init__(self, bot, db, bet, author, user=None):
        self.bot = bot
        self.db = db
        self.bet = bet
        self.author = author
        self.user = user
        super().__init__(label="Сразиться", style=ButtonStyle.blurple)

    async def play(self, interaction):
        if self.db[str(interaction.guild_id)].find_one({'id': interaction.user.id})["cash"] < self.bet:
            embed = Embed(title="Дуэли",
                          description=f"{interaction.user.mention}, у Вас **недостаточно средств**")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            value = int(self.bet * (1 - (self.db[str(interaction.guild_id)].find_one({})["commission"] / 100)))
            if randint(1, 2) == 1:
                desc = f"В **дуэли** победу одержал {self.author.mention} " \
                       f"и получил **{value}**\n\n**Вызов принял: {interaction.user.mention}**"
                self.db[str(interaction.guild_id)].update_one({"id": self.author.id},
                                                              {"$inc": {"cash": self.bet + value}})
                self.db[str(interaction.guild_id)].update_one({"id": interaction.user.id},
                                                              {"$inc": {"cash": -self.bet}})
            else:
                desc = f"В **дуэли** победу одержал {interaction.user.mention} " \
                       f"и получил **{value}**\n\n**Вызов принял: {interaction.user.mention}**"
                self.db[str(interaction.guild_id)].update_one({"id": interaction.user.id},
                                                              {"$inc": {"cash": value}})
            embed = Embed(title="Дуэли",
                          description=desc)
            embed.set_thumbnail(url=interaction.message.author.display_avatar.url)
            await interaction.response.edit_message(embed=embed, view=None)

    async def callback(self, interaction: Interaction):
        if self.user:
            if self.user == interaction.user:
                await self.play(interaction)
        else:
            if interaction.user == self.author:
                embed = Embed(title="Дуэли",
                              description=f"{interaction.user.mention}, Вы не можете **сражаться** с самим собой")
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await self.play(interaction)


class Duels(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @slash_command()
    async def duel(self, interaction, bet: int = SlashOption(name="bet", description="Ставка", required=True),
                   user: User = SlashOption(name="user", description="Пользователь", required=False)):
        if user == interaction.user:
            embed = Embed(title="Дуэли",
                          description=f"{interaction.user.mention}, Вы не можете **сражаться** с самим собой")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        if bet < 50:
            embed = Embed(title="Дуэли",
                          description=f"{interaction.user.mention}, ставка не может быть менее **50**")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        if self.db[str(interaction.guild_id)].find_one({'id': interaction.user.id})["cash"] < bet:
            embed = Embed(title="Дуэли",
                          description=f"{interaction.user.mention}, у Вас **недостаточно средств**")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        view = ui.View()
        self.db[str(interaction.guild_id)].update_one({'id': interaction.user.id}, {"$inc": {"cash": -bet}})
        if user:
            embed = Embed(title=f"Дуэли",
                          description=f"{interaction.user.mention} хочет **сразиться** c {user.mention} на **{bet}**")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            view.add_item(FightButton(self.bot, self.db, bet, interaction.user))
            await interaction.response.send_message(embed=embed, view=view)
        else:
            embed = Embed(title=f"Дуэли",
                          description=f"{interaction.user.mention} хочет с кем-то **сразиться** на **{bet}**")
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            view.add_item(FightButton(self.bot, self.db, bet, interaction.user, user))
            await interaction.response.send_message(embed=embed, view=view)
