import pygame
from particle import Particle
import math

particles=[]
class Fireball:
    def __init__(self,x,y,img,pimg):
        self.x=x
        self.y=y
        self.img=img
        self.speed=50
        self.a=2000
        self.life=1
        self.isY=False
        self.pimg=pimg
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
        self.angle=math.degrees(math.atan2(-self.vy,self.vx))
    def update(self,dt):
        particles.append(Particle(self.x-4,self.y-4,self.pimg))
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
        if abs(self.vx)>2000 or abs(self.vy)>2000:
            self.life=0
    def draw(self,nowsurface,dt):
        self.r_img=pygame.transform.rotate(self.img,self.angle)
        self.r_rect=self.r_img.get_rect(center=(self.x,self.y))
        nowsurface.blit(self.r_img,self.r_rect.topleft)
        for p in particles[:]:
            p.update(dt)
            p.draw(nowsurface)
            if p.life<=0:
                particles.remove(p)