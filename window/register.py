import curses
from widget.editText import EditText
from widget.label import Label
import json
import time
radio_h=0.8
radio_w=0.8
register_text="registering"
register_user="User:"
register_password="Password:"
register_again="Again:"
register_button_register="Sure"
register_button_return="Return"
register_userEdit_hint="Please input your account"
register_registerEdit_hint="Please input your password"
register_againEdit_hint="Again input your password"
register_alert="Doesn't exists the user"
class RegisterWindow():
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
        #添加头部文字
        self.subwin.addstr(0,int((self.sub_w-len(register_text))/2),register_text)
        #文本提示
        self.subwin.addstr(self.sub_h//5+1,self.sub_w//5,register_user)
        self.subwin.addstr(2*self.sub_h//5+1,self.sub_w//5,register_password)
        self.subwin.addstr(3*self.sub_h//5+1,self.sub_w//5,register_again)
        #输入框
        self.text_user=EditText(self.subwin,3,30,self.sub_y+self.sub_h//5,self.sub_x+self.sub_w//5+len(register_user)+3)
        self.text_password=EditText(self.subwin,3,30,self.sub_y+2*self.sub_h//5,self.sub_x+self.sub_w//5+len(register_password)+3)
        self.text_again=EditText(self.subwin,3,30,self.sub_y+3*self.sub_h//5,self.sub_x+self.sub_w//5+len(register_again)+3)
        #设置输入框提示
        self.text_user.setHint(register_userEdit_hint)
        self.text_password.setHint(register_registerEdit_hint)
        self.text_again.setHint(register_againEdit_hint)
        #按钮
        self.button_sure=Label(self.subwin,3,10,self.sub_y+3*int(self.sub_h/4),self.sub_x+int(self.sub_w/5))
        self.button_sure.setText(register_button_register)
        self.button_return=Label(self.subwin,3,10,self.sub_y+3*int(self.sub_h/4),self.sub_x+3*int(self.sub_w/5))
        self.button_return.setText(register_button_return)
    def refresh(self):  
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
    def button_sure_bind(self,func=None):
        self.button_sure.bind(func)
    def button_return_bind(self,func=None):
        self.button_return.bind(func)
    def ungetmouse(self):
        curses.ungetmouse(1,self.text_user.x,self.text_user.y,0,1)
    def getData(self):
        data={"user":self.text_user.getText(),\
              "password":self.text_password.getText(),\
              "again":self.text_again.getText()} 
        return data
    def __swift(self):
        if self.count==0:
            curses.curs_set(1)
            self.subwin.move(self.text_user.y,self.text_user.x)
            self.subwin.refresh()
        elif self.count==1:
            curses.curs_set(1)
            self.subwin.move(self.text_password.y,self.text_password.x)
            self.subwin.refresh()
        elif self.count==2:
            curses.curs_set(1)
            self.subwin.move(self.text_again.y,self.text_again.x)
            self.subwin.refresh()
        elif self.count==3:
            curses.curs_set(0)
            self.subwin.move(self.button_sure.y,self.button_sure.x)
            self.subwin.refresh()
        elif self.count==4:
            curses.curs_set(0)
            self.subwin.move(self.button_return.y,self.button_return.x)
            self.subwin.refresh()
    def __event(self,event):
        if event!=curses.KEY_MOUSE:
            if event==curses.KEY_UP:
                self.count-=1
                if self.count<0:
                    self.count=0
            elif event==curses.KEY_DOWN:
                self.count+=1
                if self.count>4:
                    self.count=4    
            elif event==curses.KEY_LEFT:
                if self.count==4:
                    self.count=3
            elif event==curses.KEY_RIGHT:
                if self.count==3:
                    self.count=4
            self.__swift()
        self.text_user.event(event)
        self.text_password.event(event)
        self.text_again.event(event)
        self.button_sure.event(event)
        self.button_return.event(event)
        
        if self.text_user.isActive:
            self.count=0
        elif self.text_password.isActive:
            self.count=1
        elif self.text_again.isActive:
            self.count=2
        elif self.button_sure.isActive:
            self.count=3
        elif self.button_return.isActive:
            self.count=4
        
    def event(self,event):
        if self.enable:
            self.__event(event)

