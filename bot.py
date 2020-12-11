# bot.py
import os
import random
from dotenv import load_dotenv

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='|')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='HelloWorld', help='Says hello back')
async def hello_world(ctx):
    quotes = [
        'Hello there, General Kenobi'
    ]

    response = random.choice(quotes)
    await ctx.send(response)

@bot.command(name='howisjamie', help='Finds out how Jamie is')
async def hello_world(ctx):
    quotes = [
        'Bad, very bad',
        'About to quit'
    ]

    response = random.choice(quotes)
    await ctx.send(response)

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