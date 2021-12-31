from nextcord.ext import commands
from nextcord import *
import datetime


class Daily(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @slash_command()
    async def daily(self, interaction):
        guild_info = self.db[str(interaction.guild_id)].find_one()
        mp = 1
        if interaction.user.premium_since:
            mp = guild_info["booster_mp"]
        value = guild_info["daily"] * mp
        cd = self.db[str(interaction.guild_id)].find_one({'id': interaction.user.id})["daily_cd"]
        time = datetime.datetime.now()
        if time >= cd:
            emb = Embed(title="Временные награды",
                        description=f"{interaction.user.mention},"
                                    f" Вы **забрали** свои **{value}** коинов. "
                                    f"Возвращайтесь через **{guild_info['daily_cd']}** "
                                    f"часов.\n\nМножитель бустера: **x{mp}**")
            emb.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=emb)
            self.db[str(interaction.guild_id)].update_one({'id': interaction.user.id},
                                                          {'$set': {'daily_cd': time + datetime.timedelta(
                                                              hours=guild_info["daily_cd"])}})
            self.db[str(interaction.guild_id)].update_one({'id': interaction.user.id},
                                                          {'$inc': {'cash': value}})
        else:
            x = cd - time
            emb = Embed(title="Временные награды",
                        description=f"{interaction.user.mention},"
                                    f" Вы **уже** забрали свою **временную** награду!"
                                    f" Вы можете **получить** следующую через **{x.seconds // 3600}** часов,"
                                    f" **{x.seconds % 3600 // 60}** минут, **{x.seconds % 60}** секунд.")
            emb.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=emb)
