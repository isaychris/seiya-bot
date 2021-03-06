import discord
import configparser
import time
from discord.ext import commands
from plugins import rand_joke, cryptoPrice, saucenao, translater, image, dice, youtube as yt, helper

description = '''A simple discord bot using discord.py'''
bot = commands.Bot(command_prefix='!', description=description)

config = configparser.ConfigParser()
config.read('config.ini')
token = config['DEFAULT']['BOT_TOKEN']

start = time.time()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(name='youtube', description='Returns the first video result from youtube')
async def youtube(*args : str):
    query = ' '.join(args)
    url = yt.getVideo(query, config['DEFAULT']['GOOGLE_KEY'])

    if url is None:
        await bot.say('Unable to retrieve information ... ')
        return

    await bot.say(url)


@bot.command(name='translate', description='Translates english to japanese or vice versa')
async def translate(target : str, *args : str):
    message = ' '.join(args)

    if target == 'ja':
        result = translater.getTranslation(target, message, config['DEFAULT']['GOOGLE_KEY'])
        embed = discord.Embed(title='Japanese translation', description=result, color=0x7289da)
    else:
        result = translater.getTranslation(target, message, config['DEFAULT']['GOOGLE_KEY'])
        embed = discord.Embed(title='English translation', description=result, color=0x7289da)

    await bot.say(embed=embed)


@bot.command(name='price', description='Retrieves the price of a cryptocurrency.')
async def price(name : str ):
    coin = cryptoPrice.getPrice(name,)

    if coin is None:
        await bot.say('Unable to retrieve information ... ')
        return

    message = '$ {}  |  ({}%) 24h'.format(coin['price_usd'], coin['percent_change_24h'])
    embed = discord.Embed(title=name, description=message, color=0x7289da)

    await bot.say(embed=embed)


@bot.command(name='sauce', description='Retrieves the source of an anime image, returning its name, episode, and time.')
async def sauce(url : str):
    anime = saucenao.getSauce(url, config['DEFAULT']['SAUCENAO_KEY'])

    if anime is None:
        await bot.say('Unable to retrieve information ... ')
        return

    message = '{} - Episode {} - {}'.format(anime['source'], anime['part'], anime['est_time'])

    embed = discord.Embed(title='Sauce', description=message, color=0x7289da)

    await bot.say(embed=embed)


@bot.command(name='search', description='Returns the first image result on bing search engine.')
async def search(*args : str):
    input = ' '.join(args)

    result = image.getImage(input, config['DEFAULT']['BING_KEY'])
    embed = discord.Embed(title=input, color=0x7289da)
    embed.set_image(url=result)

    await bot.say(embed=embed)


@bot.command(name='joke', description='Returns a random joke to the user.')
async def joke():
    result = rand_joke.getJoke()
    embed = discord.Embed(title='Joke', description=result, color=0x7289da)

    await bot.say(embed=embed)


@bot.command(name='roll', description='Returns a random number between 0-100.')
async def roll():
    result = dice.getDice()
    embed = discord.Embed(title='Dice', description=result, color=0x7289da)
    await bot.say(embed=embed)


@bot.command(name='status', description='Returns the status of the bot.')
async def status():
    day, hour, minutes, seconds = helper.getElapsedTime((time.time() - start))
    message = '{}d, {}h, {}m, {}s'.format(day, hour, minutes, seconds)

    embed = discord.Embed(title=' ', description=' ', color=0x7289da)
    embed.add_field(name='Online', value=message)
    embed.add_field(name='Servers', value=str(len(bot.servers)))

    await bot.say(embed=embed)


bot.run(token)