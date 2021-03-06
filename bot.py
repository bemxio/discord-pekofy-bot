from discord.ext import commands
import pekofy as peko # because i am gonna copy paste a lot of stuff
import credentials
import replies
import discord
import random

client = discord.Client()
keyphrase = '!pekofy'

def reply_chance(percent):
    return random.randint(0, 100) <= percent

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name=replies.status_content))
    
@client.event
@commands.cooldown(1, 5, commands.BucketType.user)
async def on_message(message):
    if message.author == client.user:
        return

    # pain peko (not used regex for faster results)
    if message.content.lower() in ["pain", "pain.", "pain...", "pain peko", "pain peko."] and reply_chance(50):
        await message.channel.send(replies.pain_peko_reply)

    # hey moona
    if "moona" in message.content.lower() and "pekora" in message.content.lower() and reply_chance(25):
        await message.channel.send(replies.hey_moona_reply)
    
    # pekofy command
    if message.content.startswith(keyphrase):
        channel = message.channel
        
        if message.reference:
            reply = message.reference.resolved
        else:
            return
            
        if reply.author.bot:
            await message.channel.send(replies.bot_detected)
            return
        
        reply = reply.content
        """
        try:
            reply = message.reference.resolved.content
        except AttributeError: # if no message.reference found
            reply = await channel.history(limit=2).flatten()
            reply = reply[1].content
        """
        reply = peko.pekofy(reply)
        
        # if it couldn't be pekofied, give a random pekora clip
        if reply in ["NOTHING_CHANGED", "NO_LETTER"]:
            reply = random.choice(replies.nothing_changed_reply_list)
        
        await message.channel.send(reply)
    
    if message.content.lower() == "insult me peko":
        await message.channel.send(random.choice(replies.insults))
    
    if message.content == "!pekopasta":  # easter egg
        await message.channel.send(replies.cursed_pekopasta)
    
    # rating reactions
    if message.reference:
        if message.reference.resolved.author == client.user:
            if "good bot" in message.content.lower():
                await message.channel.send(random.choice(replies.thanks))
            if "bad bot" in message.content.lower():
                await message.channel.send(random.choice(replies.sorrys))         
            if "cute bot" in message.content.lower():
                await message.channel.send(random.choice(replies.cutes))
        
client.run(credentials.token)