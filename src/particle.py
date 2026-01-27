import pygame
import random

class Particle:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.vx=random.uniform(-50,50)
        self.vy=random.uniform(200,100)
        self.life=random.uniform(0.3, 0.5)
        self.img=img
    def update(self,dt):
        self.life-=dt
        self.x+=self.vx*dt
        self.y+=self.vy*dt
        self.vy-=dt*300
    def draw(self,nowsurface):
        nowsurface.blit(self.img,(self.x,self.y))