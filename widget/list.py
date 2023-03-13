from widget.textWindow import TextWindow
from widget import color
class ListWindow(TextWindow):
    def __init__(self,h,w,y,x):
        super().__init__(h,w,y,x)

    def setText(self,msg):
        self.__msg_mark=[x[0] for x in msg]
        self._TextWindow__msg=[x[1] for x in msg]
        for i in range(len(msg)):
            if i<self._TextWindow__sub_h:
                if msg[i][0]==0:
                    
                    self._TextWindow__subwin.addstr(i,1,self._TextWindow__msg[i],color.red)
                elif msg[i][0]==1:
                    self._TextWindow__subwin.addstr(i,1,self._TextWindow__msg[i])
            else:
                self._TextWindow__bottom.append(self.__msg[i])
        self._TextWindow__subwin.refresh()
            

