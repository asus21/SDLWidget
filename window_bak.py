import curses

class Window:
    def __init__(self,h,w,y,x):
        self.w=w
        self.h=h
        self.x=x
        self.y=y
        self.win=curses.newwin(h,w,y,x)
        self.cur_x=0
        self.cur_y=w
    def addstr(self,y,x,str):
        self.win.addstr(y,x,str)
        self.cur_x+=1
    def box(self,w,h):
        self.win.box(w,h)
    def refresh(self):
        self.win.refresh()
    def onfocus(self):
        y,x=curses.getsyx()
        if x>self.x and x<self.x+self.w:
            if y>self.y and y<self.y+self.h:
                return True
            else:
                return False
        else:
            return False
    def event(self,event):
        self.msg=[]
        row=self.cur_y
        col=self.cur_x
        self.win.scrollok(True)
        self.win.setscrreg(2,self.h-1)
        if self.onfocus():
            self.win.move(row,col)   
            if event==ord("\n"):
                row+=1
                col=1
            elif event==curses.KEY_UP:
                row=row-1
            elif event==curses.KEY_LEFT:
                col=col-1
            elif event==curses.KEY_RIGHT:
                col+=1
            elif event==curses.KEY_DOWN:
                row+=1
            else:
                self.msg.append(chr(event)) 
                self.win.addstr(row,col,chr(event))
                col+=1
            if col+1>=self.w:
                row+=1
                col=1
            if col<1:
                row-=1
                col=1
            if row>=self.h:
                row=self.h-1
                self.win.scroll(1)
            if row<2:
                row=2
                self.win.scroll(-1)
            self.win.move(row,col)
            self.win.refresh()
            self.cur_y=row
            self.cur_x=col       
