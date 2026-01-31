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
        dx=mx-x
        dy=my-y
        self.D=math.hypot(dx,dy)
        self.wx=(dx/self.D)
        self.wy=(dy/self.D)
        if self.D>0:
            self.vx=self.wx*self.speed
            self.vy=self.wy*self.speed
        else:
            self.vx=self.speed
            self.vy=0
        self.angle=math.degrees(math.atan2(-self.vy,self.vx))
        self.a=a
        self.life=1
        if not bounce==None:
            self.bounce=bounce
    def draw_particles(self,dt,nowsurface):
        for p in particles[:]:
            p.update(dt)
            p.draw(nowsurface)
            if p.life<=0:
                particles.remove(p)
'''    def physic_bounce(self,pre_rect,tile):   暫時用不到
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
        self.angle=math.degrees(math.atan2(-self.vy,self.vx))'''
class Fireball(Projectile):
    def __init__(self,x,y,img,pimg,pimg2,collision_rect,a=2000):
        super().__init__(x,y,img,a)
        self.pimg=pimg
        self.pimg2=pimg2
        self.collision_rect=collision_rect
        self.r_img=pygame.transform.rotate(img,self.angle)
        self.r_rect=self.r_img.get_rect(center=(self.x,self.y))
        
    def update(self,dt):
        particles.append(Particle(self.x-3,self.y-3,random.uniform(-50,50),random.uniform(-50,50),0,random.uniform(0.3,0.5),self.pimg))
        self.x+=self.vx*dt
        self.y+=self.vy*dt
        self.r_rect.center=(self.x,self.y)
        if self.D>0:
            self.vx+=self.a*self.wx*dt
            self.vy+=self.a*self.wy*dt
        else:
            self.vx+=self.a*dt
        for tile in self.collision_rect:
            if self.r_rect.colliderect(tile):
                for i in range(10):
                    particles.append(Particle(self.x-3,self.y-3,random.uniform(-100,100),random.uniform(-100,100),0,random.uniform(0.5,0.8),self.pimg))
                    particles.append(Particle(self.x-3,self.y-3,random.uniform(-100,100),random.uniform(-100,100),0,random.uniform(0.5,0.8),self.pimg2))
                self.life=0
    def draw(self,nowsurface,dt):
        
        nowsurface.blit(self.r_img,self.r_rect.topleft)
        #pygame.draw.rect(nowsurface,(255,0,0),self.r_rect,2)
        #pygame.draw.circle(nowsurface, (0, 0, 0), (int(self.x), int(self.y)), 3)



class Bounceball(Projectile):
    def __init__(self,x,y,img,pimg,collision_rect,speed,bounce=5):
        super().__init__(x,y,img,0,bounce,speed)
        self.pimg=pimg
        self.collision_rect=collision_rect
    def update(self,dt):
        self.x+=self.vx*dt
        self.rect.centerx=self.x
        for tile in self.collision_rect:
            if self.rect.colliderect(tile):
                if self.vx>0:
                    self.rect.right=tile.left
                else:
                    self.rect.left=tile.right
                self.vx*=-1
                self.x=self.rect.centerx
                self.bounce-=1
                for _ in range(5):
                    particles.append(Particle(self.x-3,self.y-3,random.uniform(-50,50),random.uniform(-50,50),0,0.3,self.pimg))
                break
        
        self.y+=self.vy*dt
        self.rect.centery=self.y
        for tile in self.collision_rect:
            if self.rect.colliderect(tile):
                if self.vy>0:
                    self.rect.bottom=tile.top
                else:
                    self.rect.top=tile.bottom
                self.vy*=-1
                self.y=self.rect.centery
                self.bounce-=1
                for _ in range(5):
                    particles.append(Particle(self.x-3,self.y-3,random.uniform(-50,50),random.uniform(-50,50),0,0.3,self.pimg))
                break
        if self.bounce<=0:
            self.life=0
        self.angle=math.degrees(math.atan2(-self.vy,self.vx))
    def draw(self,nowsurface,dt):
        self.r_img=pygame.transform.rotate(self.img,self.angle)
        self.r_rect=self.r_img.get_rect(center=(self.rect.center))
        nowsurface.blit(self.r_img,self.rect.topleft)
        #pygame.draw.rect(nowsurface,(255,0,0),self.r_rect,2)
        #pygame.draw.circle(nowsurface, (255, 0, 0), (int(self.x), int(self.y)), 3)