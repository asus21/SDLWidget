#-*- coding: UTF-8 -*-
import curses
import locale
import time
import datetime
import signal
from curses import ascii
from threading import Thread
from queue import Queue
from widget.textWindow import TextWindow
from widget.list import ListWindow
from window.login import LoginWindow
from window.register import RegisterWindow
from window.friend import FriendWindow
from net.client import TCPClient
from net.client import UDPClient
from net.client import Client
locale.setlocale(locale.LC_ALL, '')
class MainWindow:
    '''主窗口'''
    def __init__(self):
        self.root=curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        self.h,self.w=self.root.getmaxyx()
        self.root.nodelay(0)
        self.root.keypad(True)
        self.root.untouchwin()
        self.msg=Queue()
        self.win_login=None
        self.win_register=None
        self.win_input=None
        self.win_friend=None
        self.win_output=None
        self.client=Client("./config.json")
        self.client.bind(self.event_win_output_show_msg)
        signal.signal(signal.SIGINT,self.close)
        
    def create_win_login(self):
        '''创建登录窗口'''
        self.win_login=LoginWindow(self.h,self.w,0,0)
        self.win_login.button_login_bind(self.button_login)
        self.win_login.button_register_bind(self.button_register)

    def create_win_register(self):
        '''注册窗口'''
        self.win_register=RegisterWindow(self.h,self.w,0,0)
        self.win_register.button_sure_bind(self.button_sure)
        self.win_register.button_return_bind(self.button_reture)

    def create_win_head(self):
        '''界面头部'''
        self.win_head=TextWindow(4,self.w//2,0,self.w//2)
        self.win_head.box(".",".")

    def create_win_output(self):
        '''输出窗口'''
        self.win_output=ListWindow(self.h,self.w//2,0,0)
        self.win_output.box(".",".")
        self.win_output.addstr(1,0,"output:")
        self.win_output.setEditable(False)

    def create_win_input(self):
        '''输入窗口'''
        self.win_input=TextWindow((self.h-5)//2,self.w//2,5+(self.h-5)//2,self.w//2)
        self.win_input.box(".",".")
        self.win_input.addstr(1,0,"intput:")
        self.win_input.bind(self.event_win_input)
#        self.win_input.setEditable(False)

    def create_win_friend(self):
        '''创建朋友列表窗口'''
        self.win_friend=TextWindow(int((self.h-3)/2),int(self.w/2),4,int(self.w/2))
        self.win_friend.box(".",".")
        self.win_friend.addstr(1,0,"friend:")
        self.win_friend.setEditable(False)
#        self.win_friend.setText("admin\nts")
        self.win_friend.bind(self.event_win_friend)

    def refresh_win_login(self):
        '''登录界面刷新'''
        self.win_login.refresh()

    def refresh_win_register(self):
        '''注册界面刷新'''
        self.win_register.refresh()

    def refresh_win_head(self):
        '''头部界面刷新'''
        self.win_head.refresh()

    def refresh_win_input(self):
        '''输入窗口界面刷新'''
        self.win_input.refresh()

    def refresh_win_output(self):
        '''输出界面刷新'''
        self.win_output.refresh()

    def refresh_win_right(self):
        '''朋友列表刷新'''
        self.win_friend.refresh()

    def close(self,signum,frame):
        self.client.close()
        curses.endwin()

    def exit(self):
        '''关闭界面'''
        self.client.close()
        curses.endwin()

    def button_login(self):
        '''登录按钮函数'''
        data=self.win_login.getText()
        self.client.setData(data)
        msg=self.client.verify()
        if msg["result"]:
            self.root.erase()
            self.win_login=None
            self.root.refresh()
            self.show_win_chat(msg,data)
        else:
            Thread(target=self.win_login.alert,args=(msg['error'],),daemon=True).start()

    def button_register(self):
        '''注册按钮函数'''
        self.root.erase()
        self.win_login=None
        self.root.refresh()
        self.show_win_register()

    def button_exit(self):
        self.close()
        
    def button_sure(self):
        '''确认按钮'''
        data=self.win_register.getData()
        self.client.setData(data)
        msg=self.client.register()
        if msg["result"]:
            self.root.erase()
            self.win_register=None
            self.root.refresh()
            self.show_win_login()
        else:
            Thread(target=self.win_register.alert,args=(msg['error'],),daemon=True).start()
            
    def button_reture(self):
        '''返回按钮'''
        self.root.erase()
        self.win_register=None
        self.root.refresh()
        self.show_win_login()

    def event_win_output_show_msg(self,db=None):
        '''输出框接受消息事件'''
        y,x=curses.getsyx()
        self.win_output.erase()
        msg=None
        friend=self.win_friend.getLineText() 
        if not db:
            msg=self.client.getAllMsg(friend)
        else:
            msg=db.query_friend_msg(friend)
        msg=[[x[1],x[2]] for x in msg]
        self.win_output.setText(msg)
        curses.setsyx(y,x)
        
    def event_win_input(self,ch):
        '''输入框事件'''
        if ch==ascii.ctrl("s"):
            msg=self.win_input.getText()
            friend=self.win_friend.getLineText()
            if msg:
                self.client.sendMsg(friend,msg)
                self.win_input.clean()
        elif ch==ascii.ctrl("a"):
            self.root.erase()
            self.win_input=self.win_output=self.win_friend=None
            self.root.refresh()
            self.addFd_win()
        elif ch==ascii.ctrl("q"):
            self.root.erase()
            self.win_input=None
            self.win_friend=None
            self.win_output=None
            self.client.close()
            self.root.refresh()
            self.show_win_login()

    def event_win_friend(self,ch):
        '''朋友列表事件'''
        if ch==ascii.ctrl("a"):
            self.win_friend.highlightLine()
#            y,x=self.win_input.getCursor()
            self.win_input.setEditable(True) 
            self.event_win_output_show_msg()
        elif ch==ascii.ctrl("d"):
            self.win_friend.unhighlightLine()
            self.win_input.setEditable(False)

    def show_win_login(self):
        "显示登录窗口"
        self.create_win_login()
        self.win_login.ungetmouse()
        self.refresh_win_login()

    def show_win_register(self):
        "显示注册界面"
        self.create_win_register()
        self.win_register.ungetmouse()
        self.refresh_win_register()

    def show_win_chat(self,msg,data):
        "显示聊天界面"
        self.create_win_head()
        self.create_win_input()
        self.create_win_output()
        self.create_win_friend()
        self.win_friend.setText(msg["friends"])
        self.win_friend.highlightLine()
        self.event_win_output_show_msg()
        self.win_head.addstr(1,1,"User:"+data["user"])
        self.win_head.addstr(2,1,"Time:"+datetime.datetime.now().strftime("%Y-%m-%d"))
        self.refresh_win_head()
        self.refresh_win_input()
        self.refresh_win_output()
        self.refresh_win_right()

    def root_event(self):
        '''根窗口事件'''
        while True:
            ch=self.root.get_wch()
            if ch=="\x1b":
                self.exit()
                break
            if ch==curses.KEY_MOUSE:
                _,x,y,_,n=curses.getmouse()
                self.root.move(y,x)
                self.root.refresh()
                if self.win_login:
                    self.win_login.event(ch)
                elif self.win_register:
                    self.win_register.event(ch)
                else:
                    if self.win_output:
                        self.win_input.event(ch)
                    if self.win_friend:
                        self.win_friend.event(ch)
                    if self.win_output:
                        self.win_output.event(ch)
            else:
                if self.win_login:
                    self.win_login.event(ch)
                elif self.win_register:
                    self.win_register.event(ch)
                else:
                    if self.win_output:
                        self.win_input.event(ch)
                    if self.win_friend:
                        self.win_friend.event(ch)
                    if self.win_output:
                        self.win_output.event(ch)
if __name__=="__main__":
    try:
        win=MainWindow()
        win.show_win_login()
        win.root_event()
    except Exception as e:
        raise e
    finally:
        curses.endwin()
