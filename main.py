import os
import mysql.connector

import discord
from dotenv import load_dotenv
from discord.ext import commands

from Commands.Miscellanous.help import Help
from Commands.Miscellanous.ping import Ping
from Commands.Miscellanous.say import Say
from Commands.Moderation.warn import Warn, Warns

load_dotenv('config.env')

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

print("Connection to DataBase")
db = mysql.connector.connect(host=os.getenv('DBhost'), user=os.getenv('DBuser'), passwd=os.getenv('DBpasswd'), database="damaki_db")


@bot.event
async def on_ready():
    game = discord.Game("$help | Damaki © 2021")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print("Bot ready")


bot.remove_command('help')

bot.add_cog(Ping(bot))
bot.add_cog(Help(bot))
bot.add_cog(Say(bot))
bot.add_cog(Warn(bot, db))
bot.add_cog(Warns(bot, db))


bot.run(os.getenv('DISCORD_TOKEN'))
