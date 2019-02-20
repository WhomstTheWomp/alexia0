import discord
from discord import VoiceClient
from discord.ext import commands
import asyncio
import random
import datetime
import youtube_dl

# Whoever was responsible for the r/fCord thing. it was funny, and thanks for pointing out my dumb ass mistake 
# of giving my bots token inside of a public repository

# Variables
TOKEN = 'NTQ2OTUzMDE2NjM3NTIxOTIw.D0vvSQ.Ifv74CE6SDo9nVTg0_IOX3zcJZU'
client = commands.Bot(command_prefix='Alexia0 ')
client.remove_command('help')
questions = ['What was the best game of 2018?','What sex position do you think is most efficient?','What are your chores at home?',"What's your favorite fast food chain?",'What is your favorite type of rpg?(futuristic, fantasy, etc.)'
             ,'How long does it normally take for you to shower, and why?','How do you like your coffee?','How would you describe your aesthetic?','What is your most played game, and how many hours have you logged?'
             ,'What is your ideal superpower, why, and what would you do with it?','What is your ideal color scheme?', 'Do you prefer your books with a lot of picture, only pictures, few picture, little to none pictures or no pictures at all?'
             ,"What's your ethnicity?", 'On average, how much soda do you consume per day?',"What color is your room, if you like the color why? If you don't what would you change it to?"
             ,'What is your ideal lover and your child you would have with them?','At what age did you begin gaming?', 'If you were a murder how would you do it and what theme would you have between the murders if any',
             'What animated universe would you wanna be in','What type of music do you listen to, and how often?']
announcements = []
players = {}
queues = {}

# Queue check
def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        
        player.start()

        
# Initiation

@client.event
async def on_ready():
    print("Alexia0: Online")


# Question of the day
@client.command(pass_context=True)
@commands.cooldown(1, 86400, commands.BucketType.user)
async def qotd(ctx):
    await client.say('@here %s' % questions[random.randint(0,19)])


# Music playing
@client.command(pass_context=True)
async def RISE(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def die(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def earrape(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

    await client.say('Music_startUp: Initiated')

@client.command(pass_context=True)
async def skip(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def holup(ctx):
    id = ctx.message.server.id
    players[id].pause()

@client.command(pass_context=True)
async def nvm(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def q(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queues(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Music has been queued')

# Announcements
@client.command(pass_context=True)
async def announce(ctx):
    msgContent = ctx.message.content

    if msgContent == 'Alexia0 announce':
        if announcements == []:
            await client.say('No current announcements')
        else:
            await client.say(announcements)
    else:
        announcements.append(msgContent[16:100000])
        await client.say('Announcement logged')

@client.command(pass_context=True)
async def clear(ctx):
    announcements.clear()
    await client.say('Announcements have been cleared')

    
# Version info
@client.command()
async def version():
    await client.say("My current version is V1.3")

# New help command
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    dm = discord.Embed(
        color = discord.Colour.dark_purple())

    dm.set_author(name = 'Help')
    
    dm.add_field(name = 'Prefix', value = 'The command prefix is "Alexia0 "')
    dm.add_field(name = 'qotd', value = 'Randomly selects a question and sends it (only works once per day)')
    dm.add_field(name = 'RISE', value = 'Alexia0 will join whatever voice channel you are currently in')
    dm.add_field(name = 'die', value = 'Alexia0 will leave the voice channel you are in')
    dm.add_field(name = 'earrape', value = 'Alexia0 will play the following youtube video urls audio in the voice channel you are in')
    dm.add_field(name = 'q', value = 'Will add the following youtube video url to the queue')
    dm.add_field(name = 'skip', value = 'Skips the video being played')
    dm.add_field(name = 'holup', value = 'Pauses the video being played')
    dm.add_field(name = 'nvm', value = 'Resumes the video that was being played')
    dm.add_field(name = 'announce', value = 'Takes the text following the command and stores it. If you just type "Alexia0 announce" it will output the current announcments to the server')
    dm.add_field(name = 'version', value = 'Tells you the current version of Alexia0')
    dm.add_field(name = 'subgap', value = "Sends a url to FlareTv's youtube stream")
    
    await client.send_message(author, embed = dm)
    

# Hidden/Embedded Command section
@client.command(pass_context=True)
async def sucks(ctx):
    author = ctx.message.author

    await client.send_message(author, 'T H E  F U C K  D I D  Y O U  J U S T  S A Y  T O  M E  Y O U  L I T T L E  S H I T')

    await client.say("Congratultions %s! You found the hidden command, ya' dick head!" % author)


# Embarresing people for fuck ups                  
@client.event
async def on_message_delete(message):
    channel = message.channel
    author = message.author
    
    await client.send_message(channel, 'Did you fuck up, @%s?(Message Deleted)' % author)

    
# Misc Commands
@client.command()
async def subgap():
    await client.say('https://www.youtube.com/watch?v=UVxU2HzPGug')

    
client.run(TOKEN)
