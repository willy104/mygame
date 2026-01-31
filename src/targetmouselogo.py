import pygame

class TargetLogo:
    def __init__(self,img):
        self.x=0
        self.y=0
        self.img=img
    def update(self,mx,my):
        self.x=mx
        self.y=my
    def draw(self,nowsurface):
        self.rect=self.img.get_rect(center=(self.x,self.y))
        nowsurface.blit(self.img,self.rect)