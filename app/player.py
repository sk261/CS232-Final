import time

class Player:
    def __init__(self, un, pw):
        self.isMining = False
        self.logged = False
        self._verifyTime = time.time
        self._maxTimeUntilLogOutMS = 10 # 10 seconds
        self.userID = un
        self.userPW = pw # Not the safest game
        self.position = [0, 0] # Always spawn in the center, because why not
        self.cursourPosition = [0, 0] # Modified to user (ie, [1,0] cursor at [2,3] position is a cursor at [3,3])
    
    def reverify(self):
        self._timeUntilLogOutMS = 0
        self._verifyTime = time.time
    
    def tick(self):
        # This is unnecessary - Return true if the user hasn't verified in a while
        self.logged = not (time.time - self._verifyTime > self._maxTimeUntilLogOutMS)
        return not self.logged


    # TODO: In parent, make sure player doesn't walk where they're not allowed
    def move(self, x, y):
        self.position[0] += x
        self.position[1] += y

    


'''
+ tick() : void
'''