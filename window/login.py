import curses
from widget.editText import EditText
from widget.label import Label
from widget import color
import json
import time
radio_h=0.6
radio_w=0.8
login_text="logining"
login_user="User:"
login_password="Password:"
login_button_register="Register"
login_button_login="Login"
login_userEdit_hint="Please input your account"
login_registerEdit_hint="Please input your password"
class LoginWindow():
    def __init__(self,h,w,y,x):
        self.h=h
        self.w=w
        self.y=y
        self.x=x
        self.__count=0
        self.__enable=True
        self.__func=None
        self.__sub_h=int(h*radio_h)
        self.__sub_w=int(w*radio_w)
        self.__sub_y=int((1-radio_h)/2*h)
        self.__sub_x=int((1-radio_w)/2*w)
        self.__window=curses.newwin(h,w,x,y)
        self.__subwin=self.__window.subwin(self.__sub_h,self.__sub_w,self.__sub_y,self.__sub_x)
        self.__subwin.box(".",".")
        self.__subwin.addstr(0,int((self.__sub_w-len(login_text))/2),login_text)
        self.__subwin.addstr(int(self.__sub_h/4),int(self.__sub_w/5),login_user)
        self.__subwin.addstr(2*int(self.__sub_h/4),int(self.__sub_w/5),login_password)
        self.text_user=EditText(self.__subwin,3,30,self.__sub_y+int(self.__sub_h/4)-1,self.__sub_x+int(self.__sub_w/5)+len(login_user)+3)
        self.text_password=EditText(self.__subwin,3,30,self.__sub_y+2*int(self.__sub_h/4)-1,self.__sub_x+int(self.__sub_w/5)+len(login_password)+3)
        self.text_user.setHint(login_userEdit_hint)
        self.text_password.setHint(login_registerEdit_hint)
        self.button_register=Label(self.__subwin,3,10,self.__sub_y+3*int(self.__sub_h/4),self.__sub_x+int(self.__sub_w/5))
        self.button_register.setText(login_button_register)
        self.button_login=Label(self.__subwin,3,10,self.__sub_y+3*int(self.__sub_h/4),self.__sub_x+3*int(self.__sub_w/5))
        self.button_login.setText(login_button_login)
    def refresh(self):  
        self.__window.refresh()
        self.__subwin.refresh()
    def alert(self,alert):
        self.__subwin.addstr(1,(self.__sub_w-len(alert))//2,alert,color.red)
        self.__subwin.refresh()
        y,x=curses.getsyx()
        time.sleep(2)
        curses.setsyx(y,x)
        self.__subwin.addstr(1,1," "*(self.__sub_w-2))
        self.__subwin.refresh()
    def setEnable(self,enable):
        self.__enable=enable
    def button_login_bind(self,func=None):
        self.button_login.bind(func)
    def button_register_bind(self,func=None):
        self.button_register.bind(func)
    def ungetmouse(self):
        curses.ungetmouse(1,self.text_user.x,self.text_user.y,0,1)
    def getText(self):
        data={"item":"verify",\
                "user":self.text_user.getText(),\
                "password":self.text_password.getText()} 
        return data
    def __swift(self):
        if self.__count==0:
            curses.curs_set(1)
            self.text_user.setfocus()
        elif self.__count==1:
            curses.curs_set(1)
            self.text_password.setfocus()
        elif self.__count==2:
            curses.curs_set(0)
            self.button_register.setfocus()
        elif self.__count==3:
            curses.curs_set(0)
            self.button_login.setfocus()
    def __event(self,event):
        if event!=curses.KEY_MOUSE:
            if event==curses.KEY_UP:
                self.__count-=1
                if self.__count<0:
                    self.__count=0
            elif event==curses.KEY_DOWN:
                self.__count+=1
                if self.__count>3:
                    self.__count=3
            elif event==curses.KEY_LEFT:
                if self.__count==3:
                    self.__count=2
            elif event==curses.KEY_RIGHT:
                if self.__count==2:
                    self.__count=3
            self.__swift()
        self.text_user.event(event)
        self.text_password.event(event)
        self.button_register.event(event)
        self.button_login.event(event)
        if self.text_user.isActive:
            self.__count=0
        elif self.text_password.isActive:
            self.__count=1
        elif self.button_register.isActive:
            self.__count=2
        elif self.button_login.isActive:
            self.__count=3
    def event(self,event):
        if self.__enable:
            self.__event(event)
