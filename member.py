class Member:
    def __init__(self):
        self.user = {
            'userid': '98846938123751424',
            'xp': 96,
        }
        print(self.user)

    def setxp(self, user, xp):
        self.userid = user.id
        self.userxp = int(xp)

        if self.userid == self.user['userid']:
            self.user['xp'] += self.userxp

    def getxp(self, user):
        self.userid = user.id
        if self.userid == self.user['userid']:
            return self.user['xp']

    def checkxp(self, user, oldxp):
        self.userid = user.id
        self.userxp = int(oldxp)

        if self.userid == self.user['userid']:
            if self.userxp != self.user['xp']:
                self.difference = self.userxp - self.user['xp']
                self.setxp(user, self.difference)

    # def calculatexp(self, bot, ctx):
    #     self.oldxp = 0
    #     self.user = ctx.message.mentions[0]
    #     for msg in bot.logs_from(ctx.message.channel, limit=9999999):
    #         if msg.author == self.user:
    #             self.oldxp += 1
    #
    #     self.checkxp(self.user, self.oldxp)
    #     print(self.oldxp)
