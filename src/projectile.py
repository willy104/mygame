import pygame
from particle import Particle
import math
import random

particles=[]

class Projectile:
    def __init__(self,x,y,img,a=0,bounce=None,speed=50):
        self.x=x
        self.y=y
        self.img=img
        self.speed=speed
        
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
        self.a=a
        self.life=1
        if not bounce==None:
            self.bounce=bounce
    def draw_particles(sefl,dt,nowsurface):
        for p in particles[:]:
            p.update(dt)
            p.draw(nowsurface)
            if p.life<=0:
                particles.remove(p)



class Fireball(Projectile):
    def __init__(self,x,y,img,pimg,a=2000):
        self.isY=False
        self.pimg=pimg
        super().__init__(x,y,img,a)
    def update(self,dt):
        particles.append(Particle(self.x-3,self.y-3,random.uniform(-50,50),random.uniform(-50,50),0,self.pimg))
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



class Bounceball(Projectile):
    def __init__(self,x,y,img,pimg,collision_rect,speed,bounce=4):
        super().__init__(x,y,img,0,bounce,speed)
        self.pimg=pimg
        self.collision_rect=collision_rect
        self.r_img=pygame.transform.rotate(self.img,self.angle)
        self.r_rect=self.r_img.get_rect(center=(self.x,self.y))
    def update(self,dt):
        self.r_rect.x+=self.vx*dt
        self.r_rect.y+=self.vy*dt
        for tile in self.collision_rect:
            if self.r_rect.colliderect(tile):
                dx=min(abs(self.r_rect.left-tile.right),abs(self.r_rect.right-tile.left))
                dy=min(abs(self.r_rect.top-tile.bottom),abs(self.r_rect.bottom-tile.top))
                self.bounce-=1
                if dx<dy:
                    if self.r_rect.left-tile.right <= 0:
                        self.r_rect.left=tile.right
                    else:
                        self.r_rect.right=tile.left
                    self.vx*=-1
                else:
                    if self.r_rect.top-tile.bottom <= 0:
                        self.r_rect.top=tile.bottom
                    else:
                        self.r_rect.bottom=tile.top
                    self.vy*=-1
        if self.bounce<=0:
            self.life=0
    def draw(self,nowsurface,dt):
        nowsurface.blit(self.r_img,self.r_rect.topleft)
        pygame.draw.rect(nowsurface,(255,0,0),self.r_rect,2)