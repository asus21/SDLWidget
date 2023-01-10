import curses
from widget.editText import EditText
from widget.label import Label
import json
radio_h=0.6
radio_w=0.8
login_text="logining"
#        login_text=u"登录"
login_user="user:"
login_password="password:"
login_register="register"

class LoginWindow():
    def __init__(self,h,w,y,x):
        self.h=h
        self.w=w
        self.y=y
        self.x=x
        self.count=0
        self.enable=True
        self.func=None
        self.sub_h=int(h*radio_h)
        self.sub_w=int(w*radio_w)
        self.sub_y=int((1-radio_h)/2*h)
        self.sub_x=int((1-radio_w)/2*w)
        self.window=curses.newwin(h,w,x,y)
        self.subwin=self.window.subwin(self.sub_h,self.sub_w,self.sub_y,self.sub_x)
        self.subwin.box(".",".")
        self.subwin.addstr(0,int((self.sub_w-len(login_text))/2),login_text)
        self.subwin.addstr(int(self.sub_h/4),int(self.sub_w/5),login_user)
        self.subwin.addstr(2*int(self.sub_h/4),int(self.sub_w/5),login_password)
        self.user_text=EditText(self.subwin,3,30,self.sub_y+int(self.sub_h/4)-1,self.sub_x+int(self.sub_w/5)+len(login_user)+3)
        self.password_text=EditText(self.subwin,3,30,self.sub_y+2*int(self.sub_h/4)-1,self.sub_x+int(self.sub_w/5)+len(login_password)+3)
        self.register_label=Label(self.subwin,3,10,self.sub_y+3*int(self.sub_h/4),self.sub_x+int(self.sub_w/5))
        self.register_label.setText(login_register)
        self.login_label=Label(self.subwin,3,10,self.sub_y+3*int(self.sub_h/4),self.sub_x+3*int(self.sub_w/5))
        self.login_label.setText(login_text)
    def refresh(self):  
        self.window.refresh()
        self.subwin.refresh()
    def setEnable(self,enable):
        self.enable=enable
    def bind(self,func=None):
        self.login_label.bind(func)
    def getText(self):
        data={"user":self.user_text.getText(),"password":self.password_text.getText()} 
        return json.dumps(data)
    def __event(self,event):
        if event!=curses.KEY_MOUSE:
            if event==curses.KEY_UP:
                self.count-=1
                if self.count<0:
                    self.count=0
            elif event==curses.KEY_DOWN:
                self.count+=1
                if self.count>3:
                    self.count=3
            if self.count==0:
                curses.curs_set(1)
                self.subwin.move(int(self.sub_h/4)-1,int(self.sub_w/5)+len(login_password)+4)
                self.subwin.refresh()
            elif self.count==1:
                curses.curs_set(1)
                self.subwin.move(2*int(self.sub_h/4)-1,int(self.sub_w/5)+len(login_password)+3)
                self.subwin.refresh()
            elif self.count==2:
                curses.curs_set(0)
                self.subwin.move(3*int(self.sub_h/4),int(self.sub_w/5))
                self.subwin.refresh()
            elif self.count==3:
                curses.curs_set(0)
                self.subwin.move(3*int(self.sub_h/4),3*int(self.sub_w/5))
                self.subwin.refresh()
        self.user_text.event(event)
        self.password_text.event(event)
        self.register_label.event(event)
        self.login_label.event(event)
        if self.user_text.isActive:
            self.count=0
        elif self.password_text.isActive:
            self.count=1
        elif self.register_label.isActive:
            self.count=2
        elif self.login_label.isActive:
            self.count=3
    def event(self,event):
        if self.enable:
            self.__event(event)
