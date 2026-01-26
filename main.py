import pygame
import pytmx

from pytmx.util_pygame import load_pygame
 
pygame.init()

clock=pygame.time.Clock()

winW,winH=960,640

screen=pygame.display.set_mode((winW,winH))
gameSurface=pygame.Surface((winW,winH))

pygame.display.set_caption("game")

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

#地圖
tmx_map = pytmx.load_pygame("testmap1.tmx")

collision_rects=[]
collision_layer=tmx_map.get_layer_by_name("collision")
for x,y,gid in collision_layer:
    if gid:
        rect=pygame.Rect(32*x,32*y,32,32)
        collision_rects.append(rect)

mapSurface=pygame.Surface((winW,winH),pygame.SRCALPHA)
for layer in tmx_map.visible_layers:
    if layer.name=="collision":
        continue
    if isinstance(layer,pytmx.TiledTileLayer):
        for x,y,gid in layer:
            if gid:
                tile=tmx_map.get_tile_image_by_gid(gid)
                mapSurface.blit(tile,(x*32,y*32))
#載入
playerimg=pygame.image.load("character.png")



player=Player(32,480,playerimg)
dt=0
run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            break
    
    player.update(dt,collision_rects)

    gameSurface.fill((119,221,255))
    gameSurface.blit(mapSurface,(0,0))
    player.draw(gameSurface)
    screen.blit(gameSurface,(0,0))
    pygame.display.flip()
    dt=clock.tick(60)/1000
pygame.quit()