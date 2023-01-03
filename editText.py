import curses
from curses import textpad
class EditText:
    def __init__(self,top,h,w,y,x):
        self.top=top
        self.h,self.w=h,w
        self.y,self.x=y,x
        self.boxText=top.subwin(h,w,y,x)
        self.editText=top.subwin(h-2,w-2,y+1,x+1)
        self.boxText.box(curses.ACS_VLINE,curses.ACS_HLINE)
#        self.setHint("ok")
        self.msg=""
        self.cur_y=0
        self.cur_x=0
    def highlight(self):
        self.boxText.attron(curses.A_BOLD)
        self.boxText.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.boxText.attroff(curses.A_BOLD)
        self.boxText.refresh()
    def unhighlight(self):
#        self.boxText.attrset(curses.A_BOLD)

        self.boxText.standend()
        self.boxText.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.boxText.refresh()
    def setHint(self,hint):
        curses.start_color()
        curses.init_color(curses.COLOR_RED,500,500,500)
        curses.init_pair(1,curses.COLOR_RED,0)
        self.editText.addstr(0,0,hint,curses.color_pair(1))
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
        row=self.cur_y
        col=self.cur_x
        self.editText.move(row,col)
        #确定窗口激活
        if self.onfocus():
            self.editText.move(row,col)
            if event==ord("\n"):
                pass
            elif event==curses.KEY_LEFT:
                col=col-1
                if col<=1:
                    col=1
            elif event==curses.KEY_RIGHT:
                col+=1
                if col>=self.w-3:
                    col=self.w-1
                if col>len(self.msg):
                    col=len(self.msg)+1
            elif event==127:
                if col>0:
                    col-=1
                    self.editText.delch(row,col)
                    self.msg=self.msg[0:col-1]+self.msg[col:]
            else:
                if col<self.w-3:
                    self.msg+=chr(event)
                    self.editText.addch(row,col,chr(event))
                    col+=1
            self.editText.move(row,col)   
            self.editText.refresh()
            self.cur_y=row
            self.cur_x=col
