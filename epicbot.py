import discord
from discord.ext import commands
import requests
import json
import random
import asyncio
import datetime
import praw
from discord import FFmpegPCMAudio
from discord.utils import get
from mutagen.mp3 import MP3

# Epic Bot Setup
intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="=", intents=intents)  # Bot Prefix
color = 0xfff700  # Embed Color
#bot.remove_command('help')  For custom help command later
owners = ["762104443289993227"]  # Owners

# Tells you if ready
@bot.event
async def on_ready():
    print('Ready!')

# Playsound


# Epic Commands
@bot.command(pass_context=True)
async def rdoujin(ctx):
    x = random.randint(100000, 999999)
    await ctx.send(f'https://nhentai.net/g/{str(x)}')

# Random Reddit Post
def rreddit(subreddit):
    with open('praw.json', 'r') as f:
        pr = json.load(f)
    reddit = praw.Reddit(client_id=pr["clientid"], client_secret=pr["clientsecret"], user_agent=pr["useragent"])
    submission = reddit.subreddit(subreddit).random()
    if not submission.author:
        name = '[deleted]'
    else:
        name = submission.author.name
    memes = submission.url
    return name, memes


@bot.command
async def reminder(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    embed.set_footer(
        text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link "
             "hidden",
        icon_url=f"{bot.user.avatar_url}")
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning',
                        value='Please specify what do you want me to remind you about.')  # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration, send `reminder_help` for more information.')
    elif seconds < 300:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)


# Reddit Stuff
@bot.command(pass_context=True)
async def hololive(ctx):
    with ctx.channel.typing():
        name, memes = rreddit('hololive')
        em = discord.Embed(color=color)
        em.set_image(url=memes)
        em.set_footer(text='Posted by u/' + name)
        await ctx.send(embed=em)


# Nice Cock
@bot.command(pass_context=True)
async def nicecockdm(ctx):
    for user in ctx.guild.members:
        if user.id != 810402957412925441:
            try:
                await user.send("nice cock")
            except discord.errors.Forbidden:
                pass

@bot.command(pass_context=True)
async def playsound(ctx, arg1):
    song = arg1+".mp3"
    audio = MP3(song)
    length = audio.info.length + 2
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("> Not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        source = FFmpegPCMAudio(song)
        player = voice.play(source)
        await asyncio.sleep(length)
        await voice.disconnect()




@bot.command(pass_context=True)
async def sotp(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("> Not connected.")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel
    print(f'Voice Disconnected On {channel}')
    if voice and voice.is_connected():
        await voice.disconnect()

with open('configs.json', 'r') as f:
    token = json.load(f)
    bot.run(token['3'])
