import curses

class Window:
    def __init__(self,h,w,y,x):
        self.w=w
        self.h=h
        self.x=x
        self.y=y
        self.win=curses.newwin(h,w,y,x)
        self.sub_y=self.y+2
        self.sub_x=self.x+1
        self.sub_w=self.w-2
        self.sub_h=self.h-3
        self.subwin=self.win.subwin(self.sub_h,self.sub_w,self.sub_y,self.sub_x)
        self.cur_x=0
        self.cur_y=0
        self.scroll=0
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
        self.subwin.scrollok(True)
        self.subwin.setscrreg(0,self.sub_h-1)
        if self.onfocus():
            self.subwin.move(row,col)   
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
            elif event==127:
                col-=1
                if col>0:
                    self.subwin.delch(row,col)
            else:
                self.msg.append(chr(event)) 
                self.subwin.addstr(row,col,chr(event))
                col+=1
            if col+1>=self.sub_w:
                row+=1
                col=1
            if col<1:
                row-=1
                if row>0:
                    col=self.sub_w-1
                else:
                    col=1
            if row>=self.sub_h:
                row=self.sub_h-1
                self.subwin.scroll(1)
                self.scroll+=1
            if row<0:
                row=0
                if self.scroll>0:
                    self.subwin.scroll(-1)
                    self.scroll-=1
            self.subwin.move(row,col)
            self.subwin.refresh()
            self.cur_y=row
            self.cur_x=col       
