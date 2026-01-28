import pygame
from particle import Particle
from fireball import Fireball
from skills import SKILLS
from skillmanager import SkillManager
import math
import random


particles=[]
fireballs=[]
skill123=[]
#player
class Player:
    def __init__(self,x,y,pimage,eyeimg,particleimg,fireballimg,fireballpimg,s1,s2,s3):
        #position
        self.vx=0
        self.vy=0
        self.speed=200

        #img
        self.image=pimage
        self.eye=eyeimg
        self.fireball=fireballimg
        self.rect=self.image.get_rect(topleft=(x,y))
        self.fireballpimg=fireballpimg

        #else
        self.g=1200
        self.on_ground=False
        self.double_jump=False
        self.pimg=particleimg

        #skills
        self.q_cooldown=0
        self.q_amount=0
        self.q_smallcd=0
        skill123.append(SkillManager(1))
        skill123.append(SkillManager(2))
        skill123.append(SkillManager(3))
    def handle_input(self):
        keys=pygame.key.get_pressed()
        self.vx=0
        if keys[pygame.K_a]:
            self.vx=-self.speed
        if keys[pygame.K_d]:
            self.vx+=self.speed
        if keys[pygame.K_q] and skill123[0].cooling == 0:
            skill123[0].skilluse()
        if keys[pygame.K_w] and skill123[1].cooling == 0:
            skill123[1].skilluse()
        if keys[pygame.K_SPACE]:
            if self.on_ground or (self.double_jump and not self.space_down):
                for _ in range(20):
                    particles.append(Particle(self.rect.x+16,self.rect.y+32,random.uniform(-50,50),random.uniform(100,200),300,self.pimg))
                self.vy=-500
                self.space_down=True
                if not self.on_ground :
                    self.double_jump=False
        else:
            self.space_down=False
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
        if  abs(self.vy)>30 and not random.randint(0,4):
            particles.append(Particle(self.rect.x+16,self.rect.y+16,random.uniform(-30,30),random.uniform(-30,30),0,self.pimg))
    def update(self,dt,collision_rect):
        self.handle_input()
        self.move_x(dt,collision_rect)
        self.move_y(dt,collision_rect)
        for sk in skill123:
            sk.update(dt)
            if sk.smallcd==0 and sk.amount>0:
                sk.smallcd=sk.atkspeed
                sk.amount-=1
                fireballs.append(Fireball(self.rect.x+16,self.rect.y+16,self.fireball,self.fireballpimg))
    def draw(self,nowsurface,dt,mx,my):

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
        for f in fireballs[:]:
            f.update(dt)
            f.draw(nowsurface,dt)
            if f.life<=0:
                fireballs.remove(f)