import curses
from widget.editText import EditText
from widget.label import Label
import json
import time
radio_h=0.6
radio_w=0.8
login_text="logining"
login_user="User:"
login_password="Password:"
login_button_register="Register"
login_button_login="Login"
login_userEdit_hint="please input your account"
login_registerEdit_hint="please input your password"
login_alert="doesn't exists the user"
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
        self.user_text.setHint(login_userEdit_hint)
        self.password_text.setHint(login_registerEdit_hint)
        self.button_register=Label(self.subwin,3,10,self.sub_y+3*int(self.sub_h/4),self.sub_x+int(self.sub_w/5))
        self.button_register.setText(login_button_register)
        self.button_login=Label(self.subwin,3,10,self.sub_y+3*int(self.sub_h/4),self.sub_x+3*int(self.sub_w/5))
        self.button_login.setText(login_button_login)
    def refresh(self):  
#        self.__swift()
        self.window.refresh()
        self.subwin.refresh()
    def alert(self,alert):
        curses.init_pair(3,curses.COLOR_RED,0)
        self.subwin.addstr(1,(self.sub_w-len(alert))//2,alert,curses.color_pair(3))
        self.subwin.refresh()
        y,x=curses.getsyx()
        time.sleep(2)
        curses.setsyx(y,x)
        self.subwin.addstr(1,1," "*(self.sub_w-2))
        self.subwin.refresh()
    def setEnable(self,enable):
        self.enable=enable
    def button_login_bind(self,func=None):
        self.button_login.bind(func)
    def button_register_bind(self,func=None):
        self.button_register.bind(func)
    def ungetmouse(self):
        curses.ungetmouse(1,self.user_text.x,self.user_text.y,0,1)
    def getText(self):
        data={"user":self.user_text.getText(),"password":self.password_text.getText()} 
        return data
    def __swift(self):
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
            elif event==curses.KEY_LEFT:
                if self.count==3:
                    self.count=2
            elif event==curses.KEY_RIGHT:
                if self.count==2:
                    self.count=3
            self.__swift()
        self.user_text.event(event)
        self.password_text.event(event)
        self.button_register.event(event)
        self.button_login.event(event)
        if self.user_text.isActive:
            self.count=0
        elif self.password_text.isActive:
            self.count=1
        elif self.button_register.isActive:
            self.count=2
        elif self.button_login.isActive:
            self.count=3
    def event(self,event):
        if self.enable:
            self.__event(event)
