class User:
    def __init__(self,name=None,password=None):
        self.name=name
        self.password=password
        self.friends=[]

    def getName(self):
        return self.name

    def setName(self,name):
        self.name=name

    def getPassword(self):
        return self.password

    def setPassword(self,password):
        self.password=password

    def getFriends(self):
        return self.friends

    def addFriend(self,friendName):
        self.friends.append(friendsName)


    
