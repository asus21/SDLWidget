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
register_againEdit_hint="Input your password again"
register_alert="Doesn't exists the user"
class RegisterWindow():
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
        #添加头部文字
        self.__subwin.addstr(0,int((self.__sub_w-len(register_text))/2),register_text)
        #文本提示
        self.__subwin.addstr(self.__sub_h//5+1,self.__sub_w//5,register_user)
        self.__subwin.addstr(2*self.__sub_h//5+1,self.__sub_w//5,register_password)
        self.__subwin.addstr(3*self.__sub_h//5+1,self.__sub_w//5,register_again)
        #输入框
        self.text_user=EditText(self.__subwin,3,30,self.__sub_y+self.__sub_h//5,self.__sub_x+self.__sub_w//5+len(register_user)+3)
        self.text_password=EditText(self.__subwin,3,30,self.__sub_y+2*self.__sub_h//5,self.__sub_x+self.__sub_w//5+len(register_password)+3)
        self.text_again=EditText(self.__subwin,3,30,self.__sub_y+3*self.__sub_h//5,self.__sub_x+self.__sub_w//5+len(register_again)+3)
        #设置输入框提示
        self.text_user.setHint(register_userEdit_hint)
        self.text_password.setHint(register_registerEdit_hint)
        self.text_again.setHint(register_againEdit_hint)
        #按钮
        self.button_sure=Label(self.__subwin,3,10,self.__sub_y+3*int(self.__sub_h/4),self.__sub_x+int(self.__sub_w/5))
        self.button_sure.setText(register_button_register)
        self.button_return=Label(self.__subwin,3,10,self.__sub_y+3*int(self.__sub_h/4),self.__sub_x+3*int(self.__sub_w/5))
        self.button_return.setText(register_button_return)
    def refresh(self):  
        self.__window.refresh()
        self.__subwin.refresh()
    def alert(self,alert):
        curses.init_pair(3,curses.COLOR_RED,0)
        self.__subwin.addstr(1,(self.__sub_w-len(alert))//2,alert,curses.color_pair(3))
        self.__subwin.refresh()
        y,x=curses.getsyx()
        time.sleep(2)
        curses.setsyx(y,x)
        self.__subwin.addstr(1,1," "*(self.__sub_w-2))
        self.__subwin.refresh()
    def setEnable(self,enable):
        self.__enable=enable
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
        if self.__count==0:
            curses.curs_set(1)
            self.__subwin.move(self.text_user.y,self.text_user.x)
            self.__subwin.refresh()
        elif self.__count==1:
            curses.curs_set(1)
            self.__subwin.move(self.text_password.y,self.text_password.x)
            self.__subwin.refresh()
        elif self.__count==2:
            curses.curs_set(1)
            self.__subwin.move(self.text_again.y,self.text_again.x)
            self.__subwin.refresh()
        elif self.__count==3:
            curses.curs_set(0)
            self.__subwin.move(self.button_sure.y,self.button_sure.x)
            self.__subwin.refresh()
        elif self.__count==4:
            curses.curs_set(0)
            self.__subwin.move(self.button_return.y,self.button_return.x)
            self.__subwin.refresh()
    def __event(self,event):
        if event!=curses.KEY_MOUSE:
            if event==curses.KEY_UP:
                self.__count-=1
                if self.__count<0:
                    self.__count=0
            elif event==curses.KEY_DOWN:
                self.__count+=1
                if self.__count>4:
                    self.__count=4    
            elif event==curses.KEY_LEFT:
                if self.__count==4:
                    self.__count=3
            elif event==curses.KEY_RIGHT:
                if self.__count==3:
                    self.__count=4
            self.__swift()
        self.text_user.event(event)
        self.text_password.event(event)
        self.text_again.event(event)
        self.button_sure.event(event)
        self.button_return.event(event)
        
        if self.text_user.isActive:
            self.__count=0
        elif self.text_password.isActive:
            self.__count=1
        elif self.text_again.isActive:
            self.__count=2
        elif self.button_sure.isActive:
            self.__count=3
        elif self.button_return.isActive:
            self.__count=4
        
    def event(self,event):
        if self.__enable:
            self.__event(event)

