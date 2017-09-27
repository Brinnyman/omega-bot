class Experience:
    def __init__(self):
        self.user = {
            'userid': '98846938123751424',
            'xp': 96,
        }

    def getxp(self, user):
        self.userid = user.id
        if self.userid == self.user['userid']:
            return self.user['xp']

    def setxp(self, user, xp):
        self.userid = user.id
        self.userxp = int(xp)

        if self.userid == self.user['userid']:
            if self.userxp != self.getxp(user):
                self.user['xp'] += self.userxp

    def removexp(self, user, xp):
        self.userid = user.id
        self.userxp = int(xp)

        if self.userid == self.user['userid']:
            if self.userxp != self.getxp(user):
                self.user['xp'] -= self.userxp
