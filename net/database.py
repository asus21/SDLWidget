'''
数据库
用户dbChat.db 
表1用户信息表 usersData user password
表2朋友信息表 friendData user friend
表3用户日志表 usersLog user ip
查找数据库中所有的表 SELECT name FROM sqlite_master WHERE type='table'
'''
import sqlite3
class Database:
    def __init__(self,datafile):
        self.db=sqlite3.connect(datafile)
        self.curs=self.db.cursor()

    def create_usersTable(self):
        '''创建用户信息表'''
        self.curs.execute("create table if not exists usersData(user text primary key not null,password text not null);")

    def create_friendsTable(self):
        '''创建朋友信息表'''
        self.curs.execute("create table if not exists friendsData(user text not null,friend text primary key not null);")

    def create_usersLogTable(self):
        '''创建用户日志表'''
        self.curs.execute("create table if not exists usersLog(user text primary key not null,ip text not null,port int);")

    def add_userData(self,value): 
        '''添加用户信息(用户，密码)'''
        if not self.is_existsUser(value[0]):
            self.curs.execute("insert into usersData values(?,?);",(value[0],value[1]))
            self.commit()

    def add_friendData(self,value):
        '''添加朋友'''
        if not self.is_existsFriend(value[1]):
            self.curs.execute("insert into friendsData values(?,?);",(value[0],value[1]))
            self.commit()

    def add_userLog(self,value):
        '''添加用户日志'''
        if not self.is_existsUserLog(value[0]):
            self.curs.execute("insert into usersLog values(?,?,?)",(value[0],value[1],value[2]))
            self.commit()

    def delete_userData(self,user):
        '''注销用户'''
        self.curs.execute("delete from usersData where user=?;",(user,))
        self.commit()

    def delete_friendData(self,user):
        '''删除朋友'''
        self.curs.execute("delete from friendsData where user=?;",(user,))
        self.commit()

    def delete_userLogData(self,user):
        '''删除单个用户日志'''
        self.curs.execute("delete from usersLog where user=?;",(user,))
        self.commit()
    
    def delete_userLogDatas(self):
        '''删除所有用户日志'''
        self.curs.execute("delete from usersLog")

    def update_userPassword(self,user,password):
        '''修改用户密码'''
        self.curs.execute("update usersData set password=? where user=?;",(password,user))
        self.commit()

    def update_usersPort(self,user,port):
        '''修改用户日志'''
        self.curs.execute("update usersLog set port=? where user=?;",(port,user))
        self.commit()

    def query_userPassword(self,user)->str:
        '''获取用户密码'''
        self.curs.execute("select password from usersData where user=?",(user,))
        return self.curs.fetchone()[0]

    def query_userFriends(self,user)->list:
        '''获取用户所有朋友'''
        self.curs.execute("select friend from friendsData where user=?",(user,))
        return [x[0] for x in self.curs.fetchall()]

    def query_usersLog(self,user)->str:
        '''获取用户日志'''
        self.curs.execute("select * from usersLog where user=?",(user,))
        return self.curs.fetchone()[0]

    def show_tableinfo(self,table)->list:
        '''显示数据表信息'''
        self.curs.execute("PRAGMA table_info(%s)"%(table,))
        return self.curs.fetchall()

    def is_existsUser(self,user)->bool:
        '''检查是否存在用户'''
        self.curs.execute("select * from usersData where user=?",(user,))
        return True if self.curs.fetchone() else False

    def is_existsFriend(self,friend)->bool:
        '''检查是否存在朋友'''
        self.curs.execute("select * from friendsData where friend=?",(friend,))
        return True if self.curs.fetchone() else False

    def is_existsUserLog(self,user)->bool:
        '''检查是否存在用户记录'''
        self.curs.execute("select * from usersLog where user=?",(user,))
        return True if self.curs.fetchone() else False

    def drop_table(self,table):
        '''删除数据表'''
        self.curs.execute("drop table %s"%(table))
        self.commit()

    def commit(self):
        '''提交事务'''
        self.db.commit()

    def close(self):
        '''关闭数据库'''
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
    db.add_friendData(["ts","ok"])
    print(db.query_userFriends("ts"))
    db.update_userPassword("ts","110")
    print(db.query_userPassword("ba"))
    print(db.show_tableinfo("usersData"))
    db.drop_table("usersData")
    db.drop_table("friendsData")
    db.close()
