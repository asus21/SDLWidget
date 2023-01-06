import curses
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
        self.scroll=0
        self.msg=[""]
        self.top=[]
        self.bottom=[]
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
        row=self.cur_y
        col=self.cur_x
        self.subwin.scrollok(True)
        #全屏滑动,滑动宽度为self.sub_h
        self.subwin.setscrreg(0,self.sub_h-1)
        #首先移动光标到文本位置
        self.subwin.move(row,col)
        #确定窗口激活
        if self.onfocus():
            if event==ord("\n"):
                row+=1
                col=1
                #如果行数大于滑动宽度就向下滑
                if row>=self.sub_h:
                    #滑动时保存上部文本
                    self.top.append(self.msg[self.scroll])
                    row=self.sub_h-1
                    self.subwin.scroll(1)
                    #如果下部保存有文本则显示
                    if self.bottom:
                        txt=self.bottom.pop()
                        self.subwin.insstr(row,1,txt)
                    self.scroll+=1
                    #如果当前行数大于存储文本列表长度则添加文本
                if len(self.msg)<=row+self.scroll:
                    self.msg.append("")
            elif event==curses.KEY_UP:
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
                if col>=len(self.msg[row+self.scroll])+1 and row+self.scroll+1<len(self.msg):
                    row=row+1
                    if row>=self.sub_h:
                        row=self.sub_h-1
                        self.top.append(self.msg[self.scroll])
                        row=self.sub_h-1
                        self.subwin.scroll(1)
                        if self.bottom:
                            txt=self.bottom.pop()
                            self.subwin.insstr(row,1,txt)
                        self.scroll+=1
                    col=1
                elif col>=len(self.msg[row+self.scroll])+1:
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
            elif event==127:
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
                    if col>=self.sub_w:
                        col=self.sub_w-1
                        self.subwin.delch(row,col)
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
                    self.subwin.delch(row,col)
                    tmp=self.msg[self.scroll+row]
                    self.msg[self.scroll+row]=tmp[:col-1]+tmp[col:]
            else:
                if len(self.msg)<=row+self.scroll:
                    self.msg.append(chr(event)) 
                else:
                    if len(self.msg[row+self.scroll])<col:
                        self.msg[row+self.scroll]+=chr(event)
                    else:
                        tmp=self.msg[row+self.scroll]
                        self.msg[row+self.scroll]=tmp[0:col-1]+chr(event)+tmp[col:]
                self.subwin.addch(row,col,chr(event))
                col+=1
                if col>=self.sub_w:
                    col=1
                    row+=1
                    if row>=self.sub_h:
                        self.top.append(self.msg[self.scroll])
                        row=self.sub_h-1
#                        self.subwin.scroll(1)
                        if self.bottom:
                            txt=self.bottom.pop()
                            self.subwin.insstr(row,1,txt)
                        self.scroll+=1
                    if len(self.msg)<=row+self.scroll:
                        self.msg.append("")
#            self.subwin.erase()
#            self.subwin.addstr(0,0,""+str(len(self.msg)))
#            self.subwin.addstr(1,0,""+str(len(self.bottom)))
#            self.subwin.addstr(2,0,""+str(len(self.top)))
            self.subwin.move(row,col)   
            self.subwin.refresh()
            self.cur_y=row
            self.cur_x=col       
