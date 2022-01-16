from nextcord.ext.tasks import loop


@loop(seconds=1)
async def pay(bot, database):
    for i in database.list_collections():

        if i["name"] == "config" or i['name'] == "system.indexes":
            continue

        collection = database[i["name"]]

        settings = None
        tick = None
        reward = None

        for document in collection.find({}):

            try:
                settings = document
                tick = settings["tick"]
                reward = settings["reward"]
                break
            except:
                continue

        if settings is None:
            print("Предупреждение {settings}: " + f"{i['name']}")
            contine

        if tick is None:
            print("Предупреждение {tick}: " + f"{i['name']}")
            continue

        if reward is None:
            print("Предупреждение {reward}: " + f"{i['name']}")
            continue

        guild = bot.get_guild(int(i["name"]))

        if guild:

            for channel in bot.get_guild(int(i["name"])).voice_channels:

                for member in channel.members:

                    state = member.voice

                    if state.deaf or state.mute or state.self_deaf or state.self_mute or state.suppress:
                        continue

                    collection.update_one({"id": member.id}, {"$inc": {"online_all": 1, "online_today": 1}})

                    if (pay.current_loop + 1) % tick == 0:
                        collection.update_one({"id": member.id}, {"$inc": {"cash": reward}})

        await bot.wait_until_ready()
