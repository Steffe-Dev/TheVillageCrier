# Discord Bot for The Village
#
# Known Issues:
#   if roll is called without a param, no msg is displayed to correct the user.

import os
import discord
import random
import asyncio
from discord import opus
from dotenv import load_dotenv
####################################################################

from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/701078183470170143/2rFMyamI87z3SvBYFKFCP_BFcr4iFSxlZ31AOG77Dm2aWAdqvVYAin1_5Wlw9-ZTTx9c')

# create embed object for webhook
embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color=242424)

# add embed object to webhook
webhook.add_embed(embed)

response = webhook.execute()
#######################################################################

from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SYS_MSSG = os.getenv('DISCORD_SYS_MSSG')
BOT_VOICE_CH = os.getenv('DISCORD_BOT_VOICE_CH')
BOT_TS_CH = os.getenv('DISCORD_BOT_TS_CH')
# initializes client
bot = commands.Bot(command_prefix='>>')

# defines event handler for when client connects to discord
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    
    print(
        f'{bot.user} has connected to the following Discord guild:\n'
        f'{guild.name}(id: {guild.id})'    
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.command(name='hi', help='Prints a greeting')
async def help_list(ctx):
    response = (
        'Hear, Hear! I am the village crier! I am also a bot written by STeFFe with the function\n'
        'Of bringing you all the latest news!\n'
        'My creator hopes to improve my functionality in the future.'
        'Use the >>help command for a list of what I can do.'
    )
    await ctx.send(response)

@bot.command(name='join', help='Joins the current channel')
async def join_test(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='Leaves the current channel', catagory='commands')
async def leave_test(ctx):
    await ctx.voice_client.disconnect() 

bot.run(TOKEN)
