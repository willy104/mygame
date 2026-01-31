import pygame

from player import Player 
from world import World
from targetmouselogo import TargetLogo

pygame.init()
pygame.mouse.set_visible(False)

clock=pygame.time.Clock()

winW,winH=960,640

screen=pygame.display.set_mode((winW,winH),pygame.RESIZABLE)
screen_w,screen_h=winW,winH

gameSurface=pygame.Surface((winW,winH))

pygame.display.set_caption("game")


#載入
playerimg=pygame.image.load("assets/image/character.png").convert()
playereye=pygame.image.load("assets/image/ceyes.png").convert_alpha()
fireballimg=pygame.image.load("assets/image/fireball.png").convert_alpha()
bounceballimg=pygame.image.load("assets/image/bounceball.png").convert_alpha()

targetimg=pygame.image.load("assets/image/targetlogo.png").convert_alpha()
p_red=pygame.image.load("assets/image/particle_red.png").convert_alpha()
p_orange=pygame.image.load("assets/image/particle_orange.png").convert_alpha()
p_yellow=pygame.image.load("assets/image/particle_yellow.png").convert_alpha()
p_blue=pygame.image.load("assets/image/particle_blue.png").convert_alpha()



world=World("assets/testmap1.tmx")


q,w,e=1,2,3
player=Player(32,480,q,w,e,playerimg,playereye,p_yellow,fireballimg,p_red,bounceballimg,p_blue,p_orange)
target=TargetLogo(targetimg)


dt=0
run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            break
        if event.type==pygame.VIDEORESIZE:
            screen_w,screen_h=event.w,event.h
            screen=pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
    gameSurface.fill((119,221,255))
    player.update(dt,world.collision_rects)
    world.draw(gameSurface)
    mx,my=pygame.mouse.get_pos()
    player.draw(gameSurface,dt)
    target.update(mx,my)
    target.draw(gameSurface)
    #縮放
    screen_scale=min(screen_w/winW,screen_h/winH)
    scaled_w=int(winW*screen_scale)
    scaled_h=int(winH*screen_scale)
    scaled_surface=pygame.transform.smoothscale(gameSurface,(scaled_w,scaled_h))
    x=(screen_w-scaled_w)//2
    y=(screen_h-screen_h)//2
    screen.fill((0,0,0))
    screen.blit(scaled_surface,(x,y))
    pygame.display.flip()
    dt=clock.tick(60)/1000
pygame.quit()