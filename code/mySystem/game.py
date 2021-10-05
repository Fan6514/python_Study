"game module"

import os
import json
from log import lg, LEVELS, info, debug, warn, error

# game config file
USERCONF = os.path.join(os.getcwd(), 'conf/userInfo.json')

def dict2userinfo(usr):
    return UserInfo(usr['userName'], usr['level'], usr['curExp'], 
                    usr['combatEffectiveness'], usr['healthPoint'], 
                    usr['cash'])

def userinfo2dict(usr):
    return {
        'userName' : usr.userName,
        'level' : usr.level,
        'curExp' : usr.curExp,
        'combatEffectiveness' : usr.combatEffectiveness,
        'healthPoint' : usr.healthPoint,
        'cash' : usr.cash
    }

class UserInfo(object):
    def __init__(self, userName, level, curExp, 
                combatEffectiveness, healthPoint, cash):
        self.userName = userName
        self.level = level
        self.curExp = curExp
        self.combatEffectiveness = combatEffectiveness
        self.healthPoint = healthPoint
        self.cash = cash

class Game(object):
    def __init__(self):
        self.player = None
        self.conf = USERCONF

        self.initInfo()
        self.run()
        self.deInitInfo()

    def _create_newPlayer(self):
        print('注册：')
        name = input('输入用户昵称：')
        newPlayer = UserInfo(name, 0, 0, 10, 10, 0)
        return newPlayer
        
    def loadConfig(self):
        if not os.path.exists(self.conf):
            self.saveconfig()
        
        # read player info configure
        with open(self.conf, 'r') as conf:
            self.player = json.loads(conf.read(), object_hook=dict2userinfo)

    def saveconfig(self):
        # create a new player
        if self.player is None:
            self.player = self._create_newPlayer()
        
        # write player info configure
        with open(self.conf, 'w') as conf:
            conf.write(json.dumps(self.player, default=userinfo2dict))

    def initInfo(self):
        self.loadConfig()

    def deInitInfo(self):
        self.saveconfig()
    
    def run(self):
        pass
