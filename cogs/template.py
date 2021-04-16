import time
from discord import channel, member
from discord.ext import commands
import asyncio
import discord
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests,random,os,json
import misc
from discord.ext.commands import bot


PREFIX_FILE_NAME = "prefix.json"
WELCOME_FILE_NAME = "welcome.json"

ROOT_JSON_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir)+'/json' # os.path.dirname(os.path.realpath(__file__))
PREFIX_FILE_PATH = os.path.join(ROOT_JSON_PATH,PREFIX_FILE_NAME)
ROOT_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir) # os.path.dirname(os.path.realpath(__file__))
WELCOME_FILE_PATH = os.path.join(ROOT_JSON_PATH,WELCOME_FILE_NAME)


class BotEvent(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(BotEvent(bot))