import pygame
import random

class Particle:
    def __init__(self,x,y,vx,vy,g,life,img):
        self.x=x
        self.y=y
        self.vx=vx
        self.vy=vy
        self.g=g
        self.life=life
        self.img=img
    def update(self,dt):
        self.life-=dt
        self.x+=self.vx*dt
        self.y+=self.vy*dt
        self.vy-=dt*self.g
    def draw(self,nowsurface):
        nowsurface.blit(self.img,(self.x,self.y))