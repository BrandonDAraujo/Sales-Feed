import discord
import json
import asyncio

client = discord.Client()

with open("config.json") as a:
    config = json.load(a)

#Function that updates the config file
async def updateConfig(con):
    with open("config.json", "w") as a:
        json.dump(con, a)
    with open("config.json") as a:
        config = json.load(a)
    return config

#Main Timer Start Function
async def timerUpdate():
    while True:
        await asyncio.sleep(10)
        print(config['channel'])
        await client.get_channel(246792928209403904).send("test")


@client.event
async def on_ready():
    await timerUpdate()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

        #Change Main Channel ID
    if message.content.startswith(f"{config['prefix']}channel"):
        config['channel'] = message.content.replace(f"{config['prefix']}channel ", "")
        await updateConfig(config)
        await message.channel.send(f"Updated Channel to `{config['channel']}`")

        #List All NFT Projects
    elif message.content.startswith(f"{config['prefix']}list"):
        msg = ""
        if len(config['projects']) == 0:
            await message.channel.send(f"No projects currently registered. Use `{config['prefix']}add [project url]` to add a project to the list.")
            return
        for count, x in enumerate(config["projects"]):
            msg += f"**{count}.**   {config['projects'][count]}\n"
        discordEmbed = discord.Embed()
        discordEmbed.title = "NFT Project List"
        discordEmbed.description = msg
        await message.channel.send(embed=discordEmbed)
    
        #Add NFT Project
    elif message.content.startswith(f"{config['prefix']}add "):
        config['projects'].append(message.content.replace(f"{config['prefix']}add ", ""))
        await updateConfig(config)
        await message.add_reaction("✅")

        #Remove NFT Project
    elif message.content.startswith(f"{config['prefix']}remove "):
        config['projects'].pop(int(message.content.replace(f"{config['prefix']}remove ", "")))
        await updateConfig(config)
        await message.add_reaction("✅")
#Start Client
client.run(config["key"])