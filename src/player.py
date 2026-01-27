import pygame

#player
class Player:
    def __init__(self,x,y,pimage):
        self.vx=0
        self.vy=0
        self.speed=200
        self.image=pimage
        self.rect=self.image.get_rect(topleft=(x,y))
        self.g=1200
        self.on_ground=False
    def handle_input(self):
        keys=pygame.key.get_pressed()
        self.vx=0
        if keys[pygame.K_a]:
            self.vx=-self.speed
        if keys[pygame.K_d]:
            self.vx+=self.speed
        if keys[pygame.K_w] and self.on_ground:
            self.vy=-500
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
                if self.vy<0:
                    self.rect.top=tile.bottom
                    self.vy=0
    def update(self,dt,collision_rect):
        self.handle_input()
        self.move_x(dt,collision_rect)
        self.move_y(dt,collision_rect)
    def draw(self,nowsurface):
        nowsurface.blit(self.image,self.rect)