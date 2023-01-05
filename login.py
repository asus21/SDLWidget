import curses
from editText import EditText
from label import Label
class LoginWindow():
    def __init__(self,h,w,y,x):
        radio_h=0.6
        radio_w=0.8
        login_text="logining"
#        login_text=u"登录"
        login_user="user:"
        login_password="password:"
        login_register="register"
        self.h=h
        self.w=w
        self.y=y
        self.x=x
        self.sub_h=int(h*radio_h)
        self.sub_w=int(w*radio_w)
        self.sub_y=int((1-radio_h)/2*h)
        self.sub_x=int((1-radio_w)/2*w)
        self.window=curses.newwin(h,w,x,y)
#        self.window.box(".",".")
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
    def event(self,event):
        count=0
        if event==curses.KEY_UP:
            count-=1
            if count<0:
                count=0
        elif event==curses.KEY_DOWN:
            count+=1
            if count>3:
                count=3
        else:
            self.user_text.event(event)
            self.password_text.event(event)
            self.register_label.event(event)
            self.login_label.event(event)
