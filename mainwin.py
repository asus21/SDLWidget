#-*- coding: UTF-8 -*-
import curses
from threading import Thread
import time
from textwindow import TextWindow
from login import LoginWin
class window:
    def __init__(self):
        self.root=curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.h,self.w=self.root.getmaxyx()
    def create_login(self):
        self.login=LoginWin(self.h,self.w,0,0)
    def creat_head(self):
        self.head_window=TextWindow(self.root,4,self.w,0,0)
        self.head_window.box(".",".")
        self.head_window.addstr(int(4/2),int(self.w/3),"|Welecome to here|")
    def creat_output(self):
        self.output_window=TextWindow(self.root,int(self.h-5),int(self.w/2),5,0)
        self.output_window.box(".",".")
        self.output_window.addstr(1,0,"output:")
    def creat_input(self):
        self.input_window=TextWindow(self.root,int((self.h-5)/2),int(self.w/2),5+int((self.h-5)/2+1),int(self.w/2))
        self.input_window.box(".",".")
        self.input_window.addstr(1,0,"intput:")
    def create_right(self):
        self.right_window=TextWindow(self.root,int((self.h-5)/2),int(self.w/2),5,int(self.w/2))
        self.right_window.box(".",".")
        self.right_window.addstr(1,0,"friend:")
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
    def root_event(self):
        self.root.nodelay(0)
        self.root.keypad(True)
        x=y=0
        self.root.untouchwin()
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        win=None
        while True:
            ch=self.root.getch()
            if ch==ord("\x1b"):
                self.close()

                break
            elif ch==curses.KEY_MOUSE:
                _,x,y,_,n=curses.getmouse()
                self.root.move(y,x)
            else:
                Thread(target=self.input_window.event,args=(ch,)).start()
                Thread(target=self.output_window.event,args=(ch,)).start()

if __name__=="__main__":
    try:
        isRun=True
        win=window()
        win.create_login()

        win.login_refresh()
#        win.creat_head()
#        win.creat_input()
#        win.creat_output()
#        win.create_right()
#        win.head_refresh()
#        win.input_refresh()
#        win.output_refresh()
#        win.right_refresh()
        curses.setsyx(0,0)
        win.root_event()
    except Exception as e:
        raise e
    finally:
        win.close()

