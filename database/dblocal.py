'''
数据库
用户dbChat.db 
表1朋友信息表 friend send msg datatime
查找数据库中所有的表 SELECT name FROM sqlite_master WHERE type='table'
'''
import sqlite3
import time
class dbLocal:
    def __init__(self,datafile):
        self.db=sqlite3.connect(datafile)
        self.curs=self.db.cursor()

    def create_msgTable(self):
        '''创建朋友信息表'''
        self.curs.execute("create table if not exists msgTable(friend text not null,send int not null, msg text not null ,time timestamp default (datetime('now','localtime')));")


    def add_msgData(self,value):
        '''添加消息'''
        '''信息:朋友名称,接受或发送,消息,时间'''
        self.curs.execute("insert into msgTable (friend,send,msg) values(?,?,?);",(value[0],value[1],value[2]))
        self.commit()

    def delete_all_msgData(self,user):
        '''删除所有消息'''
        self.curs.execute("delete from msgTable;")
        self.commit()

    def delete_friend_msgData(self,friend,time):
        sele.curs.execute("delete from msgTable where friend=? and send=? and time=?",(friend,send,time))
        self.commit()

    def query_all_magData(self)->list:
        '''获取用户所有朋友消息'''
        self.curs.execute("select * from msgTable")
        return self.curs.fetchall()

    def query_friend_msgData(self,friend):
        self.curs.execute("select * from msgTable where friend=?",(friend,))
        return self.curs.fetchall()

    def show_tableinfo(self,table)->list:
        '''显示数据表信息'''
        self.curs.execute("PRAGMA table_info(%s)"%(table,))
        return self.curs.fetchall()

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
    db=dbLocal("dblocal.db")
    db.create_msgTable()
    db.add_msgData(["ts",1,"hello world"])
    db.add_msgData(["me",0,"I'm not fine"])
    print(db.query_all_magData())
    print(db.query_friend_msgData("me"))
    db.close()
