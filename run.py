import json
import discord
import asyncio
from discord.ext import commands
from discord import Intents
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from discord.role import Role
import requests
import random,os
# from db import Database

PREFIX_FILE_NAME = "prefix.json"
WELCOME_FILE_NAME = "welcome.json"
ROOT_JSON_PATH = os.path.dirname(os.path.realpath(__file__))+'/json'
PREFIX_FILE_PATH = os.path.join(ROOT_JSON_PATH,PREFIX_FILE_NAME)
WELCOME_FILE_PATH = os.path.join(ROOT_JSON_PATH,WELCOME_FILE_NAME)

intents = discord.Intents.all()

def get_prefix(client,msg):
    with open(PREFIX_FILE_PATH,'r') as f:
        prefixes = json.load(f)
    return prefixes[str(msg.guild.id)]

# bot = commands.Bot(command_prefix=['y ','Y '],intents=intents)
bot = commands.Bot(command_prefix=get_prefix,intents=intents)

async def status_change():
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Activity_Name"))
        await asyncio.sleep(20)


@bot.command()
async def rules(ctx):
    if int(ctx.author.id) == "AUTHOR_ID": # Enter discord id
        data = """             
- Treat all members with respect.

- Harassment, abuse, hate speech or any kind of discriminatory speech will not be tolerated.  

- Do not in any way intentionally offend any member in the Discord server.  

- Racial or offensive slurs will not be tolerated.

- Tagging a member staff member without reason will result in a warning.

- Revealing private information about any individual;  is a zero tolerance rule.

- Do not publicly accuse other users players of misconduct.

- No backseat modding.

- No talking about topics related to religion or politics. 

- Words or small sentences  in other languages ​​other than English are allowed only for the purpose of teaching someone, or for clarification. 

- We welcome constructive criticism but have zero tolerance for aggressive or entitled demands. 

- Intentional toxic behavior is not allowed.
"""
        embed = discord.Embed(
            title="__***:fire:!           General Rules         !***__", description=data, color=0x00ff00)
        await ctx.send(embed=embed)
        data = """
- Anyone found with multiple accounts will get all the alternatives, as well as the original account, banned. 

- For you to get an exception for more than one account on the server, you'll have to contact a Discord Admin for permission.  

- Once an account ban is set, you're banned and not welcomed back until you properly appeal to the staff member that issued the punishment, 
and it gets approved.

- If you have any doubts about a staff member's decision, you are free to create a ticket and have another staff member review it.  

- Offensive / NSFW usernames or avatars are not allowed and will result in a warning if it remains unchanged. 

- Conducting any kind of real-world economic activity on this server is strictly prohibited, and may result in the account responsible getting terminate
"""
        embed = discord.Embed(
            title="__***:fire:!     Account security     !***__", description=data, color=0x00ff00)
        await ctx.send(embed=embed)
        data = """
- Bot commands are only to be used in the <#795237258297868298>

- Staff members reserved the right to use bot commands anywhere needed.

- Any form of abuse of the bots is forbidden.

- Do not spam in channels to gain experience for the ranking system.

- Userbots are strictly prohibited and will result in an instant ban. Terms of Service (ToS): 

- Every member is to follow https://discord.com/new/terms
"""
        embed = discord.Embed(
            title="__***:fire:!  Discord Bot Rules  !***__", description=data, color=0x00ff00)
        await ctx.send(embed=embed)
        data = """
- Do not queue NSFW noises, ear rape or disturb others in any way in voice channels. 

- Playing songs through your mic will result in a mute. 

- No bullying in any form. 

- Do not use a voice changer or text - to - speech software. 

- Do not use words that will spark controversy.  Racial slurs will be treated very seriously.

- Please make sure you notify everyone that you intend to record the conversation and wait for everyone's assent before you do so. 

- Do not argue with Administrators or Moderators about the rules.
"""
        embed = discord.Embed(
            title="__***:fire:!        Voice      !***__", description=data, color=0x00ff00)
        await ctx.send(embed=embed)


bot.remove_command("help")
bot.load_extension('cogs.botEvent')
bot.load_extension('cogs.botHelp')
bot.load_extension('cogs.botSelf')
bot.load_extension('cogs.botCMD')
bot.load_extension('cogs.botWelcome')

# SAKURA
bot.run(os.getenv("KEY"))
