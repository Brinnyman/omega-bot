from tinydb import TinyDB
from tinydb import where
import os

path = os.path.abspath('')
db_file = os.path.join(path, 'config', 'db.json')
db = TinyDB(db_file)


class Experience:
    def getxp(self, user):
        self.userid = user.id
        if db.search(where('userid') == self.userid):
            for data in db.search(where('userid') == self.userid):
                return data['xp']
        else:
            db.insert({'userid': self.userid, 'xp': 0})
            return 0

    def setxp(self, user, xp):
        self.userid = user.id
        self.userxp = int(xp)
        if db.search(where('userid') == self.userid):
            for data in db.search(where('userid') == self.userid):
                self.userxp += data['xp']
                db.update({'xp': self.userxp}, where('userid') == self.userid)
        else:
            db.insert({'userid': self.userid, 'xp': self.userxp})

    def removexp(self, user, xp):
        self.userid = user.id
        self.userxp = int(xp)
        if db.search(where('userid') == self.userid):
            for data in db.search(where('userid') == self.userid):
                if data['xp'] - self.userxp < 0:
                    data['xp'] = 0
                    print('less then 0')
                else:
                    data['xp'] -= self.userxp
                    print('is higher then 0')

                db.update({'xp': data['xp']}, where('userid') == self.userid)
        else:
            db.insert({'userid': self.userid, 'xp': self.userxp})

    def getrank(self, user):
        xp = self.getxp(user)
        rank = ''

        if xp >= 100:
            rank = 'King'
        elif xp >= 50:
            rank = 'Alpha'
        elif xp >= 0:
            rank = 'Pleb'

        return rank
