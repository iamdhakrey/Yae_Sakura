import discord
from discord import colour
from discord.ext import commands
import os

import help
import misc

# cmd_help = help.Help()
PREFIX_FILE_NAME = "prefix.json"
ROOT_JSON_PATH = os.path.normpath(os.path.realpath(__file__)+os.sep + os.pardir + os.sep + os.pardir)+'/json' # os.path.dirname(os.path.realpath(__file__))
PREFIX_FILE_PATH = os.path.join(ROOT_JSON_PATH,PREFIX_FILE_NAME)

class botHelp(commands.Cog):
    """
    Know how to use me
    """
    def __init__(self,bot) -> None:
        self.bot = bot
        super().__init__()
    
    @commands.command()
    async def hl(self,ctx,*cmd):
        """Send bot help msg
    Args:
        {prefix} help command
        """

        # print(misc.return_data(str(ctx.guild.name),PREFIX_FILE_PATH))
        prefix_data = misc.return_data(str(ctx.guild.id),PREFIX_FILE_PATH)

        prefixes = ",".join(prefix_data)
        # for i in prefix_data:
            # prefixes  = i + ","+prefixes

        if len(prefix_data) < 2:
            prefix = prefix_data
        else:
            prefix = prefix_data[1]

        embed = discord.Embed(color = ctx.author.color,description="Use `{0}help <commands or modules>` to know what I do ".format(prefix))
        embed.set_author(icon_url=self.bot.user.avatar_url,name = self.bot.user)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        
        if not cmd: 
            

            embed.add_field(name="Prefixes",value="Current Prefixes for {0} is `{1}`".format(str(ctx.guild.name),prefixes),inline=False)
        
            cogs_description = ""
            for cog in self.bot.cogs:
                # print(str(cog))
                if "BotEvent" in str(cog):
                    pass
                else:
                # cogs_description += "`{0}` {1}\n".format(cog,self.bot.cogs[cog].__doc__) 

                    embed.add_field(name=cog,value=self.bot.cogs[cog].__doc__,inline=True)

        elif len(cmd) == 1 :
            for cog in self.bot.cogs:
                # print(cog.lower())
                # print(cmd[0].lower())
                if cmd[0].lower() == cog.lower():
                    embed.add_field(
                        name="{0} - Commands ".format(cog),
                        value=self.bot.cogs[cog].__doc__,
                        inline=False
                    )

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            embed.add_field(
                                name="`{0}{1}`".format(prefix,command.name),
                                value=command.help,
                                inline = True
                            )
                    break

            for cog in self.bot.cogs:
                for commands in self.bot.get_cog(cog).get_commands():
                    # print(commands,cmd)
                    if cmd[0].lower() ==str(commands).lower():
                        embed.add_field(
                            name="`{0}{1} `".format(prefix,cmd[0]),
                            value=help.return_help(str(cmd[0]))
                        ) 
                # break
                    # embed = discord.Embed(title="{}")

        # footer 
        embed.add_field(name="Join Our Community For More Help",value="[Community](https://discord.gg/SgV5yhzy)",inline=False)
        # embed.set_footer(text="https://discord.gg/SgV5yhzy",)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(botHelp(bot))

