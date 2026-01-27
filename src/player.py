import pygame
from particle import Particle
import math
import random
particles=[]
#player
class Player:
    def __init__(self,x,y,pimage,eyeimg,particleimg):
        self.vx=0
        self.vy=0
        self.speed=200
        self.image=pimage
        self.eye=eyeimg
        self.rect=self.image.get_rect(topleft=(x,y))
        self.g=1200
        self.on_ground=False
        self.double_jump=False
        self.pimg=particleimg
    def handle_input(self):
        keys=pygame.key.get_pressed()
        self.vx=0
        if keys[pygame.K_a]:
            self.vx=-self.speed
        if keys[pygame.K_d]:
            self.vx+=self.speed
        if keys[pygame.K_w]:
            if self.on_ground or (self.double_jump and not self.w_down):
                for _ in range(20):
                    particles.append(Particle(self.rect.x+16,self.rect.y+32,self.pimg))
                self.vy=-500
                self.w_down=True
                if not self.on_ground :
                    self.double_jump=False
        else:
            self.w_down=False
    def move_x(self,dt,collision_rect):
        self.rect.x+=self.vx*dt
        for tile in collision_rect:
            if self.rect.colliderect(tile):
                if self.vx>0:
                    self.rect.right=tile.left
                if self.vx<0:
                    self.rect.left=tile.right
    def move_y(self,dt,collision_rect):
        self.vy+=self.g*dt
        self.rect.y+=self.vy*dt
        self.on_ground=False

        for tile in collision_rect:
            if self.rect.colliderect(tile):
                if self.vy>0:
                    self.rect.bottom=tile.top
                    self.vy=0
                    self.on_ground=True
                    self.double_jump=True
                if self.vy<0:
                    self.rect.top=tile.bottom
                    self.vy=0
        if  (self.vy<-20 or self.vy>30) and not random.randint(0,4):
            particles.append(Particle(self.rect.x,self.rect.y,self.pimg))
    def update(self,dt,collision_rect):
        self.handle_input()
        self.move_x(dt,collision_rect)
        self.move_y(dt,collision_rect)
        
    def draw(self,nowsurface,dt):
        mx,my=pygame.mouse.get_pos()
        dx,dy=mx-self.rect.x-16,my-self.rect.y-16
        if dx>4:
            dx=4
        if dx<-4:
            dx=-4
        if dy>5:
            dy=5
        if dy<-7:
            dy=-7
        self.eyerect=self.eye.get_rect(center=(self.rect.x+16+dx,self.rect.y+16+dy))
        nowsurface.blit(self.image,self.rect)
        nowsurface.blit(self.eye,self.eyerect)
        for p in particles[:]:
            p.update(dt)
            p.draw(nowsurface)
            if p.life<=0:
                particles.remove(p)