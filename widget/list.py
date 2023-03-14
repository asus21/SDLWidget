from widget.textWindow import TextWindow
from widget import color
import curses
class ListWindow(TextWindow):
    def __init__(self,h,w,y,x):
        super().__init__(h,w,y,x)

    def insert_str(y,x,text):

        self._TextWindow__subwin.insstr(y,x,text[1])

    def setText(self,msg):
        y,x=curses.getsyx()
        curses.curs_set(0)
        self.__msg_mark=[x[0] for x in msg]
        self._TextWindow__msg=msg#[x[1] for x in msg]
        for i in range(len(msg)):
            if i>=len(msg)-self._TextWindow__sub_h:
                if msg[i][0]==0:
                    self._TextWindow__subwin.addstr(i,self._TextWindow__sub_w-len(self._TextWindow__msg[i][1]+":Friend"),self._TextWindow__msg[i][1]+":Friend",color.blue)
                elif msg[i][0]==1:
                    self._TextWindow__subwin.addstr(i-self._TextWindow__sub_h,1,"Me:")
            else:
                self._TextWindow__top.append(self._TextWindow__msg[i])
        self._TextWindow__subwin.refresh()
        curses.setsyx(y,x)
        curses.curs_set(1)

