import curses

class Label:
    def __init__(self,top,h,w,y,x):
        self.h,self.w=h,w
        self.y,self.x=y,x
        self.label=top.subwin(h,w,y,x)
        self.label.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.func=None
        self.light=False
        self.isActive=True
    def setText(self,text):
        self.label.addstr(int(self.h/2),int(self.w/2-len(text)/2),text)
        self.label.refresh()
    def bind(self,func=None):
        self.func=func
    def refresh(self):
        self.label.refresh()
    def highlight(self):
        y,x=curses.getsyx()
        curses.init_pair(1,curses.COLOR_RED,0)  
        self.label.attron(curses.A_BOLD|curses.color_pair(1))
        self.label.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.label.attroff(curses.A_BOLD|curses.color_pair(1))
        self.label.refresh()                                                        
        curses.setsyx(y,x)   
        curses.doupdate()
    def unhighlight(self):
        y,x=curses.getsyx()
        self.label.box(curses.ACS_VLINE,curses.ACS_HLINE)       
        self.label.refresh()
        curses.setsyx(y,x)
        curses.doupdate()
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
            self.isActive=True
            if not self.light:
                self.highlight()
                self.light=True
            if event==curses.KEY_MOUSE:
                if self.func:
                    self.func()
        else:
            self.isActive=False
            if self.light:
                self.unhighlight()
                self.light=False
        
