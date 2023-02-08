#-*- coding: UTF-8 -*-
import curses
from curses import ascii
from threading import Thread
import time
from widget.textWindow import TextWindow
from window.login import LoginWindow
from window.register import RegisterWindow
from window.friend import FriendWindow
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
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        self.h,self.w=self.root.getmaxyx()
        self.root.nodelay(0)
        self.root.keypad(True)
        self.root.untouchwin()
        self.tcp=TCPClient(host,TCPport)
        self.udp=UDPClient(host,UDPport)
        self.login=None
        self.input_window=None
        self.register=None
    def create_login(self):
        '''创建登录窗口'''
        self.login=LoginWindow(self.h,self.w,0,0)
        self.login.button_login_bind(self.button_login)
        self.login.button_register_bind(self.button_register)
    def create_register(self):
        '''注册窗口'''
        self.register=RegisterWindow(self.h,self.w,0,0)
        self.register.button_sure_bind(self.button_sure)
        self.register.button_return_bind(self.button_reture)
    def create_head(self):
        '''截面头部'''
        self.head_window=TextWindow(4,self.w,0,0)
        self.head_window.box(".",".")
        self.head_window.addstr(4//2,self.w//3,"|Welecome to myChat|")
    def create_output(self):
        '''输出窗口'''
        self.output_window=TextWindow(self.h-5,self.w//2,5,0)
        self.output_window.box(".",".")
        self.output_window.addstr(1,0,"output:")
        self.output_window.setEditable(False)
    def create_input(self):
        '''输入窗口'''
        self.input_window=TextWindow((self.h-5)//2,self.w//2,5+(self.h-5)//2,self.w//2)
        self.input_window.box(".",".")
        self.input_window.addstr(1,0,"intput:")
        self.input_window.bind(self.inputFun)
    def create_right(self):
        '''创建朋友列表窗口'''
        self.right_window=TextWindow(int((self.h-5)/2),int(self.w/2),5,int(self.w/2))
        self.right_window.box(".",".")
        self.right_window.addstr(1,0,"friend:")
        self.right_window.setEditable(False)
        self.right_window.setText("a\nb\bhello world")
        self.right_window.bind(self.friendFun)
    def login_refresh(self):
        '''登录界面刷新'''
        self.login.refresh()
    def register_refreah(self):
        '''注册截面刷新'''
        self.register.refresh()
    def head_refresh(self):
        '''头部界面刷新'''
        self.head_window.refresh()
    def input_refresh(self):
        '''输入窗口截面刷新'''
        self.input_window.refresh()
    def output_refresh(self):
        '''输出截面刷新'''
        self.output_window.refresh()
    def right_refresh(self):
        '''朋友列表刷新'''
        self.right_window.refresh()
    def close(self):
        '''关闭界面'''
        self.tcp.close()
        self.udp.close()
        curses.endwin()
    def button_login(self):
        '''登录函数'''
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
    def button_register(self):
        self.root.erase()
        self.login=None
        self.root.refresh()
        self.register_win()
    def button_exit(self):
        self.close()
    def button_sure(self):
        data=self.register.getData()
        if data["password"]==data["again"]:
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
                    Thread(target=self.register.alert,args=("Fail to register",)).start()
            else:
                Thread(target=self.register.alert,args=('The password is null',)).start()
        else:
            Thread(target=self.register.alert,args=('Differ from password and again',)).start()
    def button_reture(self):
        self.root.erase()
        self.register=None
        self.root.refresh()
        self.login_win()
    def inputFun(self,ch):
        if ch==ascii.ctrl("s"):
            msg=self.input_window.getText()
            friend=self.right_window.getLineText()
            self.udp.setMsg(msg)
            self.udp.setFriend(self.right_window.getLineText())
            self.udp.sendMsg()
        if ch==ascii.ctrl("a"):
            self.root.erase()
            self.input_window=self.output_window=self.right_window=None
            self.root.refresh()
            self.addFd_win()

    def friendFun(self,ch):
        if ch==ascii.ctrl("a"):
            self.right_window.highlightLine()
            y,x=self.input_window.getCursor()
#            self.root.addstr(0,0,str(y)+" "+str(x))
#            self.root.move(5,5)
#            self.root.refresh()
            
        elif ch==ascii.ctrl("d"):
            self.right_window.unhighlightLine()
    def root_event(self):
#        self.login.ungetmouse()
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
                else:
                    self.input_window.event(ch)
                    self.output_window.event(ch)
                    self.right_window.event(ch)
            else:
                if self.login:
                    self.login.event(ch)
                elif self.register:
                    self.register.event(ch)
                else:   
                    self.input_window.event(ch)
                    self.output_window.event(ch)
                    self.right_window.event(ch)
    def login_win(self):
        self.create_login()
        self.login.ungetmouse()
        self.login_refresh()
    def register_win(self):
        self.create_register()
        self.register.ungetmouse()
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

