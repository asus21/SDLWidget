#-*- coding: UTF-8 -*-
import curses
from curses import ascii
from threading import Thread
import time
from widget.textWindow import TextWindow
from login import LoginWindow
from register import RegisterWindow
from net.client import TCPClient
from net.client import UDPClient
import locale
locale.setlocale(locale.LC_ALL, '')
host="127.0.0.1"
TCPport=8080
UDPport=8081
class MainWindow:
    '''主窗口'''
    def __init__(self):
        self.root=curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)
        self.h,self.w=self.root.getmaxyx()
        self.root.nodelay(0)
        self.root.keypad(True)
        self.tcp=TCPClient(host,TCPport)
        self.udp=UDPClient(host,UDPport)
        self.login=None
        self.input_window=None
        self.register=None
    def create_login(self):
        self.login=LoginWindow(self.h,self.w,0,0)
        self.login.login_bind(self.loginFun)
        self.login.register_bind(self.login_registerFun)
    def create_register(self):
        self.register=RegisterWindow(self.h,self.w,0,0)
        self.register.register_bind(self.registerFun)
        self.register.exit_bind(self.register_exitFun)
    def create_head(self):
        self.head_window=TextWindow(4,self.w,0,0)
        self.head_window.box(".",".")
        self.head_window.addstr(4//2,self.w//3,"|Welecome to myChat|")
    def create_output(self):
        self.output_window=TextWindow(self.h-5,self.w//2,5,0)
        self.output_window.box(".",".")
        self.output_window.addstr(1,0,"output:")
        self.output_window.setEditable(False)
    def create_input(self):
        self.input_window=TextWindow((self.h-5)//2,self.w//2,5+(self.h-5)//2,self.w//2)
        self.input_window.box(".",".")
        self.input_window.addstr(1,0,"intput:")
        self.input_window.bind(self.sendFun)
    def create_right(self):
        self.right_window=TextWindow(int((self.h-5)/2),int(self.w/2),5,int(self.w/2))
        self.right_window.box(".",".")
        self.right_window.addstr(1,0,"friend:")
        self.right_window.setEditable(False)
        self.right_window.setText("a\nb\bhello world")
        self.right_window.bind(self.friendFun)
    def login_refresh(self):
        self.login.refresh()
    def register_refreah(self):
        self.register.refresh()
    def head_refresh(self):
        self.head_window.refresh()
    def input_refresh(self):
        self.input_window.refresh()
    def output_refresh(self):
        self.output_window.refresh()
    def right_refresh(self):
        self.right_window.refresh()
    def close(self):
        self.tcp.close()
        self.udp.close()
        curses.endwin()
    def loginFun(self):
        data=self.login.getText()
        if data["user"] and data["password"]:
            self.tcp.setUser(data["user"])
            self.tcp.setPassword(data["password"])
            self.tcp.setMsg("verify")
            self.tcp.sendMsg()
            msg=self.tcp.recvMsg()
            if msg["result"]:
                self.root.erase()
                self.login=None
                self.root.refresh()
                self.chat_win()
                self.tcp.close()
                self.udp.setUser(data['user'])
            else:
                Thread(target=self.login.alert,args=("don't exist the user",)).start()
        else:
            Thread(target=self.login.alert,args=('the password is null',)).start()
    def login_registerFun(self):
        self.root.erase()
        self.login=None
        self.root.refresh()
        self.register_win()
    def login_exitFun(self):
        self.close()
    def registerFun(self):
        data=self.register.getText()
        if data["user"] and data["password"]:
            self.tcp.setUser(data["user"])
            self.tcp.setPassword(data["password"])
            self.tcp.setMsg("register")
            self.tcp.sendMsg()
            msg=self.tcp.recvMsg()
            if msg["result"]:
                self.root.erase()
                self.register=None
                self.root.refresh()
                self.login_win()
            else:
                Thread(target=self.register.alert,args=("fail to register",)).start()
        else:
            Thread(target=self.register.alert,args=('the password is null',)).start()
    def register_exitFun(self):
        self.root.erase()
        self.register=None
        self.root.refresh()
        self.login_win()
    def sendFun(self,ch):
        if ch==ascii.ctrl("s"):
            msg=self.input_window.getText()
            friend=self.right_window.getLineText()
            self.udp.setMsg(msg)
            self.udp.setFriend(self.right_window.getLineText())
            self.udp.sendMsg()
    def friendFun(self,ch):
        if ch==ascii.ctrl("a"):
            self.right_window.highlightLine()
        elif ch==ascii.ctrl("d"):
            self.right_window.unhighlightLine()
    def root_event(self):
        self.root.untouchwin()
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        win=None
        while True:
            ch=self.root.get_wch()
            if ch=="\x1b":
                self.close()
                break
            if ch==curses.KEY_MOUSE:
                _,x,y,_,n=curses.getmouse()
                self.root.move(y,x)
                self.root.refresh()
                if self.login:
                    self.login.event(ch)
                elif self.register:
                    self.register.event(ch)
                elif self.input_window:
                    self.input_window.event(ch)
                    self.output_window.event(ch)
                    self.right_window.event(ch)
            else:
                if self.login:
                    self.login.event(ch)
                elif self.register:
                    self.register.event(ch)
                elif self.input_window:   
                    self.input_window.event(ch)
                    self.output_window.event(ch)
                    self.right_window.event(ch)
    def login_win(self):
        self.create_login()
        self.login_refresh()
    def register_win(self):
        self.create_register()
        self.register_refreah()
    def chat_win(self):
        self.create_head()
        self.create_input()
        self.create_output()
        self.create_right()
        self.head_refresh()
        self.input_refresh()
        self.output_refresh()
        self.right_refresh()
if __name__=="__main__":
    win=MainWindow()
    try:
        win.login_win()
        win.root_event()
    except Exception as e:
        raise e
    finally:
        win.close()

