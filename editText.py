import curses
from curses import textpad
class EditText:
    def __init__(self,top,h,w,y,x):
        self.top=top
        self.h,self.w=h,w
        self.y,self.x=y,x
        self.editText=top.subwin(h,w,y,x)
        self.editText.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.setHint("ok")
        self.msg=""
        self.cur_y=1
        self.cur_x=1
    def setHint(self,hint):
#        self.win=curses.newwin(10,10,10,10)
        curses.init_pair(1,1,1)
        self.editText.attron()
        self.editText.addstr(int(self.h/2),0,hint)
        self.editText.attroff(curses.A_BOLD)
    def onfocus(self):
        y,x=curses.getsyx()
#        self.editText.addstr(1,1,"ok"+" "+" "+str(self.y)+" "+str(self.x)+" "+str(self.h)+" "+str(self.w)+" "+str(y)+" "+str(x))
#        self.editText.refresh()
        if x>self.x and x<self.x+self.w:
            if y>self.y and y<self.y+self.h:
                return True
            else:
                return False
        else:
            return False
    def event(self,event):
        row=self.cur_y
        col=self.cur_x
        self.editText.move(row,col)
        #确定窗口激活
        if self.onfocus():
#            self.editText.addstr(1,1,"hello")
#            self.editText.refresh()
            self.editText.move(row,col)
            if event==ord("\n"):
                pass
            elif event==curses.KEY_LEFT:
                col=col-1
                if col<=1:
                    col=1
            elif event==curses.KEY_RIGHT:
                col+=1
                if col>=self.w-1:
                    col=self.w-1
                if col>len(self.msg):
                    col=len(self.msg)+1
            elif event==127:
                if col>1:
                    col-=1
                    self.editText.delch(row,col)
                    self.msg=self.msg[0:col-1]+self.msg[col:]
            else:
                if col<self.w-1:
                    self.msg+=chr(event)
                    self.editText.addch(row,col,chr(event))
                    col+=1
            self.editText.move(row,col)   
            self.editText.refresh()
            self.cur_y=row
            self.cur_x=col 
