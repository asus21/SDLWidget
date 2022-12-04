#-*- coding: UTF-8 -*-
import curses
from threading import Thread
import time
import window as wind
class window:
    def __init__(self):
        self.root=curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.h,self.w=self.root.getmaxyx()
    def creat_head(self):
        self.head_window=wind.Window(4,self.w,0,0)
        self.head_window.box(".",".")
        self.head_window.addstr(int(4/2),int(self.w/3),"|Welecome to here|")
    def creat_output(self):
        self.output_window=wind.Window(int(self.h-5),int(self.w/2),5,0)
        self.output_window.box(".",".")
        self.output_window.addstr(1,0,"output:")
    def creat_input(self):
        self.input_window=wind.Window(int((self.h-5)/2),int(self.w/2),5+int((self.h-5)/2+1),int(self.w/2))
        self.input_window.box(".",".")
        self.input_window.addstr(1,0,"intput:")
    def create_right(self):
        self.right_window=wind.Window(int((self.h-5)/2),int(self.w/2),5,int(self.w/2))
        self.right_window.box(".",".")
        self.right_window.addstr(1,0,"friend:")
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
try:
    isRun=True
    win=window()
    win.creat_head()
    win.creat_input()
    win.creat_output()
    win.create_right()
    win.head_refresh()
    win.input_refresh()
    win.output_refresh()
    win.right_refresh()
    curses.setsyx(0,0)
    win.root_event()
except Exception as e:
    raise e
finally:
    win.close()
'''
stdscr = curses.initscr()
newwin=curses.newwin(10,10,0,0)
def display_info(str, x, y, colorpair=2):
      
    global stdscr,newwin
    
    newwin.addstr(y, x,str, curses.color_pair(colorpair))
    newwin.refresh()
def get_key():
    
    global stdscr
    if stdscr.getkey()==curses.KEY_ENTER:
        return True
    else:
        return False

def get_ch_and_continue():
    global stdscr
    #设置nodelay，为0时会变成阻塞式等待
    mes=[]
    row=0
    col=0
    stdscr.nodelay(0)
    #输入一个字符
    while True: 
        ch=stdscr.getch()
        if ch==ord("\x1b"):
            break
        elif ch==ord("\n"):
            row+=1
            col=0
            stdscr.move(row,col)
        else:
            display_info(chr(ch),col,row,2)
            mes.append(ch)
            col+=1
    #重置nodelay,使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
#    stdscr.nodelay(1)
    return True

def set_win():
    global stdscr,newwin
    #使用颜色首先需要调用这个方法
    curses.start_color()
    #文字和背景色设置，设置了两个color pair，分别为1和2
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    #关闭屏幕回显
    curses.noecho()
    stdscr.box(".",".")
    newwin.box(".",".")
    #输入时不需要回车确认
#    curses.cbreak()
    #设置nodelay，使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)

def unset_win():
    global stdstr
    #恢复控制台默认设置（若不恢复，会导致即使程序结束退出了，控制台仍然是没有回显的）
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    #结束窗口
    curses.endwin()
if __name__=='__main__':
    try:
        set_win()
        get_ch_and_continue()
    except Exception as e:
        raise e
    finally:
        unset_win()
'''
