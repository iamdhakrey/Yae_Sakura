from discord.embeds import Embed
from discord.ext import commands
import asyncio
import discord
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from discord.ext.commands import has_permissions
import requests,random,os,json
from discord.ext.commands import bot
import re
import misc


PREFIX_FILE_NAME = "prefix.json"
ROOT_JSON_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir)+'/json' # os.path.dirname(os.path.realpath(__file__))
PREFIX_FILE_PATH = os.path.join(ROOT_JSON_PATH,PREFIX_FILE_NAME)

class BotCMD(commands.Cog):
    """
    List of Various Commands
    """
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=["av"])
    async def avatar(self,ctx, *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        user = user or ctx.author
        embed = discord.Embed(title="Avatar")
        embed.set_author(icon_url=user.avatar_url,name=user)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)
        # await ctx.send(f"Avatar to **{user.name}**\n{user.avatar_url_as(size=1024)}")

    @commands.command(aliases=["purge","clean"])
    @has_permissions(administrator=True)
    async def clear(self,ctx,amount: int):
        """
        Delete Messages 
        """
        await ctx.channel.purge(limit=amount)


    @commands.command()
    async def ping(self,ctx):
        """
        Check Bot Ping
        """
        ping = round(self.bot.latency,2)
        data = "Pong 🟢 {}ms ".format(ping)
        # print(data)
        embed = discord.Embed(title=None, description=data, color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(aliases=["an"])
    @has_permissions(administrator=True)
    async def announcement(self,ctx,*,msg):
        """
        Send an announcements msg
        """
        # if int(ctx.author.id) == 540631315561840640 or int(ctx.author.id) == 500286166180954114:
         # print(msg)
        msg = str(msg).split(':')
        # print(msg)
        new_msg = []
        for i in msg:
            if i == '':
                pass
            else:
                # print(discord.utils.get(ctx.guild.emojis,name=i))
                if discord.utils.get(ctx.guild.emojis,name=i):
                    emoji = discord.utils.get(ctx.guild.emojis,name=i)
                    # print(emoji)
                    new_msg.append(str(emoji))
                else:
                    new_msg.append(str(i))
        # print(new_msg)
        data = new_msg
        # await ctx.send(new_msg)
        embed = discord.Embed(title=None, description="".join(new_msg), color=0x00ff00)
            # print(data)
        await ctx.send(embed=embed)
        await ctx.message.delete() 
    
    @announcement.error
    async def an_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("No Message is given")
    
    @commands.command()
    @has_permissions(administrator=True)
    async def image(self,ctx,msg):
        """
        `Send Embed Image` 
        """
        embed = discord.Embed(color=0x00ff00) 
        embed.set_image(url=msg)
        await ctx.send(embed=embed)

    @commands.command()
    @has_permissions(administrator=True)
    async def change_prefix(self,ctx,prefix):
        """
        Set The Server Prefix
        """
        try:
            if str(prefix).split(","):
                prefix = str(prefix).split(",")
                for pre in prefix:
                    if pre.isdigit():
                        await ctx.send("number prefix are not support for now")
                        return
                    try:
                        for i in pre:
                            if i.isdigit():
                                await ctx.send("number prefix are not support for now")
                                return
                            if i.startswith('[') or i.endswith("]"): 
                                await ctx.send("Bro, check help cmd for change_prefix")
                                return    
                    except:
                        pass
                        # await ctx.send("number prefix are not support for now")
                        # return
        except:
            print(prefix)
            # return 
        with open(PREFIX_FILE_PATH,'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix

        with open(PREFIX_FILE_PATH,'w') as f:
            json.dump(prefixes,f,indent=4)

        await ctx.send("The Prefix in changed to {}".format(prefix))
    
    @change_prefix.error
    async def change_prefix_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("prefix is a required argument that is missing.")

    @commands.command(aliases=["get_prefix"])
    async def show_prefix(self,ctx,*,msg=None):
        """
        Show The Sets Prefix to The Server
        """
        data = misc.return_data(str(ctx.guild.id),PREFIX_FILE_PATH)
        guild = ctx.guild.id
        try:
            if type(data) == type(str("d")):
                await ctx.reply("The prefix for the {} is '' **{}** ''".format(ctx.guild.name,data))
            else:
                pre = ",".join(data)
                # pre = " "
                # for i in data:
                #     pre = i + " ," + pre
                await ctx.reply("The prefixes for the {} is '' **{}** ''".format(str(ctx.guild.name),pre))
        except Exception as e:
            print(e)

    # @commands.command()
    # async def count(self,ctx):
    #     await ctx.send(ctx.guild.member_count)

def setup(bot):
    bot.add_cog(BotCMD(bot))