import pygame
from particle import Particle
from projectile import Projectile
from projectile import Fireball
from projectile import Bounceball
from skills import SKILLS
from skillmanager import SkillManager
import math
import random


particles=[]
projectiles=[]
skill123=[]
skill_key=[pygame.K_q,pygame.K_w,pygame.K_e]
k_down=[False,False,False]
#player
class Player:
    def __init__(self,x,y,s1,s2,s3,pimage,eyeimg,p_yellow,proimg,p_red,bounceballimg,p_blue,p_orange):
        #position
        self.vx=0
        self.vy=0
        self.ax=0
        self.ay=0
        self.speed=200
        self.movement_skill_using=False
        #img
        self.image=pimage
        self.eye=eyeimg
        self.proimg=proimg
        self.rect=self.image.get_rect(topleft=(x,y))
        self.p_red=p_red
        self.bounceballimg=bounceballimg
        self.p_blue=p_blue
        #else
        self.g=1200
        self.on_ground=False
        self.double_jump=False
        self.p_yellow=p_yellow
        self.p_orange=p_orange
        self.q_down=False
        self.w_down=False
        self.e_down=False
        #skills
        self.q_cooldown=0
        self.q_amount=0
        self.q_smallcd=0
        skill123.append(SkillManager(s1))
        skill123.append(SkillManager(s2))
        skill123.append(SkillManager(s3))
        self.casting=False
    def handle_input(self):
        keys=pygame.key.get_pressed()
        if not self.movement_skill_using:
            self.vx=0
            if keys[pygame.K_a]:
                self.vx=-self.speed
            if keys[pygame.K_d]:
                self.vx+=self.speed

            if keys[pygame.K_SPACE]:
                if self.on_ground or (self.double_jump and not self.space_down):
                    for _ in range(20):
                        particles.append(Particle(self.rect.x+16,self.rect.y+32,random.uniform(-50,50),random.uniform(100,200),300,random.uniform(0.3,0.5),self.p_yellow))
                    self.vy=-500
                    self.space_down=True
                    if not self.on_ground :
                        self.double_jump=False
            else:
                self.space_down=False
            if not self.casting:
                for i in range(3):
                    if keys[skill_key[i]]:
                        
                        if skill123[i].cooling == 0 and k_down[i]==False:
                            skill123[i].skilluse(self)
                            k_down[i]=True
                            break
                    else:
                        k_down[i]=False
        
    def move_x(self,dt,collision_rect):
        self.vx+=self.ax*dt
        self.rect.x+=self.vx*dt
        for tile in collision_rect:
            if self.rect.colliderect(tile):
                if self.vx>0:
                    self.rect.right=tile.left
                if self.vx<0:
                    self.rect.left=tile.right
                if self.movement_skill_using:
                    self.vy=0
                break
    def move_y(self,dt,collision_rect):
        if self.movement_skill_using:
            self.vy+=self.ay*dt
        else:
            self.vy+=self.g*dt
        
        self.rect.y+=self.vy*dt
        self.on_ground=False

        for tile in collision_rect:
            if self.rect.colliderect(tile):
                if self.vy>0:
                    self.rect.bottom=tile.top
                    self.vy=16
                    self.on_ground=True
                    self.double_jump=True
                if self.vy<0:
                    self.rect.top=tile.bottom
                    self.vy=16
                if self.movement_skill_using:
                    self.vx=0
                break
        if  abs(self.vy)>30 and not random.randint(0,4):
            particles.append(Particle(self.rect.x+16,self.rect.y+16,random.uniform(-30,30),random.uniform(-30,30),0,random.uniform(0.3,0.5),self.p_yellow))

    def update(self,dt,collision_rect):
        self.mx,self.my=pygame.mouse.get_pos()
        self.handle_input()
        self.move_x(dt,collision_rect)
        self.move_y(dt,collision_rect)
        for sk in skill123:
            sk.update(dt)
            if sk.smallcd==0 and sk.amount>0:
                sk.smallcd=sk.atkspeed
                sk.amount-=1
                if sk.type=="projectile":
                    self.summon_projectile(sk.skillname,collision_rect)
                if sk.type=="movement" and sk.amount==0:
                    pass
                if sk.amount==0:
                    self.casting=False
                    if sk.type == "movement":
                        self.movement_skill_using = False
                        self.vx /= 5
                        self.vy /= 5
    def draw(self,nowsurface,dt):
        self.mx,self.my=pygame.mouse.get_pos()
        dx,dy=self.mx-self.rect.x-16,self.my-self.rect.y-16
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
        for f in projectiles[:]:
            f.update(dt)
            f.draw(nowsurface,dt)
            if f.life<=0:
                projectiles.remove(f)
        Projectile.draw_particles(self,dt,nowsurface)

    def summon_projectile(self,name,collision_rect):
        if name=="fireball":
            projectiles.append(Fireball(self.rect.x+16,self.rect.y+16,self.proimg,self.p_red,self.p_orange,collision_rect))
        if name=="bounceball":
            projectiles.append(Bounceball(self.rect.x+16,self.rect.y+16,self.bounceballimg,self.p_blue,collision_rect,500))
    
    def use_movement_skill(self,name):
        pass
