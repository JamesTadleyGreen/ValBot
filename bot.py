# bot.py
import os
import random
from dotenv import load_dotenv
import discord

import api
import data_manipulation as dm
import database_functions as df
import json


from strats import strats

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 2
bot = commands.Bot(command_prefix="|")


# Strats generator
selection = strats["generic"]


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="add_player", help="Adds a new player to check the stats with")
async def add_players(ctx, player):
    response = df.add_player_to_list(player)
    await ctx.send(response)


@bot.command(name="remove_player", help="Removes an existing player from the database")
@commands.has_role("Mod")
async def rm_players(ctx, player):
    response = df.remove_player_from_list(player)
    await ctx.send(response)


@bot.command(name="online", help="Checks if anyone's in game")
async def update(ctx):
    embedVar = discord.Embed(title="Who's online", description="", color=0x00FF00)
    online_list = dm.get_online_players()
    for player in online_list:
        name, online = player
        emoji = ":heart:"
        if online:
            emoji = ":green_heart:"
        embedVar.add_field(name=name, value=emoji, inline=False)
    await ctx.send(embed=embedVar)


@bot.command(name="update", help="Updates the stored stats")
async def update(ctx):
    await ctx.send(df.update_players_info())


@bot.command(name="val_players", help="Finds out last time people were online")
async def val_players(ctx):
    # print(api.update_players_info())
    embedVar = discord.Embed(
        title="Most recent game.",
        description="The last time we saw the following players. :clock10:",
        color=0x00FF00,
    )
    for player in dm.get_player_list()["players"]:
        embedVar.add_field(
            name=player["nickname"], value=player["last_online"], inline=False
        )
    await ctx.send(embed=embedVar)


@bot.command(name="nickname", help="Updates the nickname for a player")
async def update(ctx, player, nickname):
    await ctx.send(df.set_player_nickname(player, nickname))


@bot.command(name="ranks", help="Progression within ranks")
async def ranks(ctx):
    # print(api.update_players_info())
    embedVar = discord.Embed(
        title="Ranks.", description="The current ranks of players.", color=0x00FF00
    )
    for player in sorted(
        dm.get_player_list()["players"],
        key=lambda x: x["rank_data"]["elo"],
        reverse=True,
    ):
        embedVar.add_field(
            name=f"{player['nickname']} {dm.rank_emoji(player['rank_data']['currenttierpatched'])}",
            value=f"{dm.rank_prog_emoji(player['rank_data']['ranking_in_tier'])}",
            inline=False,
        )
    await ctx.send(embed=embedVar)


@bot.command(name="wimp", help="Progression within ranks")
async def wimp(ctx, player):
    # print(api.update_players_info())
    embedVarRed = discord.Embed(
        title="Who's been wimpy today then.",
        description="Tells you who's been a little bitch on attack / defense.",
        color=0xFF0000,
    )
    embedVarBlue = discord.Embed(
        title="Who's been wimpy today then.",
        description="Tells you who's been a little bitch on attack / defense.",
        color=0x0000FF,
    )
    print("Fetching match data")
    match_data = api.get_match_info(player).json()["data"]["matches"]
    print("Got match data")
    for player in dm.last_to_die(match_data[0])["Red"]:
        embedVarRed.add_field(
            name=f'{player["name"]}',
            value=f':scream_cat:: {player["pussy_score"]}\t:sloth:: {player["rotate_score"]}',
            inline=False,
        )
    for player in dm.last_to_die(match_data[0])["Blue"]:
        embedVarBlue.add_field(
            name=f'{player["name"]}',
            value=f':scream_cat:: {player["pussy_score"]}\t:sloth:: {player["rotate_score"]}',
            inline=False,
        )
    await ctx.send(embed=embedVarRed)
    await ctx.send(embed=embedVarBlue)


@bot.command(name="adam", help="Finds out how many kills adam got in the last game")
async def val_players(ctx):
    await ctx.send("Less than 10 lol")


@bot.command(name="congrats", help="Congratulates you")
async def congrats(ctx):
    await ctx.send("https://media.giphy.com/media/d31w24psGYeekCZy/giphy.gif")


@bot.command(name="roll_dice", help="Simulates rolling dice.")
# @commands.has_role('Mod')
async def roll(ctx, number_of_dice=1, number_of_sides=6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)
    ]
    await ctx.send(", ".join(dice))


@bot.command(
    name="strat",
    help="Generates a strat, optionally provide a map or side",
)
async def strat(ctx, map: str = None, side: str = None, selection=selection):
    if side is not None:
        selection = strats["generic"]
        selection += strats[map.lower()]
        selection += strats[side.lower()]
    await ctx.send(random.choice(selection))


@bot.command(
    name="strats",
    help="Prints all strats",
)
async def print_strats(ctx):
    strats_string = json.dumps(strats)
    await ctx.send(strats_string)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Not a command *mate*.")


bot.run(TOKEN)
