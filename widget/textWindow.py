import curses
from curses import ascii
class TextWindow:
    def __init__(self,h,w,y,x):
        self.h,self.w=h,w
        self.y,self.x=y,x
        self.win=curses.newwin(h,w,y,x)
        self.sub_y=self.y+2
        self.sub_x=self.x+1
        self.sub_w=self.w-2
        self.sub_h=self.h-3
        self.subwin=self.win.subwin(self.sub_h,self.sub_w,self.sub_y,self.sub_x)
        self.cur_x=0
        self.cur_y=0
        self.cur_choose=0
        self.scroll=0
        self.msg=[""]
        self.top=[]
        self.bottom=[]
        self.editable=True
        self.func=None
        self.subWiget=[]
    def addstr(self,y,x,str):
        self.win.addstr(y,x,str)
        self.cur_x+=1
    def addWidght(self,widget):
        self.subWidget.append(widget)
    def getCursor(self):
        return (self.y+self.cur_y,self.x+self.cur_x)
    def setCursor(self,y,x):
        curses.setsyx(self.y,self.x)
        curses.doupdate()
    def highlightLine(self):
        if self.cur_choose==self.cur_y:
            y,x=curses.getsyx()
            curses.init_color(curses.COLOR_RED,1000,0,0)
            curses.init_pair(4,curses.COLOR_BLACK,curses.COLOR_RED)
            self.subwin.addstr(self.cur_y,1,self.msg[self.cur_y],curses.color_pair(4))
            self.subwin.refresh()
            curses.setsyx(y,x)
            curses.doupdate()
        else:
            self.unhighlightLine()
            y,x=curses.getsyx()
            curses.init_color(curses.COLOR_RED,1000,0,0)
            curses.init_pair(4,curses.COLOR_BLACK,curses.COLOR_RED)
            self.subwin.addstr(self.cur_y,1,self.msg[self.cur_y],curses.color_pair(4))
            self.subwin.refresh()
            curses.setsyx(y,x)
            curses.doupdate()
            self.cur_choose=self.cur_y
    def unhighlightLine(self):
        y,x=curses.getsyx()
        self.subwin.standend()
        self.subwin.addstr(self.cur_choose,1,self.msg[self.cur_choose])
        self.subwin.refresh()
        curses.setsyx(y,x)
        curses.doupdate()
    def bind(self,func=None):
        self.func=func
    def getText(self):
        return "".join(self.msg)
    def getLine(self):
        return self.cur_y
    def getLineText(self):
        return self.msg[self.cur_y]
    def setText(self,text):
        self.msg=text.split("\n")
        for i in range(len(self.msg)):
            if i<self.sub_h:
                self.subwin.addstr(i,1,self.msg[i])
            else:
                self.bottom.append(self.msg[i])
        self.subwin.refresh()
    def box(self,w,h):
        self.win.box(w,h)
    def refresh(self):
        self.win.refresh()
    def setEditable(self,editable):
        self.editable=editable
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
        curses.curs_set(1)
        row=self.cur_y
        col=self.cur_x
        self.subwin.scrollok(True)
        #全屏滑动,滑动宽度为self.sub_h
        self.subwin.setscrreg(0,self.sub_h-1)
        #确定窗口激活
        if self.onfocus():
            #首先移动光标到文本位置
            self.subwin.move(row,col)
            if isinstance(event,int):
                if event==curses.KEY_UP:
                #如果实际行数大于0行数就减一
                    if row+self.scroll>0:
                        row=row-1
                #如果行数小于0行数就不变，滑动计数减一
                        if row<0:
                            row=0
                            if self.scroll>0:
                                self.subwin.scroll(-1)
                                self.bottom.append(self.msg[-1-len(self.bottom)])
                                if len(self.top)>0:
                                    txt=self.top.pop()
                                    self.subwin.insstr(row,1,txt)
                                self.scroll-=1
                    if col>len(self.msg[row+self.scroll]):
                        col=len(self.msg[row+self.scroll])+1
                elif event==curses.KEY_DOWN:
                    if row+self.scroll<len(self.msg)-1:
                        row+=1
                    if row>=self.sub_h:
                        self.top.append(self.msg[self.scroll])
                        row=self.sub_h-1
                        self.subwin.scroll(1)
                        if self.bottom:
                            txt=self.bottom.pop()
                            self.subwin.insstr(row,1,txt)
                        self.scroll+=1
                    if col>len(self.msg[row+self.scroll]):
                        col=len(self.msg[row+self.scroll])+1
                elif event==curses.KEY_LEFT:
                    col=col-1
                    if col<1 and row+self.scroll>0:
                        row=row-1
                        if row<0:
                            row=0
                            if self.scroll>0:
                                self.subwin.scroll(-1)
                                self.bottom.append(self.msg[-1-len(self.bottom)])
                                if len(self.top)>0:
                                    txt=self.top.pop()
                                    self.subwin.insstr(row,1,txt)
                                self.scroll-=1
                        col=len(self.msg[self.scroll+row])
                    if col==0 and row+self.scroll==0:
                        col=1
                elif event==curses.KEY_RIGHT:
                    if col<len(self.msg[row+self.scroll])+1 and col<self.sub_w:
                        col+=1
                    if col>len(self.msg[row+self.scroll])+1 and row+self.scroll+1<len(self.msg):
                        row=row+1
                        if row>=self.sub_h:
                            self.subwin.scroll(1)
                            row=self.sub_h-1
                            self.top.append(self.msg[self.scroll])
                            row=self.sub_h-1
                            if self.bottom:
                                txt=self.bottom.pop()
                                self.subwin.insstr(row,1,txt)
                            self.scroll+=1
                        col=1
                    elif col>=len(self.msg[row+self.scroll])+1:
                        col=len(self.msg[row+self.scroll])+1
            else:
                if event=="\n":
                    row+=1
                    col=1 
                #如果行数大于滑动宽度就向下滑
                    if row>=self.sub_h:
                    #滑动时保存上部文本
                        self.top.append(self.msg[self.scroll])
                        row=self.sub_h-1
                        self.scroll+=1
                        self.subwin.scroll(1)
                    #如果下部保存有文本则显示
                        if self.bottom:
                            txt=self.bottom.pop()
                            self.subwin.insstr(row,1,txt)
                    #如果当前行数大于存储文本列表长度则添加文本
                    if len(self.msg)<=row+self.scroll:
                        self.msg.append("")
                elif ord(event)==127:
                    try:
                        col-=1
                        if col<1 and row+self.scroll>0:
                            row=row-1
                            if row<0:
                                row=0
                                if self.scroll>0:
                                    self.subwin.scroll(-1)
                                    if len(self.top)>0:
                                        txt=self.top.pop()
                                        self.subwin.insstr(row,1,txt)
                                    self.scroll-=1
                            col=len(self.msg[self.scroll+row])+1
                            tmp=self.scroll+row
                            if len(self.msg[row+self.scroll][:col-1].encode('gbk'))+1>=self.sub_w:
                                col=len(self.msg[row+self.scroll])
                                self.subwin.delch(row,len(self.msg[row+self.scroll][:col-1].encode('gbk')))
                                self.msg[tmp]=self.msg[tmp][0:-1]
                            lens=len(self.msg[tmp])
                            lens2=len(self.msg[tmp+1])
                            if lens+lens2>=self.sub_w:
                                self.msg[tmp]=self.msg[tmp]+self.msg[tmp+1][0:self.sub_w-lens-1]
                                self.msg[tmp+1]=self.msg[tmp+1][self.sub_w-lens-1:]
                            else:
                                self.msg[tmp]=self.msg[tmp]+self.msg[tmp+1]
                                self.msg[tmp+1]=""
                            self.subwin.deleteln()
                            if len(self.msg[tmp+1])>0:
                                self.subwin.addstr(row+1,1,self.msg[tmp+1])
                            else:
                                del self.msg[tmp+1]
                            self.subwin.addstr(row,1,self.msg[tmp])
                        elif col==0 and self.scroll+row==0:
                            col=1
                        else:
                            pos=len(self.msg[row+self.scroll][:col-1].encode('gbk'))+1
                            if len(self.msg[row+self.scroll][col-1].encode('gbk'))==1:
                                self.subwin.delch(row,pos)
                            elif len(self.msg[row+self.scroll][col-1].encode('gbk'))==2:
                                self.subwin.delch(row,pos+1)
                                self.subwin.delch(row,pos)
                            tmp=self.msg[self.scroll+row]
                            self.msg[self.scroll+row]=tmp[:col-1]+tmp[col:]
                    except:
                        pass
                elif self.editable and not ascii.isctrl(event):
                    if len(self.msg[row+self.scroll].encode('gbk'))<col:
                        self.msg[row+self.scroll]+=event
                        self.subwin.addstr(row,len(self.msg[row+self.scroll][:col-1].encode('gbk'))+1,event)
                    else:
                        tmp=self.msg[row+self.scroll]
                        self.msg[row+self.scroll]=tmp[0:col-1]+event+tmp[col-1:]
                        self.subwin.insstr(row,len(self.msg[row+self.scroll][:col-1].encode('gbk'))+1,str(event))
                    col+=len(event)
                    if len(self.msg[row+self.scroll][:col-1].encode('gbk'))+1>=self.sub_w:
                        col=1
                        row+=1
                        if row>=self.sub_h:
                            self.top.append(self.msg[self.scroll])
                            if len(self.msg[row+self.scroll-1])<self.sub_w-1:                                    self.subwin.scroll(1)
                            row=self.sub_h-1
                            if self.bottom:
                                txt=self.bottom.pop()
                                self.subwin.insstr(row,1,txt)
                            self.scroll+=1
                        if len(self.msg)<=row+self.scroll:
                            self.msg.append("")
                else:
                    if self.func:
                        self.func(event)
#            self.subwin.erase()
#            self.subwin.addstr(11,0,str(len(self.msg[row+self.scroll])))
#            self.subwin.addstr(12,0,str(col))
#            self.subwin.addstr(10,0,str(self.sub_w)
#            self.subwin.addstr(1,0,str(len(self.msg)))
#            self.subwin.addstr(10,0,str(row))
            self.subwin.move(row,len(self.msg[row+self.scroll][:col-1].encode('gbk'))+1)   
            self.subwin.refresh()
            self.cur_y=row
            self.cur_x=col       
