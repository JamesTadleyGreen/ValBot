# bot.py
import os
import random
from dotenv import load_dotenv
import api

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='|')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='val_players', help='Finds out last time people were online')
async def val_players(ctx):
    player_list = api.check_last_onlines()
    player_list = ["Players Last Seen:"] + player_list
    await ctx.send('\n'.join(player_list))

@bot.command(name='adam', help='Finds out how many kills adam got in the last game')
async def val_players(ctx):
    await ctx.send("Less than 10 lol")

@bot.command(name='roll_dice', help='Simulates rolling dice.')
#@commands.has_role('Mod')
async def roll(ctx, number_of_dice=1, number_of_sides=6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)