import os
from random import randint, random
from random import choice
from time import time
from io import BytesIO
import PIL
from PIL import Image, UnidentifiedImageError
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont
from discord import channel, colour, guild
from discord.ext import commands
from discord.ext.commands import has_permissions
import discord
import json
import requests
import re
import shutil


from discord.utils import MAX_ASYNCIO_SECONDS

import misc

WELCOME_FILE_NAME = "welcome.json"
ROOT_JSON_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir)+'/json' # os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir) # os.path.dirname(os.path.realpath(__file__))
WELCOME_FILE_PATH = os.path.join(ROOT_JSON_PATH,WELCOME_FILE_NAME)


# class MemberRoles():
#     def check_role
class botWelcome(commands.Cog):
    """
    List of Welcome Commands
    """
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()
    
    @commands.command(aliases=['swm','set_welcome'])
    @has_permissions(administrator=True)
    async def set_welcome_message(self,ctx,set_channel : discord.TextChannel = None,*,msg=None):
        """
        Set Welcome Message
        """
        if msg is None:
            msg =""

        msg = str(msg).split(':')

        #new welcome msg store in new_msg
        new_msg = []
        # print(msg)
        for i in msg:
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

        #replace new line 
        for i in new_msg:
            wel = wel + i 
        wel = wel.replace('\n',"\n\ncers").split("\ncers")

        # roles = None

        # server_id
        guild_id = ctx.guild.id

        # check author is server owner or not
        # if ctx.guild.owner_id != ctx.author.id:
            # await ctx.send("Bro you are not owner of this server so you cant set welcome msg")

        # get Welcome data for the server 
        data = misc.return_data(str(guild_id),WELCOME_FILE_PATH)
        
        # Check welcome channel exist or not
        if discord.utils.get(self.bot.get_all_channels(),guild__name= ctx.guild.name,id=set_channel.id):
            channel_id = set_channel.id
        else:
            #get welcome channel
            channel_id = data["welcome_channel"]

        # if self_role
        with open(WELCOME_FILE_PATH,'r') as f:
            msg_data = json.load(f)
        msg_data[str(ctx.guild.id)]["welcome_channel"] = channel_id
        msg_data[str(ctx.guild.id)]["welcome_msg"] = wel
        with open(WELCOME_FILE_PATH,'w') as f:
            json.dump(msg_data,f,indent=4)
        
        await ctx.send("welcome msg set successfully")

    @set_welcome_message.error
    async def swm_error(self,ctx,error):
        # if msg is not given
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Welcome Msg Requierd")
        # Role  not Found
        if isinstance(error,commands.RoleNotFound):
            await ctx.send(error)

        #channel not Found
        if isinstance(error,commands.ChannelNotFound):
            await ctx.send(error)
        # print(error)

    @commands.command(aliases=['set_join_role','join_role'])
    @has_permissions(administrator=True)
    async def set_join_self(self,ctx,role: discord.Role):
        """
        Set Role When member Join
        """
        guild_data = {}
        data = misc.return_data(str(ctx.guild.id),WELCOME_FILE_PATH)
        #guild Data
        guild_data[str(ctx.guild.id)] = data 
        
        
        if discord.utils.get(ctx.guild.roles,id=role.id):
            guild_data[str(ctx.guild.id)]["self_role"] = role.id
            misc.write_data(guild_data,WELCOME_FILE_PATH)     
        else:
            await ctx.send("{} Role Not Found".format(role))

    @set_join_self.error
    async def set_self_error(self,ctx,error):
        if isinstance(error,commands.RoleNotFound):
            await ctx.send(error)
        # await ctx.send(error)

    @commands.command(aliases=["gw"])
    @has_permissions(administrator=True)
    async def get_welcome(self,ctx):
        """
        Get Welcome Message status
        """
        data  = misc.return_data(str(ctx.guild.id),WELCOME_FILE_PATH)
        role = discord.utils.get(ctx.guild.roles,id=data["self_role"])
        # print(role )
        w_channel = discord.utils.get(ctx.guild.channels,id=data["welcome_channel"])
        welcome_msg = data["welcome_msg"]
        args = data['args']
        # w_channel = data['welcome_channel']
        enable = data['enable']
        # for arg in args:
            # welcome_msg = welcome_msg.replace("{}","{"+arg+"}").replace("\n","")

        w_data = dict(
            enable = enable,
            welcome_msg = welcome_msg,
            welcome_channel = w_channel,
            self_role = role,
        )
        # print(type(welcome_msg),welcome_msg)
        # welcome_msg = ["fsdf \n\n","\nfsgegs"]
        # await ctx.send(welcome_msg)
        embed = discord.Embed(
            title = "Welcome msg",
            colour = 0x00ff00,
            description= "".join(welcome_msg)
        )
        # print(welcome_msg)
        # embed.set_image(url='attachment://tmpBv.png')
        # file = discord.File(open('tmpBv.png', 'rb'))

        embed.add_field(name="is_enable",value=enable,inline=False)
        # embed.add_field(name="welcome_message",value="".join(welcome_msg),inline=True)
        embed.add_field(name="welcome_channel",value=w_channel,inline=True)
        embed.add_field(name="self_role",value=role,inline=False)
        await ctx.send(embed=embed)
        # await ctx.send(w_data)

    @commands.command(aliases=["cw"])
    @has_permissions(administrator=True)
    async def check_welcome(self,ctx,*,msg):
        """
        Check Welcome Msg how it look then you set
        """
        new_msg = []
        msg = str(msg).split(':')
        # print(msg)
        for i in msg:
            if i == '':
                pass
            else:
                # print(discord.utils.get(ctx.guild.emojis,name=i))
                if discord.utils.get(ctx.guild.emojis,name=i):
                    emoji = discord.utils.get(ctx.guild.emojis,name=i)
                    new_msg.append(str(emoji))
                else:
                    new_msg.append(str(i))
                # print(new_msg)
        wel = ""
        for i in new_msg:
            wel = wel + i 
        embed = discord.Embed(
            description = wel,

        )
        # print(wel)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["we"])
    @has_permissions(administrator=True)
    async def welcome_enable(self,ctx,status):
        """
        Enable/Disable welcome msg
        """
        guild_data = {}
        data = misc.return_data(str(ctx.guild.id),WELCOME_FILE_PATH)
        if str(status) == "on" or str(status) == "ON" or str(status) == "enable":
            data['enable'] = True
            # print(status)
        elif str(status) == "off" or str(status) == "OFF" or str(status) == "disable":
            data['enable'] = False
        
        else:
            await ctx.reply("Bro use on/off or enable/disable ") 
            return   # print(status+"1")
        # print(data)
        guild_data[str(ctx.guild.id)] = data
        misc.write_data(guild_data,WELCOME_FILE_PATH)
        await ctx.reply("welcome status is set to  {}".format(status))

    @welcome_enable.error
    async def welcome_enable_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.reply("use on/off or enable/disable")


    @commands.command(aliases=["welcome_image","swi"])
    @has_permissions(administrator=True)
    async def set_welcome_image(self,ctx,*,images_link):
        """
        Set Welcome Image
        """
        _image_list = images_link.split(" ")
        if len(_image_list) > 10:
            ctx.reply("No More 10 Images")
            return
        i = 0
        guild_data = {}
        image_name = []
        for link in _image_list:
            i = i + 1
            url = requests.get(link)
            background = Image.open(BytesIO(url.content))
            width,height = background.size
            if width <= 1920 and height <= 972:
                await ctx.send("minimum 1920*972 resolution required")
                return
            background = background.resize((1920,972))
            output = ImageOps.fit(background,background.size,centering=(0.5,0.5))
            output.save("images/backgrounds/"+str(ctx.guild.id)+"_"+str(i)+".jpg")
            image_name.append(str(ctx.guild.id)+"_"+str(i)+".jpg")
        data =  misc.return_data(str(ctx.guild.id),WELCOME_FILE_PATH)
        image_data = data['welcome_images']
        if len(image_data) >10:
            ctx.reply("No More 10 Images")
        data["last_update"] = str(ctx.auther.id)
        guild_data[str(ctx.guild.id)] = data
        misc.write_data(str(ctx.guild.id),WELCOME_FILE_PATH)
        await ctx.send("backgrounds images set successfully")

    @set_welcome_image.error
    async def set_welcome_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.reply("Image link requie")
        if isinstance(error,UnidentifiedImageError):
            await ctx.reply("Bro send the current image link")
        if isinstance(error,commands.CommandInvokeError):
            await ctx.reply("Invalid URL")
    #     print(error)

    @commands.command(aliases=["tw"])
    @has_permissions(administrator=True)
    async def test_welcome(self,ctx):
        """
        Send Original Set Msg
        """
        member_id = ctx.author.id
        member_name = ctx.author.name +"#"+ctx.author.discriminator
        member_tag = "<@"+str(member_id)+">"

        data  = misc.return_data(str(ctx.guild.id),WELCOME_FILE_PATH)
        role = discord.utils.get(ctx.guild.roles,id=data["self_role"])
        # print(role )
        w_channel = discord.utils.get(ctx.guild.channels,id=data["welcome_channel"])
        welcome_msg = data["welcome_msg"]
        server_name = data["server_name"]
        # print(server_name)
        args = data['args']
        # w_channel = data['welcome_channel']
        enable = data['enable']
        # for arg in args:
            # welcome_msg = welcome_msg.replace("{}","{"+arg+"}").replace("\n","")

        w_data = dict(
            enable = enable,
            welcome_msg = welcome_msg,
            welcome_channel = w_channel,
            self_role = role,
        )
        # print(type(welcome_msg),welcome_msg)
        # welcome_msg = ["fsdf \n\n","\nfsgegs"]
        # await ctx.send(welcome_msg)
        test = []
        for i in welcome_msg:
            # tags = re.findall("{{(.*)}}")
            wlmsg = i
            if "member.mention" in i:
                wlmsg = str(i).replace("{"+"member.mention"+"}",member_tag)
                # test.append(wlmsg)
            if "member.name" in i:
                wlmsg = str(i).replace("{"+"member.name"+"}",member_name)
                # test.append(wlmsg)
            if "member.count" in i:
                wlmsg = str(i).replace("{"+"member.count"+"}",str(ctx.guild.member_count))
                # test.append(wlmsg)
            if "member.server_name" in i:
                wlmsg = str(i).replace("{"+"member.server_name"+"}",str(ctx.guild.name))
                # test.append(wlmsg)
            if "member.role" in i:
                wlmsg = str(i).replace("{"+"member.role"+"}",str(role.mention))
                # test.append(wlmsg)
            test.append(wlmsg)
            # else:
                # test.append(i)
        # if os.path.isfile(os.path.join(ROOT_PATH,"images/backgrounds/"+str(ctx.guild.id)+"_1.jpg")):
        #     is_w_images = True
        # else:
        embed = discord.Embed(
        #     # title = "Welcome msg",
            colour = 0x00ff00,
            # description= "".join(welcome_msg)
        )
        is_w_images = False
        count_list = []
        for i in range(10):
            if os.path.isfile(os.path.join(ROOT_PATH,"images/backgrounds/"+str(ctx.guild.id)+"_"+str(i)+".jpg")):
                is_w_images = True
                count_list.append(i)
            else:
                pass
        # print(count_list)
        try:
            image_num = choice(count_list)
            # print(image_num,is_w_images)
        except:
            image_num = randint(1,10)

        W,H = 1920,872
        # messeges
        hello = "Hey Buddy,"
        username = str(self.bot.get_user(ctx.author.id))
        msg = 'You Are {}th Member of The Server'.format(ctx.guild.member_count)

        url = requests.get(ctx.author.avatar_url)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((380, 380))
        bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size)
        avatar.putalpha(mask)
        output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save('images/avatar.png')
        ava = Image.open('images/avatar.png')
        ava_draw = ImageDraw.Draw(ava)
        ava_draw.arc((0, 0, 380, 380), start=0, end=360, fill=(194,83,111),width=12)
        ava.save("images/avatar.png")

        if is_w_images:
            welc = Image.open( 'images/backgrounds/'+str(ctx.guild.id)+"_"+str(image_num)+'.jpg' )

        else:
            welc = Image.open( 'images/backgrounds/welcome'+str(image_num)+'.jpg' )
        font1 = ImageFont.truetype('fonts/UbuntuMono-B.ttf', 90)
        font2 = ImageFont.truetype('fonts/Caveat-Bold.ttf', 100)

        welc_draw = ImageDraw.Draw(welc)
        hello_w,hello_h = welc_draw.textsize(hello,font2)
        user_w,user_h = welc_draw.textsize(username,font1)
        msg_w,msg_h = welc_draw.textsize(msg,font2)
        welc_draw.text(xy=((W-hello_w)/2,(H-hello_h)/1.44), text=hello, fill=(190,222,203), font=font2,align='center')
        welc_draw.text(xy=((W-user_w)/2,(H-user_h)/1.2), text=username, fill=(222,239,90), font=font1,align='center')
        welc_draw.text(xy=((W-msg_w)/2,(H-msg_h)/1), text=msg, fill=(248,206,160), font=font2,align = 'center')
        welc.paste(ava, (760, 150), ava)

        welc.save('tmpBv.png', format='PNG')
        # print(test)
        embed = discord.Embed(
            # title = "Welcome msg",
            colour = 0x00ff00,
            description= "".join(test)
        )
        file = discord.File(open("tmpBv.png", 'rb'))
        embed.set_image(url='attachment://tmpBv.png')
        await ctx.send(embed=embed,file=file)

def setup(bot):
    bot.add_cog(botWelcome(bot))

