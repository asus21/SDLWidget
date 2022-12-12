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
        self.subwin.setscrreg(0,self.sub_h-1)
        self.subwin.move(row,col)   
        if self.onfocus():
            if event==ord("\n"):
                row+=1
                col=1
                if row>=self.sub_h-1:
                    self.top.append(self.msg[self.scroll])
                    row=self.sub_h-1
                    self.subwin.scroll(1)
                    if self.bottom:
                        txt=self.bottom.pop()
                        self.subwin.insstr(row,1,txt)
                    self.scroll+=1
                if len(self.msg)<=row+self.scroll:
                    self.msg.append("")
            elif event==curses.KEY_UP:
                if row+self.scroll>0:
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
                    col=len(self.msg[self.scroll+row])+1
                if col==0 and row+self.scroll==0:
                    col=1
            elif event==curses.KEY_RIGHT:
                if col<len(self.msg[row+self.scroll])+1:
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
                            self.bottom.append(self.msg[-1-len(self.bottom)])
                            if len(self.top)>0:
                                txt=self.top.pop()
                                self.subwin.insstr(row,1,txt)
                            self.scroll-=1
                    col=len(self.msg[self.scroll+row])+1
                    tmp=self.msg[self.scroll+row]
                    self.msg[self.scroll+row]=tmp+self.msg[self.scroll+row+1]
                    if self.scroll+row!=0:
                        del self.msg[self.scroll+row+1]
                    self.subwin.deleteln()
                    self.subwin.addstr(row,1,self.msg[self.scroll+row])
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
                    self.msg[row+self.scroll]+=chr(event)
                self.subwin.addch(row,col,chr(event))
                col+=1
            self.subwin.move(row,col)   
            self.subwin.refresh()
            self.cur_y=row
            self.cur_x=col       
