import curses

class Label:
    def __init__(self,top,h,w,y,x):
        self.h,self.w=h,w
        self.y,self.x=y,x
        self.label=top.derwin(h,w,y,x)
        self.label.box(curses.ACS_VLINE,curses.ACS_HLINE) 
    def setText(self,text):
        self.label.addstr(int(self.h/2),int(self.w/2-len(text)/2),text)
        self.label.refresh()
    def bind(self,func=None):
        self.func=func
    def refresh(self):
        self.label.refresh()
    def onfocus(self):
        y,x=curses.getsyx()
        if x>self.x and x<self.x+self.w:
            if y>self.y and y<self.y+self.h:
                return True
            else:
                return False
        else:
            return False
    def event(self):
        if self.onfocus():
            if self.func:
                self.func()
        
