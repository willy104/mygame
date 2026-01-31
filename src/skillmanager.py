import pygame
from skills import SKILLS
import math

class SkillManager:
    def __init__(self,id):
        self.skillname=SKILLS[id]["name"]
        self.cd=SKILLS[id]["cd"]
        self.dmg=SKILLS[id]["dmg"]
        self.Mamount=SKILLS[id]["amount"]
        self.atkspeed=SKILLS[id]["atkspeed"]
        self.aim=SKILLS[id]["aim"]
        self.type=SKILLS[id]["type"]
        self.cooling=0
        self.smallcd=0
        self.amount=0
    def skilluse(self,player):
        player.casting=True
        self.amount=self.Mamount
        self.cooling=self.cd
        self.smallcd=self.atkspeed
        if self.type=="movement":
            player.movement_skill_using=True
            dx=player.mx-player.rect.centerx
            dy=player.my-player.rect.centery
            D=math.hypot(dx,dy)
            if D>0:
                wx=(dx/D)
                wy=(dy/D)
                player.vx=wx*1600
                player.vy=wy*1600
            else:
                player.vx=1600
                player.vy=0
            self.angle=math.degrees(math.atan2(-player.vy,player.vx))
    def update(self,dt):
        if self.cooling>0:
            self.cooling-=dt
        if not self.smallcd==None and self.smallcd>0 :
            self.smallcd-=dt
            self.smallcd=max(0,self.smallcd)
        self.cooling = max(0, self.cooling)
            