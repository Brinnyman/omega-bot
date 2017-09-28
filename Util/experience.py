from tinydb import TinyDB
from tinydb import where
import os

path = os.getcwd()
db_file = path + '/config/db.json'
db = TinyDB(db_file)


class Experience:
    def getxp(self, user):
        self.userid = user.id
        if db.search(where('userid') == self.userid):
            for data in db.search(where('userid') == self.userid):
                print(data['xp'])
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
                print(self.userxp)
                db.update({'xp': self.userxp}, where('userid') == self.userid)
        else:
            db.insert({'userid': self.userid, 'xp': self.userxp})

    def removexp(self, user, xp):
        self.userid = user.id
        self.userxp = int(xp)
        if db.search(where('userid') == self.userid):
            for data in db.search(where('userid') == self.userid):
                data['xp'] -= self.userxp
                print(data['xp'])
                db.update({'xp': data['xp']}, where('userid') == self.userid)
        else:
            db.insert({'userid': self.userid, 'xp': self.userxp})
