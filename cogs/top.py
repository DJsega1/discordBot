from nextcord.ext import commands
from nextcord import *


class Top(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @slash_command()
    async def top(self, interaction):
        pass

    @top.subcommand()
    async def cash(self, interaction):
        users = self.db[str(interaction.guild_id)].find().sort("cash", -1).limit(11)
        desc = ""
        for i in users:
            try:
                desc += f'{self.bot.get_user(i["id"]).mention} - **{i["cash"]}**\n'
            except KeyError:
                continue
        embed = Embed(title="ТОП-10 пользователей по количеству валюты на балансе", description=desc)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @top.subcommand()
    async def online(self, interaction):
        users = list(self.db[str(interaction.guild_id)].find().sort("online_all", -1).limit(10))
        if len(users) < 11:
            users.pop()
        desc = ""
        for i in users:
            time = f"**{i['online_all'] // 3600}** часов, **{i['online_all'] % 3600 // 60}** минут," \
                   f" **{i['online_all'] % 60}** секунд"
            try:
                desc += f'{self.bot.get_user(i["id"]).mention} - {time}\n'
            except KeyError:
                pass
        embed = Embed(title="ТОП-10 пользователей по онлайну", description=desc)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)
