import curses

class LoginWin():
    def __init__(self,h,w,y,x):
        radio_h=0.6
        radio_w=0.8
        login_text="logining"
        login_user="user:"
        login_password="password:"
        login_register="register:"
        self.sub_h=int(h*radio_h)
        self.sub_w=int(w*radio_w)
        self.window=curses.newwin(h,w,x,y)
        self.window.box(".",".")
        self.subwin=self.window.subwin(self.sub_h,self.sub_w,int((1-radio_h)/2*h),int((1-radio_w)/2*w))
        self.subwin.box(".",".")
        self.subwin.addstr(0,int((self.sub_w-len(login_text))/2),login_text)
        self.subwin.addstr(int(self.sub_h/4),int(self.sub_w/5),login_user)
        self.subwin.addstr(2*int(self.sub_h/4),int(self.sub_w/5),login_password)
        self.user_text=self.create_textpad(3,30,int(self.sub_h/4)-1,int(self.sub_w/5)+len(login_user)+3)
        self.password_text=self.create_textpad(3,30,2*int(self.sub_h/4)-1,int(self.sub_w/5)+len(login_password)+3)
    def create_textpad(self,h,w,y,x):
        textpad=self.subwin.derwin(h,w,y,x)
        textpad.box("|","-")
    
    def refresh(self):  
        self.window.refresh()
        self.subwin.refresh()


