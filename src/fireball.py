import pygame
import math


class Fireball:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.speed=50
        self.a=800
        self.life=1
        self.isY=False
        mx,my=pygame.mouse.get_pos()
        if (abs(mx-x)+abs(my-y)):
            self.isY=True
            self.rat=abs(mx-x)/(abs(mx-x)+abs(my-y))
            self.vx=self.speed*self.rat
            self.vy=self.speed*(1-self.rat)
            if mx-x<0:
                self.vx*=-1
            if my-y<0:
                self.vy*=-1
        else:
            self.vx=200
            self.vy=0
    def update(self,dt):
        self.x+=self.vx*dt
        self.y+=self.vy*dt
        if self.isY:
            if self.vx>0:
                self.vx+=self.a*self.rat*dt
            else:
                self.vx+=self.a*self.rat*dt*-1
            if self.vy>0:
                self.vy+=self.a*(1-self.rat)*dt
            else:
                self.vy+=self.a*(1-self.rat)*dt*-1
        else:
            self.vx+=self.a*dt
        if abs(self.vx)>1000 or abs(self.vy)>1000:
            self.life=0
    def draw(self,nowsurface):
        nowsurface.blit(self.img,(self.x-14,self.y-16))