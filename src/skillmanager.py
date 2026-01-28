import pygame
from skills import SKILLS


class SkillManager:
    def __init__(self,id):
        self.skillname=SKILLS[id]["name"]
        self.cd=SKILLS[id]["cd"]
        self.dmg=SKILLS[id]["dmg"]
        self.Mamount=SKILLS[id]["amount"]
        self.atkspeed=SKILLS[id]["atkspeed"]
        self.cooling=0
        self.smallcd=0
        self.amount=0
    def skilluse(self):
        self.amount=self.Mamount
        self.cooling=self.cd
        self.smallcd=self.atkspeed
    def update(self,dt):
        if self.cooling>0:
            self.cooling-=dt
        if self.smallcd>0:
            self.smallcd-=dt

        self.cooling = max(0, self.cooling)
        if not self.smallcd==None:
            self.smallcd=max(0,self.smallcd)
        