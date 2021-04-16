
import time
from discord import channel, client, member
from discord.errors import HTTPException
from discord.ext import commands
import asyncio
import discord
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from discord.utils import _unique, parse_time, sleep_until
import requests,random,os,json
import misc
from discord.ext.commands import bot
import random


PREFIX_FILE_NAME = "prefix.json"
WELCOME_FILE_NAME = "welcome.json"
ROLE_FILE_NAME  = "self_role.json"
MEMBER_ROLE_FILE_NAME = "memberoles.json"

ROOT_JSON_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir)+'/json' # os.path.dirname(os.path.realpath(__file__))
PREFIX_FILE_PATH = os.path.join(ROOT_JSON_PATH,PREFIX_FILE_NAME)
ROOT_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir) # os.path.dirname(os.path.realpath(__file__))
WELCOME_FILE_PATH = os.path.join(ROOT_JSON_PATH,WELCOME_FILE_NAME)
ROLE_FILE_PATH = os.path.join(ROOT_JSON_PATH,ROLE_FILE_NAME)
MEMBER_ROLE_FILE_PATH = os.path.join(ROOT_JSON_PATH,MEMBER_ROLE_FILE_NAME)


hi_set = [' Bol BC '," Tu Fir AA Gya ",' Kesa h re tu ',' Nikl L**** '," or Bta "," Ae Tu Ja Reee! "]
class BotEvent(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    async def status_change(self):
        while True:
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Sponsored by Unload",type=discord.ActivityType.listening))
            await asyncio.sleep(20)
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Suggested by Verma",type=discord.ActivityType.listening))
            await asyncio.sleep(20)
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Created by Dhakrey",type=discord.ActivityType.listening))
            await asyncio.sleep(20)

    # @bot.event
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.status_change())
        # check_status()
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')
    
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        
        # send msg when sakura join in new server
        send_log = discord.Embed(
            title = "Joined",
            description = "Sakura is added on **{0}** Server".format(str(guild.name)),
            color = 0x00ff00
        )

        send_log.set_thumbnail(url=guild.icon_url)
        send_log.add_field(
            name="server id",
            value="{0}".format(guild.id)
        )

        send_log.add_field(
            name="Owner Name",
            value="{0}".format(guild.owner)
        )
        
        send_log.add_field(
            name="Owner Id",
            value="{0}".format(guild.owner_id)
        )

        sakura_log_channel = self.bot.get_channel(825386231537336371)
        # print(sakura_log_channel)
        await sakura_log_channel.send(embed=send_log)
        # prefix set 
        with open(PREFIX_FILE_PATH,'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = eval(str(["y","Y"]))

        # prefixes = eval(str(prefixes))
        # print(json.dumps(prefixes,indent=4))
        with open(PREFIX_FILE_PATH,'w') as f:
            json.dump(prefixes,f,indent=4)
        # print("Default prefix in set for server {} , {}".format(str(guild.id),str(guild.name)))
        # welcome msg set
        with open(WELCOME_FILE_PATH,'r') as f:
            msg_data = json.load(f)
        # print(check_exist(str(guild.id),WELCOME_FILE_PATH))
        if misc.check_exist(str(guild.id),WELCOME_FILE_PATH) == False:
            msg_data[str(guild.id)]= dict(
                active = True,
                enable = False,
                welcome_msg = str("""hey {} \n Welcome to the {} Server \n you are the {}th member of the server"""),
                args = ["member.mention","member.guild.name","member.guild.member_count"],
                self_role = None,
                welcome_images = ["welcome1.jpg","welcome2.jpg","welcome3.jpg","welcome4.jpg","welcome5.jpg","welcome6.jpg","welcome7.jpg","welcome8.jpg","welcome9.jpg","welcome10.jpg"],
                welcome_channel =  None,
                server_name = str(guild.name),
                owner_id = str(guild.owner_id),
                last_update = "Yae Sakura"
            )
        # print(json.dumps(msg_data,indent=4,ensure_ascii=False))
        with open(WELCOME_FILE_PATH,'w') as f:
            json.dump(msg_data,f,indent=4)
        # print("default welcome msg set for {}".format(str(guild.name)))

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):

        send_log = discord.Embed(
            title = "Remove",
            description = "Sakura was removed on **{0}**".format(str(guild.name)),
            color = 0xff0000
        )

        send_log.set_thumbnail(url=guild.icon_url)
        send_log.add_field(
            name="server id",
            value="{0}".format(guild.id)
        )

        send_log.add_field(
            name="Owner Name",
            value="{0}".format(guild.owner)
        )
        
        send_log.add_field(
            name="Owner Id",
            value="{0}".format(guild.owner_id)
        )

        sakura_log_channel = self.bot.get_channel(825386231537336371)

        await sakura_log_channel.send(embed=send_log)

        with open(PREFIX_FILE_PATH,'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open(PREFIX_FILE_PATH,'w') as f:
            json.dump(prefixes,f,indent=4)

    @commands.Cog.listener()
    async def on_message(self,msg):
        if (msg.content.startswith("hi") or msg.content.startswith("Hi") or msg.content.startswith("HI")) and len(msg.content)==2:
            channel = msg.channel
            _num = random.randint(0,5)
            # for i in msg.author.roles:
            #     print(i.id,i.name)
            await channel.send("{}".format(msg.author.mention)+str(hi_set[_num]))
            pass
    # @bot.event
    
    @commands.Cog.listener()
    async def on_member_join(self,member):

        member_id = member.id
        member_name = member.name
        member_tag = "<@"+str(member_id)+">"
        data  = misc.return_data(str(member.guild.id),WELCOME_FILE_PATH)
        role = discord.utils.get(member.guild.roles,id=data["self_role"])
        w_channel = discord.utils.get(member.guild.channels,id=data["welcome_channel"])

        welcome_msg = data["welcome_msg"]

        is_w_images = False
        count_list = []
        for i in range(10):
            if os.path.isfile(os.path.join(ROOT_PATH,"images/backgrounds/"+str(member.guild.id)+"_"+str(i)+".jpg")):
                is_w_images = True
                count_list.append(i)
            else:
                pass
        try:
            image_num = random.choice(count_list)
        except:
            image_num = random.randint(1,10)

        W,H = 1920,872
        # messeges
        hello = "Hey Buddy,"
        username = str(self.bot.get_user(member.id))
        msg = 'You Are {}th Member of The Server'.format(member.guild.member_count)

        url = requests.get(member.avatar_url)
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
        # avatar = Image.open('avatar2.png')
        if is_w_images:
            welc = Image.open( 'images/backgrounds/'+str(member.guild.id)+"_"+str(image_num)+'.jpg' )

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
        test = []
        for i in welcome_msg:
            wlmsg = i
            if "member.mention" in i:
                wlmsg = str(i).replace("{"+"member.mention"+"}",str(member_tag))
            if "member.name" in i:
                wlmsg = str(i).replace("{"+"member.name"+"}",str(member_name))
            if "member.count" in i:
                wlmsg = str(i).replace("{"+"member.count"+"}",str(member.guild.member_count))
            if "member.server_name" in i:
                wlmsg = str(i).replace("{"+"member.server_name"+"}",str(member.guild.name))
            if "member.role" in i:
                wlmsg = str(i).replace("{"+"member.role"+"}",str(role))
            else:
                test.append(wlmsg)
        welc.save('tmpBv.png', format='PNG')
        # bot.
        if role:
            await member.add_roles(role)
        file = discord.File(open('tmpBv.png', 'rb'))
        # embed = discord.Embed(title=':r_arrow: Hey buddy {}'.format(str(member)), description='welcome to the  {}! you are  {}th member of no server.'.format(member.guild.name, member.guild.member_count), color=0x1f1d1d) 
        embed = discord.Embed(description=''.join(test), color=0x00ff00) 
        # embed.set_thumbnail(url = member.guild.icon_url)
        embed.set_image(url='attachment://tmpBv.png')
        await w_channel.send(file=file ,embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        reaction = str(payload.emoji)
        msg_id = payload.message_id
        ch_id = payload.channel_id
        username = payload.member
        user_id = payload.user_id
        guild_id = payload.guild_id
        
        """
        {
            guild.id : {
                member_list : [],
                member_id : []
                }
            }
        }
        """
        print(reaction)
        data = misc.return_data(str(guild_id),ROLE_FILE_PATH)

        if msg_id not in data["message_id"]:
            return

        # {
        #     member_list : [],
        #     member_id : []
        # }
        member_rols = []
        member_id_list =[]
        member_data = misc.return_data(str(guild_id),MEMBER_ROLE_FILE_PATH)
        print(member_data)
        try:
            member_id_list = member_data['member_list']
            try:
                if str(user_id) in member_data["member_list"]:
                    member_rols = member_data[str(user_id)]
                else:
                    member_id_list.append(str(user_id))
                    pass
            except:
                pass
        except TypeError:
            member_id_list.append(str(user_id))
            pass
        
        print(member_rols,"roles")

        # if isinstance(unique,int):


        unique = "no"
        get_data  = data[str(msg_id)]

        unique_status = get_data['unique']

        print(isinstance(unique_status,int))
        get_str = False
        if isinstance(unique_status,int):
            unique = unique_status
        else:
            get_str = True
            if str(unique_status).lower() == "yes":
                unique = 'yes'
        
        
        # if isinstance()
        emoji_role_dict = get_data["reactionrole"]
        channel = discord.utils.get(payload.member.guild.channels,id = ch_id)
        member =  await payload.member.guild.fetch_member(user_id)
        
        dis_msg = await channel.fetch_message(int(msg_id))
        self_role_list = []
        member_rol_list = []
        for key,value in emoji_role_dict.items():
            self_role_list.append(int(str(value).replace("<@&","").replace(">",'')))
            try:
                if discord.utils.get(payload.member.guild.emojis,name=str(key).replace(":",'')):
                    key = discord.utils.get(payload.member.guild.emojis,name=str(key).replace(":",''))
            except:
                if discord.utils.get(payload.member.guild.emojis,name=key):
                    key = discord.utils.get(payload.member.guild.emojis,name=key)
            if str(key) == (reaction):
                
                member =  await payload.member.guild.fetch_member(user_id)
                role = payload.member.guild.get_role(int(str(value).replace("<@&",'').replace(">",'')))
                await member.add_roles(role)
                member_rols.append(str(role.id))
                write = {}
                
                # write[str(guild_id)] = {
                try:
                    temp_data  = {
                        "member_list": member_id_list,
                        str(user_id) : member_rols
                    }
                    member_data.update(temp_data)
                except:
                    member_data = {
                            "member_list": member_id_list,
                            str(user_id) : member_rols
                        }
                write[str(guild_id)] = member_data
                misc.write_data(write,MEMBER_ROLE_FILE_PATH)
                channel = discord.utils.get(payload.member.guild.channels,id = ch_id)

            else:
                if get_str:
                    if unique.lower() == "yes":
                        await dis_msg.remove_reaction(key,member)

        member =  await payload.member.guild.fetch_member(user_id)

        # try:    
        if int(unique) < len(member_rols):
            ran_num = random.randint(0,(len(member_rols)-1))
            # ran_num = 0
            print(ran_num)
            _reaction = str(list(emoji_role_dict.keys())[ran_num]).strip()
            print(_reaction)
            print((str(emoji_role_dict[_reaction]).replace("<@&",'').replace(">",'')))
            role = payload.member.guild.get_role(int(str(emoji_role_dict[_reaction]).replace("<@&",'').replace(">",'')))
            print(role,role.id)
            member_rols.remove(str(role.id))
            write = {}
            write[str(guild_id)] = {
                    "member_list": member_id_list,
                    str(user_id) : member_rols
                }
            misc.write_data(write,MEMBER_ROLE_FILE_PATH)
            print(discord.utils.get(payload.member.guild.emojis,name=str(_reaction).replace(":",'')))
            if discord.utils.get(payload.member.guild.emojis,name=str(_reaction).replace(":",'')):
                key = discord.utils.get(payload.member.guild.emojis,name=str(_reaction).replace(":",''))
            else:
                print("exce")
                # if discord.utils.get(payload.member.guild.emojis,name=_reaction):
                    # key = discord.utils.get(payload.member.guild.emojis,name=_reaction)
                key = _reaction
            
            print(key)
            await dis_msg.remove_reaction(key,member)
        

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        reaction = str(payload.emoji)
        msg_id = payload.message_id
        user_id = payload.user_id
        guild_id = payload.guild_id
        
        guild_name = self.bot.get_guild(guild_id)

        member_name = guild_name.get_member(user_id)
        data = misc.return_data(str(guild_id),ROLE_FILE_PATH)

        if msg_id not in data["message_id"]:
            return
        get_data  = data[str(msg_id)]
        emoji_role_dict = get_data["reactionrole"]
        for key,value in emoji_role_dict.items():
            try:
                if discord.utils.get(guild_name.emojis,name=str(key).replace(":",'')):
                    key = discord.utils.get(guild_name.emojis,name=str(key).replace(":",''))
            except:
                if discord.utils.get(guild_name.emojis,name=key):
                    key = discord.utils.get(guild_name.emojis,name=key)
            try:
                # ifreaction is in form of <:name:id>
                if str(key.id) == str(reaction.split(":")[2].replace(">",'')):
                    role = guild_name.get_role(int(str(value).replace("<@&",'').replace(">",'')))
                    await member_name.remove_roles(role)
            except:
                # if reaction is default emoji
                if str(key) == reaction:
                    role = guild_name.get_role(int(str(value).replace("<@&",'').replace(">",'')))
                    await member_name.remove_roles(role)


def setup(bot):
    bot.add_cog(BotEvent(bot))