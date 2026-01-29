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
        self.rect = self.img.get_rect(center=(self.x, self.y))
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
    def physic_bounce(self,pre_rect,tile):
        nx,ny=0,0
        if pre_rect.right <= tile.left and self.rect.right >tile.left:
            self.rect.right=tile.left
            nx,ny= 1,0
        elif pre_rect.left >= tile.right and self.rect.left < tile.right:
            self.rect.left=tile.right
            nx,ny= -1,0
        elif pre_rect.top >= tile.bottom and self.rect.top < tile.bottom:
            self.rect.top=tile.bottom
            nx,ny= 0,1
        elif pre_rect.bottom <= tile.top and self.rect.bottom > tile.top:
            self.rect.bottom=tile.top
            nx,ny= 0,-1
                
        if nx == 0 and ny == 0:
            return

        #反彈計算
        dot = self.vx * nx + self.vy * ny
        self.vx = self.vx - 2 * dot * nx
        self.vy = self.vy - 2 * dot * ny
        # 同步位置
        self.x,self.y=self.rect.center
        self.angle=math.degrees(math.atan2(-self.vy,self.vx))
class Fireball(Projectile):
    def __init__(self,x,y,img,pimg,a=2000):
        self.isY=False
        self.pimg=pimg
        super().__init__(x,y,img,a)
    def update(self,dt):
        particles.append(Particle(self.x-3,self.y-3,random.uniform(-50,50),random.uniform(-50,50),0,random.uniform(0.3,0.5),self.pimg))
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
    def __init__(self,x,y,img,pimg,collision_rect,speed,bounce=20):
        super().__init__(x,y,img,0,bounce,speed)
        self.pimg=pimg
        self.collision_rect=collision_rect
        
    def update(self,dt):
        self.pre_rect=self.rect.copy()
        self.x+=self.vx*dt
        self.y+=self.vy*dt
        self.rect.center=(self.x,self.y)
        for tile in self.collision_rect:
            if self.rect.colliderect(tile):
                Projectile.physic_bounce(self,self.pre_rect,tile)
                self.bounce-=1
                for _ in range(5):
                    particles.append(Particle(self.x-3,self.y-3,random.uniform(-50,50),random.uniform(-50,50),0,0.3,self.pimg))
                break
        if self.bounce<=0:
            self.life=0
    def draw(self,nowsurface,dt):
        self.r_img=pygame.transform.rotate(self.img,self.angle)
        self.r_rect=self.r_img.get_rect(center=(self.rect.center))
        nowsurface.blit(self.r_img,self.r_rect.topleft)
        #pygame.draw.rect(nowsurface,(255,0,0),self.r_rect,2)