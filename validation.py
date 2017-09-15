from discord.ext import commands
from config import Configuration
from permission import Permission
config = Configuration()
permit = Permission()

def validation():
    def validate(ctx):
        userid = ctx.message.author.id
        userroles = ctx.message.author.roles
        command = ctx.message.content.split(' ', 1)[0][1:]
        validated = False

        if userid == config.ownerid:
            validated = True
        else:
            for i in userroles:
                if i.id in config.permitted:
                    if permit.check_command(i.name, command):
                        validated = True

        return validated

    return commands.check(validate)
