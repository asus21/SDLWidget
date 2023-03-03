import curses
from widget import color
class Label:
    def __init__(self,top,h,w,y,x):
        self.h,self.w=h,w
        self.y,self.x=y,x
        self.__label=top.subwin(h,w,y,x)
        self.__label.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.__func=None
        self.__light=False
        self.__isActive=True
    def setText(self,text):
        self.__label.addstr(self.h//2,(self.w-len(text))//2,text)
        self.__label.refresh()
    def bind(self,func=None):
        self.__func=func
    def refresh(self):
        self.__label.refresh()
    def highlight(self):
        y,x=curses.getsyx()
        self.__label.attron(color.red)
        self.__label.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.__label.attroff(color.red)
        self.__label.refresh()
        curses.setsyx(y,x)   
        curses.doupdate()
    def unhighlight(self):
        y,x=curses.getsyx()
        self.__label.box(curses.ACS_VLINE,curses.ACS_HLINE)       
        self.__label.refresh()
        curses.setsyx(y,x)
        curses.doupdate()
    @property
    def isActive(self):
        return self.__isActive
    def setfocus(self):
        self.__label.move(0,0)
        self.__label.refresh()
    def onfocus(self):
        y,x=curses.getsyx()
        if x>=self.x and x<=self.x+self.w:
            if y>=self.y and y<=self.y+self.h:
                return True
            else:
                return False
        else:
            return False
    def event(self,event):
        if self.onfocus():
            self.__isActive=True
            if not self.__light:
                self.highlight()
                self.__light=True
            if event==curses.KEY_MOUSE:
                if self.__func:
                    self.__func()
            elif event=='\n':
                if self.__func:
                    self.__func()
        else:
            self.__isActive=False
            if self.__light:
                self.unhighlight()
                self.__light=False
        
