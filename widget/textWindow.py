import curses
from curses import ascii
from widget import color
class TextWindow:
    def __init__(self,h,w,y,x):
        self.h,self.w=h,w
        self.y,self.x=y,x
        self.__win=curses.newwin(h,w,y,x)
        self.__sub_y=self.y+2
        self.__sub_x=self.x+1
        self.__sub_w=self.w-2
        self.__sub_h=self.h-3
        self.__subwin=self.__win.subwin(self.__sub_h,self.__sub_w,self.__sub_y,self.__sub_x)
        self.__cur_x=1
        self.__cur_y=0
        self.__cur_choose=0
        self.__scroll=0
        self.__msg=[""]
        self.__top=[]
        self.__bottom=[]
        self.__func=None
        self.__editable=True
        self.__subWiget=[]
    def erase(self):
        self.__subwin.erase()
    def addstr(self,y,x,str):
        self.__win.addstr(y,x,str)
    def addWidght(self,widget):
        self.__subWidget.append(widget)
    def getCursor(self):
        return (self.y+self.__cur_y,self.x+self.__cur_x)
    def setCursor(self,y,x):
        curses.setsyx(self.y,self.x)
        curses.doupdate()
    def ungetmouse(self):
        curses.ungetmouse(1,self.__sub_x,self.__sub_y,0,1)
    def highlightLine(self):
        if self.__cur_choose==self.__cur_y:
            y,x=curses.getsyx()
            self.__subwin.addstr(self.__cur_y,1,self.__msg[self.__cur_y],color.Red)
            self.__subwin.refresh()
            curses.setsyx(y,x)
            curses.doupdate()
        else:
            self.unhighlightLine()
            y,x=curses.getsyx()
            self.__subwin.addstr(self.__cur_y,1,self.__msg[self.__cur_y],color.Red)
            self.__subwin.refresh()
            curses.setsyx(y,x)
            curses.doupdate()
            self.__cur_choose=self.__cur_y
    def unhighlightLine(self):
        y,x=curses.getsyx()
        self.__subwin.standend()
        self.__subwin.addstr(self.__cur_choose,1,self.__msg[self.__cur_choose])
        self.__subwin.refresh()
        curses.setsyx(y,x)
        curses.doupdate()
    def bind(self,func=None):
        self.__func=func
    def getText(self):
        return "".join(self.__msg)
    def getLineRow(self):
        return self.__cur_y
    def getLineText(self,line=None):
        text=None
        if line:
            try:
                text=self.__msg[line]
            except:
                text=None
        else:
            text=self.__msg[self.__cur_y]
        return text
    def setText(self,text):
        if isinstance(text,str):
            self.__msg=text.split("\n")
        else:
            self.__msg=text
        for i in range(len(self.__msg)):
            if i<self.__sub_h:
                self.__subwin.addstr(i,1,self.__msg[i])
            else:
                self.__bottom.append(self.__msg[i])
        self.__subwin.refresh()
    def box(self,w,h):
        self.__win.box(w,h)
    def refresh(self):
        self.__win.refresh()
    def clean(self):
        self.__cur_x=1
        self.__cur_y=0
        self.__cur_choose=0
        self.__scroll=0
        self.__msg=[""]
        self.__top=[]
        self.__bottom=[]
        self.__subwin.erase()
        self.__subwin.refresh()
#        self.__subwin.addstr(10,0,"ok")
        self.ungetmouse()
    def setEditable(self,editable):
        self.__editable=editable
    def onfocus(self):
        y,x=curses.getsyx()
        if x>=self.x and x<=self.x+self.w:
            if y>=self.y and y<=self.y+self.h:
                return True
            else:
                return False
        else:
            return False
    def insert_str(self,y,x,text):
        self.__subwin.insstr(y,x,txt)
    def __slide_down(self,row):
        if row<0:
            row=0
            if self.__scroll>0:
                self.__subwin.scroll(-1)
                self.__bottom.append(self.__msg[-1-len(self.__bottom)])
                if len(self.__top)>0:
                    txt=self.__top.pop()
                    self.insert_str(row,1,txt)
                self.__scroll-=1
        return row

    def __slide_up(self,row):
        if row>=self.__sub_h:
            self.__top.append(self.__msg[self.__scroll])
            row=self.__sub_h-1
            self.__subwin.scroll(1)
            if self.__bottom:
                txt=self.__bottom.pop()
                self.insert_str(row,1,txt)
#                self.__subwin.insstr(row,1,txt)
            self.__scroll+=1
        return row

    def move(self,row,col):
        self.__subwin.move(row,len(self.__msg[row+self.__scroll][:col-1].encode('gbk'))+1)   
    def event(self,event):
        curses.curs_set(1)
        row=self.__cur_y
        col=self.__cur_x
        self.__subwin.scrollok(True)
        #全屏滑动,滑动宽度为self.__sub_h
        self.__subwin.setscrreg(0,self.__sub_h-1)
        #确定窗口激活
        if self.onfocus():
            #首先移动光标到文本位置
            self.__subwin.move(row,col)
            if isinstance(event,int):
                if event==curses.KEY_UP:
                #如果实际行数大于0行数就减一
                    if row+self.__scroll>0:
                        row=row-1
                        row=self.__slide_down(row)
                #如果行数小于0行数就不变，滑动计数减一
                    if col>len(self.__msg[row+self.__scroll]):
                        col=len(self.__msg[row+self.__scroll])+1
                elif event==curses.KEY_DOWN:
                    if row+self.__scroll<len(self.__msg)-1:
                        row+=1
                        row=self.__slide_up(row)
                    if col>len(self.__msg[row+self.__scroll]):
                        col=len(self.__msg[row+self.__scroll])+1
                elif event==curses.KEY_LEFT:
                    col=col-1
                    if col<1 and row+self.__scroll>0:
                        row=row-1
                        row=self.__slide_down(row)
                        col=len(self.__msg[self.__scroll+row])
                    if col==0 and row+self.__scroll==0:
                        col=1
                elif event==curses.KEY_RIGHT:
                    if col<len(self.__msg[row+self.__scroll])+1 and col<self.__sub_w:
                        col+=1
                    if col>len(self.__msg[row+self.__scroll])+1 and row+self.__scroll+1<len(self.__msg):
                        row=row+1
                        row=self.__slide_up(row)
                        col=1
                    elif col>=len(self.__msg[row+self.__scroll])+1:
                        col=len(self.__msg[row+self.__scroll])+1
            else:
                if event=="\n":
                    row+=1
                    col=1 
                    row=self.__slide_up(row)
                    if len(self.__msg)<=row+self.__scroll:
                        self.__msg.append("")
                elif self.__editable and ord(event)==127:
                    try:
                        col-=1
                        if col<1 and row+self.__scroll>0:
                            row=row-1
                            if row<0:
                                row=0
                                if self.__scroll>0:
                                    self.__subwin.scroll(-1)
                                    if len(self.__top)>0:
                                        txt=self.__top.pop()
                                        self.__subwin.insstr(row,1,txt)
                                    self.__scroll-=1
                            col=len(self.__msg[self.__scroll+row])+1
                            tmp=self.__scroll+row
                            if len(self.__msg[row+self.__scroll][:col-1].encode('gbk'))+1>=self.__sub_w:
                                col=len(self.__msg[row+self.__scroll])
                                self.__subwin.delch(row,len(self.__msg[row+self.__scroll][:col-1].encode('gbk')))
                                self.__msg[tmp]=self.__msg[tmp][0:-1]
                            lens=len(self.__msg[tmp])
                            lens2=len(self.__msg[tmp+1])
                            if lens+lens2>=self.__sub_w:
                                self.__msg[tmp]=self.__msg[tmp]+self.__msg[tmp+1][0:self.__sub_w-lens-1]
                                self.__msg[tmp+1]=self.__msg[tmp+1][self.__sub_w-lens-1:]
                            else:
                                self.__msg[tmp]=self.__msg[tmp]+self.__msg[tmp+1]
                                self.__msg[tmp+1]=""
                            self.__subwin.deleteln()
                            if len(self.__msg[tmp+1])>0:
                                self.__subwin.addstr(row+1,1,self.__msg[tmp+1])
                            else:
                                del self.__msg[tmp+1]
                            self.__subwin.addstr(row,1,self.__msg[tmp])
                        elif col==0 and self.__scroll+row==0:
                            col=1
                        else:
                            pos=len(self.__msg[row+self.__scroll][:col-1].encode('gbk'))+1
                            if len(self.__msg[row+self.__scroll][col-1].encode('gbk'))==1:
                                self.__subwin.delch(row,pos)
                            elif len(self.__msg[row+self.__scroll][col-1].encode('gbk'))==2:
                                self.__subwin.delch(row,pos+1)
                                self.__subwin.delch(row,pos)
                            tmp=self.__msg[self.__scroll+row]
                            self.__msg[self.__scroll+row]=tmp[:col-1]+tmp[col:]
                    except:
                        pass
                elif self.__editable and not ascii.isctrl(event):
                    if len(self.__msg[row+self.__scroll].encode('gbk'))<col:
                        self.__msg[row+self.__scroll]+=event
                        self.__subwin.addstr(row,len(self.__msg[row+self.__scroll][:col-1].encode('gbk'))+1,event)
                    else:
                        tmp=self.__msg[row+self.__scroll]
                        self.__msg[row+self.__scroll]=tmp[0:col-1]+event+tmp[col-1:]
                        self.__subwin.insstr(row,len(self.__msg[row+self.__scroll][:col-1].encode('gbk'))+1,str(event))
                    col+=len(event)
                    if len(self.__msg[row+self.__scroll][:col-1].encode('gbk'))+1>=self.__sub_w:
                        col=1
                        row+=1
                        if row>=self.__sub_h:
                            self.__top.append(self.__msg[self.__scroll])
                            if len(self.__msg[row+self.__scroll-1])<self.__sub_w-1:                                    self.__subwin.scroll(1)
                            row=self.__sub_h-1
                            if self.__bottom:
                                txt=self.__bottom.pop()
                                self.__subwin.insstr(row,1,txt)
                            self.__scroll+=1
                        if len(self.__msg)<=row+self.__scroll:
                            self.__msg.append("")
#                else:
#                    if self.__func:
#                        self.__func(event)

#            self.__subwin.erase()
#            self.__subwin.addstr(11,0,str(len(self.__msg[row+self.__scroll])))
#            self.__subwin.addstr(10,0,str(self.__sub_w)
#            self.__subwin.addstr(1,0,str(len(self.__msg)))
#            self.__subwin.addstr(10,0,str(row))
#            self.__subwin.move(row,len(self.__msg[row+self.__scroll][:col-1].encode('gbk'))+1)   
            self.move(row,col)
            self.__subwin.refresh()
            self.__cur_y=row
            self.__cur_x=col 
            if self.__func:
                self.__func(event)
