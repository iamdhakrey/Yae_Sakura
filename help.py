class Help():
    def __init__(self) -> None:
        pass

    def avatar(self):
        return """
        Get your or Someone avatar

        Aliases:
            `['av']`

        Roles:
            `@everyone`

        Ex:
            `Yav`
            `Yav @Lunatian#3389`
        
        """

    def clear(self):
        return """
        Delete Messages 
        
        Aliases:
            `['clean','purge']`
            
        Roles:
            `Administrator`

        Ex:
            `Yclear 5`
        """

    def ping(self):
        return """
        Check My Health

        Aliases:
            `['status']`

        Roles:
            `@everyone`

        Ex:
            `Yping`
        """
        pass

    def announcement(self):
        return """
        Send an Announcement Message
        
        Aliases:
            `['an','send_announcement']`

        Roles:
            `Administrator`

        Ex:
            `Yannouncement Hi everyone`
        """

    def image(self):
        return """
        Send an Embed Image

        Aliases:
            `['send_embed_image','send_image']`
        
        Roles:
            `Administrator`

        Ex:
            `Yimage image_url`
        """


    def change_prefix(self):
        return """
        Set the Server Prefix

        Aliases:
            `['cp','update_prefix']`
        
        Roles:
            `Administrator`

        Ex:
            `Ychange_prefix !`
            `Ychange_prefix !,#`
        """

    def show_prefix(self):
        return """
        Show The Sets Prefix to The Server

        Aliases:
            `['sp']`

        Roles:
            `@everyone`

        Ex:
            `Yshow_prefix`
        """
    def set_welcome_message(self):
        return """
        Set Welcome Message

        Alieses:
            `['swm','set_welcome']`
        
        Roles:
            `Administrator`

        Command:
            `Yset_welcome_message channel_name welcome_msg`
        
        Ex:
            `Yset_welcome_message #welcome Hey buddy {member.mention} you are the {member.count}th member of the server`
        
        Extras:
            {member.mention} : mention member
            {member.name} : member username
            {member.count} : server member count
            {member.server_name} : server name
            {member.role} : member role

        Default:
            `Hey Buddy {member.mention},\n Welcome To The {member.server_name} Server \n You are the {member.count}th Member of The Server.`
        
        Note:
            `Before you set welcome msg pls first check welcome msg using **check_welcome** command then set welcome msg.`
        """

    def set_join_self(self):
        return """
        Set Role When Member Join in Server

        Aliases:
            `['set_join_role','join_role']`

        Roles:
            `Administrator`
        
        Ex:
            `Yset_join_self @ROLE`
        
        """

    def get_welcome(self):
        return """
        Get Welcome Message Status

        Roles:
            `Administrator`
        
        Ex:
            `Yget_welcome`
        
        Note:
            `It Will return **welcome msg, is_enable,welcome channel** and **join role**.` 
        """

    def check_welcome(self):
        return """
        Check Welcome Msg how it look then you set 
        
        Aliases:
            `['cw']`

        Roles:
            `Administrator`

        Ex:
            `Ycheck_welcome Hey buddy {member.mention} you are the {member.count}th member of the server`
        
        Extras:
            `{member.mention} : mention member`
            `{member.name} : member username`
            `{member.count} : server member count`
            `{member.server_name} : server name`
            `{member.role} : member role`

        Note:
            `Before Set Welcome msg pls use this command`
        """
    
    def welcome_enable(self):
        return """
        Enable or Disable Welcome Msg
        
        Aliases:
            `['we']`
        
        Roles:
            `Administrator`
        Ex:
            `Ywelcome_enable on`
            `Ywelcome_enable enable`
            `Ywelcome_enable disable`
            `Ywelcome_enable off`
        """
    
    def set_welcome_image(self):
        return """
        Set Welcome Images

        Aliases:
            `['welcome_image','swi']`

        Roles:
            `Administrator`
        
        Ex:
            `Yset_welcome_image image_url`
        
        Default:
            `Yae Sakura Images`

        Note:
            `You can Set 10 images max`

        """

    def test_welcome(self):
        return """
        Send Original Set Msg
        
        Aliases:
            `['tw']`

        Roles:
            `Administrator`
        
        Ex:
            `Ytest_welcome`

        Note:
            `When You set New Welcome Msg after that use This Command. This will Show how welcome msg look like when member join.`    
        """
        # pass

    # def compare(self,name):
        
    #     pass

def return_help(name):
    get_help = Help()
    method_list = [method for method in dir(Help) if method.startswith('__') is False]
    for func in method_list:
        if str(func) == str(name):
            return (str(eval('get_help.'+func+"()")))

# print(return_help("show_prefix"))
# print(method_list)
