#-*- coding: UTF-8 -*-
import curses
from threading import Thread
import time
from widget.textWindow import TextWindow
from login import LoginWindow
import locale
locale.setlocale(locale.LC_ALL, '')
class MainWindow:
    def __init__(self):
        self.root=curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0)
        self.h,self.w=self.root.getmaxyx()
        self.login=None
        self.input_window=None
        self.root.nodelay(0)
        self.root.keypad(True)
    def create_login(self):
        self.login=LoginWindow(self.h,self.w,0,0)
        self.login.bind(self.loginFun)
    def create_head(self):
        self.head_window=TextWindow(4,self.w,0,0)
        self.head_window.box(".",".")
        self.head_window.addstr(int(4/2),int(self.w/3),"|Welecome to here|")
    def create_output(self):
        self.output_window=TextWindow(int(self.h-5),int(self.w/2),5,0)
        self.output_window.box(".",".")
        self.output_window.addstr(1,0,"output:")
        self.output_window.setEditable(False)
    def create_input(self):
        self.input_window=TextWindow(int((self.h-5)/2),int(self.w/2),5+int((self.h-5)/2),int(self.w/2))
        self.input_window.box(".",".")
        self.input_window.addstr(1,0,"intput:")
    def create_right(self):
        self.right_window=TextWindow(int((self.h-5)/2),int(self.w/2),5,int(self.w/2))
        self.right_window.box(".",".")
        self.right_window.addstr(1,0,"friend:")
        self.right_window.setEditable(False)
    def login_refresh(self):
        self.login.refresh()
    def head_refresh(self):
        self.head_window.refresh()
    def input_refresh(self):
        self.input_window.refresh()
    def output_refresh(self):
        self.output_window.refresh()
    def right_refresh(self):
        self.right_window.refresh()
    def close(self):
        curses.endwin()
    def loginFun(self):
        self.root.erase()
        self.login.setEnable(False)
        self.root.refresh()
        self.chat_win()
    def root_event(self):
        self.root.untouchwin()
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        win=None
        while True:
            ch=self.root.get_wch()
#            ch=self.root.getch()
            if ch=="\x1b":
                self.close()
                break
            if ch==curses.KEY_MOUSE:
                _,x,y,_,n=curses.getmouse()
                self.root.move(y,x)
                self.root.refresh()
                if self.login:
                    self.login.event(ch)
                if self.input_window:
                    self.input_window.event(ch)
                    self.output_window.event(ch)
                    self.right_window.event(ch)
            else:
                if self.login:
                    self.login.event(ch)
                if self.input_window:   
                    self.input_window.event(ch)
                    self.output_window.event(ch)
                    self.right_window.event(ch)
    def login_win(self):
        self.create_login()
        self.login_refresh()
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
    try:
        win=MainWindow()
        win.login_win()
#        win.create_login()
#        win.login_refresh()
#        win.creat_head()
#        win.creat_input()
#        win.creat_output()
#        win.create_right()
#        win.head_refresh()
#        win.input_refresh()
#        win.output_refresh()
#        win.right_refresh()
#        curses.setsyx(0,0)
        win.root_event()
    except Exception as e:
        raise e
    finally:
        win.close()

