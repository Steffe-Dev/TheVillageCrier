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
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SYS_MSSG = os.getenv('DISCORD_SYS_MSSG')
BOT_VOICE_CH = os.getenv('DISCORD_BOT_VOICE_CH')
BOT_TS_CH = os.getenv('DISCORD_BOT_TS_CH')
# initializes client
bot = commands.Bot(command_prefix='w>')

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
    await bot.change_presence(activity=discord.Game(name="w>help"))

@bot.command(name='hi', help='Prints a greeting')
async def help_list(ctx):
    response = (
        'Behold, puny mortals, for I am  the mighty Village Wizard!\n'
        'Fight me, if you dare...\n'
        'Not even STeFFe, my creator, can stop me!\n'
        '(Use the w>help command for a list of what I can do.)'
    )
    await ctx.send(response)

@bot.command(name='join', help='Joins the current channel')
async def join_test(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='Leaves the current channel', catagory='commands')
async def leave_test(ctx):
    await ctx.voice_client.disconnect() 

@bot.command(name='fight',  help='Challenge the wizard to a duel.')

 

async def fight(ctx):
    def check(author):
        def inner_check(message):
            if message.author != author:
                return False
            try:
                int(message.content)
                if (message.content == "1" or  message.content == "2" or message.content == "3" or message.content == "4"):
                    return True
                else:
                    return False
            except ValueError:
                return False
            return inner_check
        return inner_check

    initial_response = (
        'So,  you wish to  fight  me? Very well...'
    )
    await ctx.send(initial_response)

    player_turn = True
    wizard_stats = [100,100]
    player_stats = [100,100]
    spell_prob = [.25,.25,.25,.25]
    full_dmg  =  30.
    mana_mult = 20.

    def damage(response):
        # object conating data about the attack [spell, dmg]
        data  =  [response,0.0]
        rand = random.uniform(0,1)
        if rand > (1 - spell_prob[response]):
            data[1] = full_dmg
            if player_turn:
                wizard_stats[0] -= full_dmg
            else:
                player_stats[0] -= full_dmg
        else:
            dam =  (spell_prob[response] + rand) * full_dmg
            data[1] = dam
            if player_turn:
                wizard_stats[0] -= dam 
            else:
                player_stats[0] -= dam 

        if player_turn:
            player_stats[1] -=  spell_prob[response] * mana_mult
        else:
            wizard_stats[1] -=  spell_prob[response] * mana_mult
        
        for i in range(0,len(spell_prob)):
            if i == response:
                spell_prob[i] -= 0.05 * spell_prob[i]
            else:
                spell_prob[i] += 0.05 * spell_prob[i]
        return data

    while player_stats[0] > 0 and wizard_stats[0] > 0:
        if player_turn:
            
            player_turn_response = (
                f'========================================\n'
                f'Your Turn!\nHealth: {player_stats[0]:.2f}, Mana: {player_stats[1]:.2f}\n\n'
                f'What do you do? (Full spell damage: {full_dmg})\n'
                f'1. Fire spell ({spell_prob[0]:.2f} probability for full dmg) ({(spell_prob[0] * mana_mult):.2f} mana)\n'
                f'2. Ice spell ({spell_prob[1]:.2f} probability for full dmg) ({(spell_prob[1] * mana_mult):.2f} mana)\n'
                f'3. Wind spell ({spell_prob[2]:.2f} probability for full dmg) ({(spell_prob[2] * mana_mult):.2f} mana)\n'
                f'4. Earth spell ({spell_prob[3]:.2f} probability for full dmg) ({(spell_prob[3] * mana_mult):.2f} mana)\n'
                'Act in 30 seconds!\n'
                f'========================================\n'
            )
            await ctx.send(player_turn_response)
            player_response = await bot.wait_for('message', check=check(ctx.author), timeout=30)
            p_response = int(player_response.content) -  1
            data_p = damage(p_response) 
            await ctx.send(f'{data_p[0]+1} was used and did {data_p[1]} damage!\n')
        else:
            
            wiz_turn_response = (
                f'========================================\n'
                f'My Turn!\nHealth: {wizard_stats[0]:.2f}, Mana: {wizard_stats[1]:.2f}\n\n'
                f'What shall I do? (Full spell damage: {full_dmg})\n'
                f'1. Fire spell  ({spell_prob[0]:.2f} probability for full dmg) ({(spell_prob[0] * mana_mult):.2f} mana)\n'
                f'2. Ice spell  ({spell_prob[1]:.2f} probability for full dmg) ({(spell_prob[1] * mana_mult):.2f} mana)\n'
                f'3. Wind spell  ({spell_prob[2]:.2f} probability for full dmg) ({(spell_prob[2] * mana_mult):.2f} mana)\n'
                f'4. Earth spell  ({spell_prob[3]:.2f} probability for full dmg) ({(spell_prob[3] * mana_mult):.2f} mana)\n'
                f'========================================\n'
            )
            await ctx.send(wiz_turn_response)
            wiz_response = random.randint(0,3) 
            data_w = damage(wiz_response)
            await ctx.send(f'{data_w[0]+1} was used and did {data_w[1]} damage!\n')
        player_turn = not player_turn

    if player_stats[0] <= 0:
        await ctx.send("As expected, you lose!")
    elif wizard_stats[0] <= 0:
        await ctx.send("What?! You beat me, how can this be...")

bot.run(TOKEN)
