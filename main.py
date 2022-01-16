import datetime
from pymongo import MongoClient
import nextcord
from background_tasks import *
from nextcord.ext.commands import AutoShardedBot
from cogs.profile import Profile
from cogs.transfer import Transfer
from cogs.daily import Daily
from cogs.top import Top
from cogs.duels import Duels
from cogs.personal_roles import Roles

client = MongoClient('localhost', 27017)
db = client["guildRyoko"]
intents = nextcord.Intents.default()
intents.members = True


def new_member(collection, member):
    if not collection.find_one({"id": member.id}):
        collection.insert_one({"id": member.id, "cash": 0, "donate": 0, "status": "Не установлен",
                               "inst": "Не установлен", "vk": "Не установлен", "tg": "Не установлен",
                               "online_all": 0, "online_today": 0, "marry": "Отсутствует", "marry_time": None,
                               "messages": 0, "room": None, "own_roles": [], "bought_roles": [],
                               "daily_cd": datetime.datetime(2020, 1, 1)})


def guild_check(collection):
    if not list(collection.find()):
        collection.insert_one({"commission": 4, "daily": 50, "booster_mp": 2, "tick": 120, "reward": 1,
                               "donate_url": "https://discord.gg/6UnUNyqeF3", "daily_cd": 12, "emoji": None})


class MyBot(AutoShardedBot):

    def __init__(self):
        super().__init__(command_prefix="/", shard_count=2, intents=intents)
        self.flag = True

    async def on_guild_join(self, guild):
        col = db[str(guild.id)]
        guild_check(col)
        await self.wait_until_ready()
        members = guild.members
        for i in members:
            new_member(col, i)
        await self.wait_until_ready()

    async def on_member_join(self, member):
        col = db[str(member.guild.id)]
        new_member(col, member)

    async def on_ready(self):
        if self.flag:
            guilds = self.guilds
            for i in guilds:
                col = db[str(i.id)]
                guild_check(col)
                await self.wait_until_ready()
                for j in i.members:
                    new_member(col, j)
                await self.wait_until_ready()
            pay.start(self, db)
            self.flag = False
        print(1)


bot = MyBot()
bot.add_cog(Transfer(bot, db))
bot.add_cog(Profile(bot, db))
bot.add_cog(Daily(bot, db))
bot.add_cog(Roles(bot, db))
bot.add_cog(Top(bot, db))
bot.add_cog(Duels(bot, db))

bot.run("OTE1NzA4MzM1NjI4NjI4MDA4.Yafh2A.T2UFhjqE7sGh-STTGFL6HhK2o_c")
