import pygame
import pytmx

from pytmx.util_pygame import load_pygame
from player import Player 
from world import World
pygame.init()

clock=pygame.time.Clock()

winW,winH=960,640

screen=pygame.display.set_mode((winW,winH))
gameSurface=pygame.Surface((winW,winH))

pygame.display.set_caption("game")


#載入
playerimg=pygame.image.load("assets/image/character.png")


world=World("assets/testmap1.tmx")
player=Player(32,480,playerimg)
dt=0
run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            break
    player.update(dt,world.collision_rects)
    gameSurface.fill((119,221,255))
    world.draw(gameSurface)
    player.draw(gameSurface)
    screen.blit(gameSurface,(0,0))
    pygame.display.flip()
    dt=clock.tick(60)/1000
pygame.quit()