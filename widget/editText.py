import curses
class EditText:
    def __init__(self,top,h,w,y,x):
        self.top=top
        self.h,self.w=h,w
        self.y,self.x=y,x
        self.boxText=top.subwin(h,w,y,x)
        self.editText=top.subwin(h-2,w-2,y+1,x+1)
        self.boxText.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.light=False
        self.msg=""
        self.cur_y=0
        self.cur_x=0
        self.str_x=0
        self.isActive=False 
        self.hint=""
        self.isClear=False
    def highlight(self):
        y,x=curses.getsyx()
        curses.init_color(curses.COLOR_RED,1000,0,0)
        curses.init_pair(2,curses.COLOR_RED,0)
        self.boxText.attron(curses.A_BOLD|curses.color_pair(2))
        self.boxText.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.boxText.attroff(curses.A_BOLD|curses.color_pair(2))
        self.boxText.refresh()
        curses.setsyx(y,x)
        curses.doupdate()
    def unhighlight(self):
        y,x=curses.getsyx()
        self.boxText.standend()
        self.boxText.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.boxText.refresh()
        curses.setsyx(y,x)
        curses.doupdate()
    def setHint(self,hint):
        self.hint=hint
        self.showHint()
    def showHint(self):
        curses.init_color(curses.COLOR_RED,500,500,500)
        curses.init_pair(1,curses.COLOR_RED,0)
        self.editText.addstr(0,0,self.hint,curses.color_pair(1))
        self.editText.move(0,0)
        self.isClear=True
    def clearHint(self):
        if self.isClear:
            self.editText.clear()
            self.isClear=False
    def getText(self):
        return self.msg
    def refresh(self):
        if len(self.msg)==0:
            self.showHint()
        self.editText.refresh()
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
        row=self.cur_y
        col=self.cur_x
        self.editText.move(row,col)
        #确定窗口激活
        if self.onfocus():
            self.isActive=True
            if not self.light:
                self.highlight()
                self.light=True
            if isinstance(event,int):
                if event==curses.KEY_LEFT:
                    if col>0 and self.str_x>0:
                        self.str_x-=1
                        col=col-len(self.msg[self.str_x].encode('gbk'))
                elif event==curses.KEY_RIGHT:
                    if col<self.w-3 and self.str_x<len(self.msg):
                        col=col+len(self.msg[self.str_x].encode('gbk'))
                        self.str_x+=1
            else:
                if event=="\n":
                    pass
                elif ord(event)==127:
                    if col>0 and self.str_x>0:
                        self.str_x-=1
                        if len(self.msg[self.str_x].encode('gbk'))==1:
                            self.editText.delch(row,col-1)
                            col-=1
                        else:
                            self.editText.delch(row,col-1)
                            self.editText.delch(row,col-2)
                            col-=2
                        self.msg=self.msg[0:self.str_x]+self.msg[self.str_x+1:]
                else:
                    self.clearHint()
                    if col<self.w-3:
                        if len(self.msg.encode('gbk'))+len(event.encode('gbk'))<self.w-3:
                            if self.str_x<len(self.msg):
                                self.msg=self.msg[0:self.str_x]+event+self.msg[self.str_x:]
                                self.editText.insstr(row,col,event)
                                col+=len(event.encode('gbk'))
                                self.str_x+=1
                            else:
                                self.msg+=event
                                self.editText.addstr(row,col,event)
                                col+=len(event.encode('gbk'))
                                self.str_x+=1
#            self.editText.addstr(0,0,str(col)+" "+str(row))
            self.editText.move(row,col)   
            self.refresh()
            self.cur_y=row
            self.cur_x=col
        else:
            self.isActive=False
            if self.light:
                self.unhighlight()
                self.light=False
