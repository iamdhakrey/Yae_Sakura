import time
from discord import channel, colour, emoji, member, message
from discord.ext import commands
import asyncio
import discord
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import requests,random,os, json
import misc
from discord.ext.commands import bot


PREFIX_FILE_NAME = "prefix.json"
WELCOME_FILE_NAME = "welcome.json"
ROLE_FILE_NAME = "self_role.json"

ROOT_JSON_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir)+'/json' # os.path.dirname(os.path.realpath(__file__))
PREFIX_FILE_PATH = os.path.join(ROOT_JSON_PATH,PREFIX_FILE_NAME)
ROOT_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir) # os.path.dirname(os.path.realpath(__file__))
WELCOME_FILE_PATH = os.path.join(ROOT_JSON_PATH,WELCOME_FILE_NAME)
ROLE_FILE_PATH=os.path.join(ROOT_JSON_PATH,ROLE_FILE_NAME)

class BotSelf(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['ssm'])
    async def set_self_message(self,ctx,unique,channel : discord.TextChannel = None ,*,msg):
        """
        Age
        Are You An Adult or a Kid? React with :boy: for Kid and :man: for Adult
        """
        # #channel  unique title | desc | emoji & role | emoji & role

        #breakpoint |

        if unique == "yes" or unique == 'Yes' or unique == 'YES':
            unique = unique
        elif unique == 'no' or unique == 'No' or unique == 'NO':
            unique = None 

        else:
            msg = unique + " " + msg
            unique = None
        
        split_msg = str(msg).split("|")

        msg = str(msg).split(':')

        #new welcome msg store in new_msg
      
        # grep title and description
        title = split_msg.pop(0)
        desc =  split_msg.pop(0)

        new_msg = []
        # print(msg)
        for i in desc.split(":"):
            if i == '':
                pass
            else:
                # check emoji or not if not that means msg 
                if discord.utils.get(ctx.guild.emojis,name=i):
                    emoji = discord.utils.get(ctx.guild.emojis,name=i)
                    new_msg.append(str(emoji))
                else:
                    new_msg.append(str(i))
        wel = ""
        for i in new_msg:
            wel = wel + i 
        
        # print(wel)
        # store emoji with role
        emoji_role_dict = {}

        # all emoji in this list
        emoji_list = []

        # insert emoji and role in dict
        for em_and_role in split_msg:
            em_and_role = em_and_role.split("%")
            emoji_list.append(em_and_role[0].strip())
            emoji_role_dict[em_and_role[0].strip()] = em_and_role[1].strip()
        
        # print(emoji_role_dict)
        send_emb = discord.Embed(
            title=title,
            description = wel,
            color = 0x00ff00
        )
        send_emb.set_thumbnail(url=ctx.guild.icon_url)
        send_msg = await channel.send(embed=send_emb)
        channel_id = channel.id
        for i in emoji_list:
            try:
                if discord.utils.get(ctx.guild.emojis,name=str(i).replace(":",'')):
                    i = discord.utils.get(ctx.guild.emojis,name=str(i).replace(":",''))
            except:
                if discord.utils.get(ctx.guild.emojis,name=i):
                    i = discord.utils.get(ctx.guild.emojis,name=i)
            await send_msg.add_reaction(i)
        mes_list = []
        self_role_list = []
        data = None
        if misc.return_data(str(ctx.guild.id),ROLE_FILE_PATH):
            data = misc.return_data(str(ctx.guild.id),ROLE_FILE_PATH)
            mes_list = data["message_id"]
            # self_role_list = data["self_role_list"]
        mes_list.append(send_msg.id)
        """format {
        guild_id  : {
            messeage_id :{
                reactionrole:{
                },
                unique: yes
            }
        }"""
        guild_data = {}
        data2 = {
                "message_id": mes_list,
                str(send_msg.id):{
                "reactionrole":emoji_role_dict,
                "unique": unique
            }
        }
        if data:
            guild_data[str(ctx.guild.id)] = {**data, **data2}
        else:
            # print("fdsg")
            guild_data[str(ctx.guild.id)] = {**data2}
        if misc.write_data(guild_data,ROLE_FILE_PATH):
            ctx.reply("role set successfully")

def setup(bot):
    bot.add_cog(BotSelf(bot))