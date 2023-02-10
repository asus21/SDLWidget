import curses
class EditText:
    def __init__(self,top,h,w,y,x):
        self.top=top
        self.h,self.w=h,w
        self.y,self.x=y,x
        self.__boxText=top.subwin(h,w,y,x)
        self.__editText=top.subwin(h-2,w-2,y+1,x+1)
        self.__boxText.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.__light=False
        self.__msg=""
        self.__cur_y=0
        self.__cur_x=0
        self.__str_x=0
        self.__isActive=False 
        self.__hint=""
        self.__isClear=False
    def highlight(self):
        y,x=curses.getsyx()
        curses.init_pair(2,curses.COLOR_RED,0)
        self.__boxText.attron(curses.A_BOLD|curses.color_pair(2))
        self.__boxText.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.__boxText.attroff(curses.A_BOLD|curses.color_pair(2))
        self.__boxText.refresh()
        curses.setsyx(y,x)
        curses.doupdate()
    @property
    def isActive(self):
        return self.__isActive
    def unhighlight(self):
        y,x=curses.getsyx()
        self.__boxText.standend()
        self.__boxText.box(curses.ACS_VLINE,curses.ACS_HLINE)
        self.__boxText.refresh()
        curses.setsyx(y,x)
        curses.doupdate()
    def setHint(self,hint):
        self.__hint=hint
        self.showHint()
    def showHint(self):
        curses.init_color(curses.COLOR_WHITE,500,500,500)
        curses.init_pair(1,curses.COLOR_WHITE,0)
        self.__editText.addstr(0,0,self.__hint,curses.color_pair(1))
        self.__editText.move(0,0)
        self.__isClear=True
        curses.init_color(curses.COLOR_WHITE,1000,1000,1000)
    def clearHint(self):
        if self.__isClear:
            self.__editText.clear()
            self.__isClear=False
    def getText(self):
        return self.__msg
    def refresh(self):
        if len(self.__msg)==0:
            self.showHint()
        self.__editText.refresh()
    def setfocus(self):
        self.__editText.move(self.__cur_y,self.__cur_x)
        self.refresh()
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
        row=self.__cur_y
        col=self.__cur_x
        self.__editText.move(row,col)
        #确定窗口激活
        if self.onfocus():
            self.__isActive=True
            if not self.__light:
                self.highlight()
                self.__light=True
            if isinstance(event,int):
                if event==curses.KEY_LEFT:
                    if col>0 and self.__str_x>0:
                        self.__str_x-=1
                        col=col-len(self.__msg[self.__str_x].encode('gbk'))
                elif event==curses.KEY_RIGHT:
                    if col<self.w-3 and self.__str_x<len(self.__msg):
                        col=col+len(self.__msg[self.__str_x].encode('gbk'))
                        self.__str_x+=1
            else:
                if event=="\n":
                    pass
                elif ord(event)==127:
                    if col>0 and self.__str_x>0:
                        self.__str_x-=1
                        if len(self.__msg[self.__str_x].encode('gbk'))==1:
                            self.__editText.delch(row,col-1)
                            col-=1
                        else:
                            self.__editText.delch(row,col-1)
                            self.__editText.delch(row,col-2)
                            col-=2
                        self.__msg=self.__msg[0:self.__str_x]+self.__msg[self.__str_x+1:]
                else:
                    self.clearHint()
                    if col<self.w-3:
                        if len(self.__msg.encode('gbk'))+len(event.encode('gbk'))<self.w-3:
                            if self.__str_x<len(self.__msg):
                                self.__msg=self.__msg[0:self.__str_x]+event+self.__msg[self.__str_x:]
                                self.__editText.insstr(row,col,event)
                                col+=len(event.encode('gbk'))
                                self.__str_x+=1
                            else:
                                self.__msg+=event
                                self.__editText.addstr(row,col,event)
                                col+=len(event.encode('gbk'))
                                self.__str_x+=1
#            self.__editText.addstr(0,0,str(col)+" "+str(row))
            self.__editText.move(row,col)   
            self.refresh()
            self.__cur_y=row
            self.__cur_x=col
        else:
            self.__isActive=False
            if self.__light:
                self.unhighlight()
                self.__light=False
