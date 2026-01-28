import pygame

from player import Player 
from world import World
from targetmouselogo import TargetLogo

pygame.init()
pygame.mouse.set_visible(False)

clock=pygame.time.Clock()

winW,winH=960,640

screen=pygame.display.set_mode((winW,winH))
gameSurface=pygame.Surface((winW,winH))

pygame.display.set_caption("game")


#載入
playerimg=pygame.image.load("assets/image/character.png").convert()
playereye=pygame.image.load("assets/image/ceyes.png").convert_alpha()
particleimg=pygame.image.load("assets/image/particle1.png").convert_alpha()
fireballimg=pygame.image.load("assets/image/fireball.png").convert_alpha()
fireballparimg=pygame.image.load("assets/image/particle2.png").convert_alpha()
bounceballimg=pygame.image.load("assets/image/bounceball.png").convert_alpha()
targetimg=pygame.image.load("assets/image/targetlogo.png").convert_alpha()


world=World("assets/testmap1.tmx")


q,w,e=1,2,3
player=Player(32,480,q,w,e,playerimg,playereye,particleimg,fireballimg,fireballparimg,bounceballimg)
target=TargetLogo(targetimg)


dt=0
run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            break
    gameSurface.fill((119,221,255))
    player.update(dt,world.collision_rects)
    world.draw(gameSurface)
    mx,my=pygame.mouse.get_pos()
    player.draw(gameSurface,dt,mx,my)
    target.update(mx,my)
    target.draw(gameSurface)
    screen.blit(gameSurface,(0,0))
    pygame.display.flip()
    dt=clock.tick(60)/1000
pygame.quit()