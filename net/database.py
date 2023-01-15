'''
数据库
用户users.db 
表1db_user username gender password friend 
表2db_friend username friendname

在线用户online.db username
查找数据库中所有的表 SELECT name FROM sqlite_master WHERE type='table'
'''
import sqlite3
class Database:
    def __init__(self,datafile):
        self.db=sqlite3.connect(datafile)
        self.curs=self.db.cursor()
    def create_usersTable(self):
        self.curs.execute("create table if not exists usersData(user text primary key,password text not null);")
    def create_friendsTable(self):
        self.curs.execute("create table if not exists friendsData(user text,friend text primary key);")
    def add_userData(self,value): 
        if not self.is_existsUser(value[0]):
            self.curs.execute("insert into usersData values(?,?);",(value[0],value[1]))
    def add_friendData(self,value):
        if not self.is_existsFriend(value[1]):
            self.curs.execute("insert into friendsData values(?,?);",(value[0],value[1]))
    def delete_userData(self,user):
        self.curs.execute("delete from usersData where user=?;",(user,))
    def delete_friendData(self,user):
        self.curs.execute("delete friendsData where user=?;",(user,))
    def update_userPassword(self,user,password):
        self.curs.execute("update usersData set password=? where user=?;",(password,user))
    def query_userPassword(self,user):
        self.curs.execute("select password from usersData where user=?",(user,))
        return self.curs.fetchone()
    def query_userFriends(self,user):
        self.curs.execute("select friend from friendsData where user=?",(user,))
        return self.curs.fetchall()
    def show_tableinfo(self,table):
        self.curs.execute("PRAGMA table_info(%s)"%(table,))
        return self.curs.fetchall()
    def is_existsUser(self,user):
        self.curs.execute("select * from usersData where user=?",(user,))
        return True if self.curs.fetchone() else False
    def is_existsFriend(self,friend):
        self.curs.execute("select * from friendsData where friend=?",(friend,))
        return True if self.curs.fetchone() else False
    def drop_table(self,table):
        self.curs.execute("drop table %s"%(table))
    def close(self):
        self.curs.close()
        self.db.commit()
        self.db.close()

if __name__=="__main__":
    db=Database("dbChat.db")
    db.create_usersTable()
    db.create_friendsTable()
    db.add_userData(["ts","187"])
    db.add_userData(["ba","135"])
    db.add_friendData(["ts","ba"])
    print(db.query_userPassword("ts"))
    db.update_userPassword("ts","110")
    print(db.query_userPassword("ba"))
    print(db.show_tableinfo("usersData"))
    db.drop_table("usersData")
    db.drop_table("friendsData")
    db.close()
