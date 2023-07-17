import pygame
import time
import random
import math
import sys
if sys.platform=='win32':
    ppi=112
else:
    ppi=382
class Object:
    g=10
    v_x=v_y=0
    p_x=p_y=0
    t=1
    w,h=0,0
    alpha=0.01
    alive=True
    screen=None
    def __init__(self,screen,v_x,v_y,ax=0,ay=0):
        self.v_x=v_x
        self.v_y=v_y
        self.ax=ax
        self.ay=ay
        self.screen=screen
        self.w,self.h=self.screen.get_size()
    def move(self):
        self.p_x+=self.v_x
        self.p_y+=self.v_y
    def rebonund(self):
        print("not implement")
    def collision(self,object):
        print("not implement")
    def update(self):
        self.move()
        self.rebonund()
        self.v_x+=self.ax
        self.v_y+=self.ay
        self.t+=1
  
class Ball(Object):
    def __init__(self,screen,v_x,v_y,r=0,ax=0,ay=0,color:list="red"):
        super().__init__(screen,v_x,v_y,ax,ay)
        self.refresh()
    def refresh(self):
        self.r=random.randint(int(10*ppi/328),int(20*ppi/328))
        self.color=(random.randint(150,255),random.randint(150,255),random.randint(150,255))
        self.p_x=random.randint(self.r,self.w-self.r)
        self.p_y=random.randint(self.r,self.h-self.r)
        self.t=random.randint(1,255/self.alpha)
    def rebonund(self):
        if self.p_x-self.r<0:
            self.v_x=-self.v_x
            self.p_x=self.r
        elif self.p_x+self.r>self.w:
            self.v_x=-self.v_x
            self.p_x=self.w-self.r
        if self.p_y-self.r<0:
            self.v_y=-self.v_y
            self.p_y=self.r
        elif self.p_y+self.r>self.h:
            self.v_y=-self.v_y
            self.p_y=self.h-self.r
    def collision(self,object):
        dist=math.sqrt((self.p_x-object.p_x)**2+(self.p_y-object.p_y)**2)
        if dist<self.r+object.r:
            tmpx=self.v_x
            tmpy=self.v_y
            self.v_x=(self.v_x*(self.r-object.r)+2*object.r*object.v_x)/(self.r+object.r)
            object.v_x=((object.v_x)*(object.r-self.r)+2*self.r*tmpx)/(self.r+object.r)  
            self.v_y=(self.v_y*(self.r-object.r)+2*object.r*object.v_y)/(self.r+object.r)
            object.v_y=((object.v_y)*(object.r-self.r)+2*self.r*tmpy)/(self.r+object.r)
    
    def show(self):    
        self.circle=pygame.Surface((2*self.r,2*self.r),pygame.SRCALPHA)
        pygame.draw.circle(self.circle,self.color+(255-self.alpha*self.t,),(self.r,self.r),self.r)
        self.screen.blit(self.circle,(self.p_x-self.r,self.p_y-self.r))
        self.update()
        if 255-self.alpha*self.t<50 or not self.alive:
            self.refresh()
            self.alive=True
        
    def drag(self,x,y):
        pass

class Screen(pygame.Surface):
    def __init__(self,screen:pygame.Surface):
        self.screen=screen
        super().__init__(screen.get_size(),pygame.SRCALPHA)
        
    def clash(self,Balls:list):
        n=len(Balls)
        for i in range(n):
            for j in range(i+1,n):
                Balls[i].collision(Balls[j])
    def center(self,Balls,x,y):
        for i in Balls:
            if i.p_x!=x and i.p_y!=y:
                vx=x-i.p_x
                vy=y-i.p_y
                vec=math.sqrt(vx**2+vy**2)
                temp_v=math.sqrt(i.v_x**2+i.v_y**2)
                i.v_x=temp_v*vx/vec
                i.v_y=temp_v*vy/vec
    def display(self):
        self.screen.blit(pygame.transform.smoothscale(self,self.screen.get_size()),(0,0))
        
class Menu:
    def __init__(self,screen:pygame.Surface):
        self.screen=screen
        self.item=[None]
        self.orient='horizon'
        self.arrow=pygame.image.load("arrow.png")
    def add_item(self,name,id=None,image:str=None,action=None):
        img=None
        rect:pygame.Rect=None
        if image:
            img=pygame.image.load(image)
            rect=img.get_rect()
        if id:
            if id>len(self.item):
                self.item=self.item+[None]*(id-len(self.item))
        else:
            try:
                self.item.index(None)
            except ValueError:
                self.item.append(None) 
            id=self.item.index(None)+1
        if self.item[id-1]==None:
            self.item[id-1]=(name,img,action,rect)
        else:
            raise RuntimeError('The order is occupied')   
    def handle_action(self,x,y):
        for item in self.item:
            func,rect=item[2],item[3]
            if rect.collidepoint(x,y):
                func()

    def display(self):
        pos_x,pos_y=pygame.mouse.get_pos()
        if(0<pos_x<=50 and 0<pos_y<=50):
            self.screen.blit(pygame.transform.smoothscale(self.arrow,(50,50)),(len(self.item)*50,0))
            for item in self.item:
                if item[1]==None:
                    font = pygame.font.SysFont('simsun', 20)
                    text = font.render(item[0], True, (255, 0, 0), (0, 0, 0))
                    self.screen.blit(text,(self.item.index(item)*50,10))
                else:
                    if(self.orient=='horizon'):
                        img:pygame.Surface=item[1]
                        img.set_colorkey((255,255,255,255))
                        self.screen.blit(pygame.transform.smoothscale(img,(50,50)),(self.item.index(item)*50,0))
        else:
            self.screen.blit(pygame.transform.smoothscale(self.arrow,(50,50)),(-10,0))
            

def main(screen):
    
    balls=[]
    n=50
    for i in range(n):
        balls.append(Ball(screen,random.randint(-1,1),random.randint(-1,1),ax=0,ay=0))
    iscenter=False
    x=y=0
    menu=Menu(screen)
    choice=0
    def change(x):
        global choice
        choice=x
    menu.add_item('add',image='add.png',action=choice)
    menu.add_item('remove',image='sub.png',action=lambda :choice)
    menu.add_item('drag',image='drag.png',action=lambda :choice)
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            elif ev.type==pygame.MOUSEBUTTONDOWN:
                x,y=ev.pos
                iscenter=True
            elif ev.type==pygame.MOUSEBUTTONUP:
                iscenter=False
            elif ev.type==pygame.MOUSEMOTION:
                x,y=ev.pos
        screen.fill('black')
        for i in balls:
            i.show()
        screen.clash(balls)
        menu.display()
        if iscenter:
            screen.center(balls,x,y)
        screen.display()
        pygame.display.flip()
        clock.tick(60)
      
              

pygame.init()
tmp=pygame.display.Info()
print(tmp)
screen=Screen(pygame.display.set_mode([tmp.current_w//2,tmp.current_h//2],pygame.RESIZABLE|pygame.SRCALPHA))
clock=pygame.time.Clock()
main(screen)
