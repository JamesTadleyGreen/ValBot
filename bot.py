# bot.py
import os
import random
from dotenv import load_dotenv
import discord

import api

import giphy



# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='|')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='add_player', help='Adds a new player to check the stats with')
async def add_players(ctx, player):
    response = api.add_player_to_list(player)
    await ctx.send(response)

@bot.command(name='remove_player', help='Removes an existing player from the database')
@commands.has_role('Mod')
async def rm_players(ctx, player):
    response = api.remove_player_from_list(player)
    await ctx.send(response)

@bot.command(name='update', help='Updates the stored stats')
async def update(ctx):
    await ctx.send(api.update_players_info())

@bot.command(name='val_players', help='Finds out last time people were online')
async def val_players(ctx):
    #print(api.update_players_info())
    embedVar = discord.Embed(title="Most recent game.", description="The last time we saw the following players. :clock10:", color=0x00ff00)
    for player in api.get_player_list()['players']:
        embedVar.add_field(name=player["nickname"], value=player["last_online"], inline=False)
    await ctx.send(embed=embedVar)

@bot.command(name='nickname', help='Updates the nickname for a player')
async def update(ctx, player, nickname):
    await ctx.send(api.set_player_nickname(player, nickname))

@bot.command(name='ranks', help='Progression within ranks')
async def ranks(ctx):
    #print(api.update_players_info())
    embedVar = discord.Embed(title="Ranks.", description="The current ranks of players.", color=0x00ff00)
    for player in sorted(api.get_player_list()['players'], key=lambda x: x['rank_data']['elo'], reverse=True):
        embedVar.add_field(name=f"{player['nickname']} {api.rank_emoji(player['rank_data']['currenttierpatched'])}", value=f"{api.rank_prog_emoji(player['rank_data']['ranking_in_tier'])}", inline=False)
    await ctx.send(embed=embedVar)

@bot.command(name='adam', help='Finds out how many kills adam got in the last game')
async def val_players(ctx):
    await ctx.send("Less than 10 lol")

@bot.command(name='congrats', help='Congratulates you')
async def congrats(ctx):
    await ctx.send("https://media.giphy.com/media/d31w24psGYeekCZy/giphy.gif")

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
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Not a command mate")

bot.run(TOKEN)