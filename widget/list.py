from widget.textWindow import TextWindow
from widget import color
import curses
class ListWindow(TextWindow):
    def __init__(self,h,w,y,x):
        super().__init__(h,w,y,x)

    def __add_send(self,row,msg,length=0): 
        self._TextWindow__subwin.addstr(row-length,1,"Me:"+msg,color.red)

    def __add_recv(self,row,msg,length=0):
        self._TextWindow__subwin.addstr(row-length,self._TextWindow__sub_w-len(msg+":Friend"),msg+":Friend",color.blue)

    def insert_str(self,y,x,text):
        '''重写父类插入字符串方法'''
        if text[0]==0:
            self.__add_recv(y,text[1])
        elif text[0]==1:
            self.__add_send(y,text[1])
    def move(self,row,col):
        '''重写父类移动光标方法'''
        self._TextWindow__subwin.move(row,len(self._TextWindow__msg[row+self._TextWindow__scroll][1][:col-1].encode('gbk'))+1)

    def setText(self,msg):
        '''重写父类设置文本方法'''
        curses.curs_set(0)
        self.__msg_mark=[x[0] for x in msg]
        self._TextWindow__msg=msg
        for i in range(len(msg)):
            length=len(msg)-self._TextWindow__sub_h
            if length<0:
                if msg[i][0]==0:
                    self.__add_recv(i,msg[i][1],0)
                elif msg[i][0]==1:
                    self.__add_send(i,msg[i][1],0)
                self._TextWindow__cur_y=i
                self._TextWindow__cur_x=1
            else:
                self._TextWindow__scroll=length
                if i<length:
                    self._TextWindow__top.append(self._TextWindow__msg[i])
                else:
                    if msg[i][0]==0:
                        self.__add_recv(i,msg[i][1],length)
                    elif msg[i][0]==1:
                        self.__add_send(i,msg[i][1],length)
                    self._TextWindow__cur_y=i-length
                    self._TextWindow__cur_x=1
        self._TextWindow__subwin.refresh()
        curses.curs_set(1)

