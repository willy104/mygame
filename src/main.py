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
pointing_arrow=pygame.image.load("assets/image/pointer.png").convert_alpha()
fireballimg=pygame.image.load("assets/image/fireball.png").convert_alpha()
bounceballimg=pygame.image.load("assets/image/bounceball.png").convert_alpha()
lanceimg=pygame.image.load("assets/image/lance.png").convert_alpha()

skillbarimg=pygame.image.load("assets/image/skillbar.png").convert_alpha()


fireballicon=pygame.image.load("assets/image/fireballicon.png").convert_alpha()
bounceballicon=pygame.image.load("assets/image/bounceballicon.png").convert_alpha()
dashicon=pygame.image.load("assets/image/dashicon.png").convert_alpha()
lanceicon=pygame.image.load("assets/image/lanceicon.png").convert_alpha()

targetimg=pygame.image.load("assets/image/targetlogo.png").convert_alpha()
p_red=pygame.image.load("assets/image/particle_red.png").convert_alpha()
p_orange=pygame.image.load("assets/image/particle_orange.png").convert_alpha()
p_yellow=pygame.image.load("assets/image/particle_yellow.png").convert_alpha()
p_blue=pygame.image.load("assets/image/particle_blue.png").convert_alpha()
p_green=pygame.image.load("assets/image/particle_green.png").convert_alpha()
p_gray=pygame.image.load("assets/image/particle_gray1.png").convert_alpha()
Colors={
    "red":p_red,
    "orange":p_orange,
    "yellow":p_yellow,
    "green":p_green,
    "blue":p_blue,
    "gray":p_gray
    }

skillimg={
    "pointing_arrowimg":pointing_arrow,
    "playerimg":playerimg,
    "playereyeimg":playereye,
    "fireball":fireballimg,
    "bounceball":bounceballimg,
    "lance":lanceimg}
world=World("assets/testmap1.tmx")


q,w,e=1,4,3
player=Player(32,480,q,w,e,skillimg,Colors)
target=TargetLogo(targetimg)

icnos=[fireballicon,bounceballicon,dashicon,lanceicon]

skillbar_base=pygame.Surface((184,64))
skillbar_base.blit(skillbarimg,(0,0))
skillbar_base.blit(icnos[q-1],(4,4))
skillbar_base.blit(icnos[w-1],(64,4))
skillbar_base.blit(icnos[e-1],(124,4))

skillbar=pygame.Surface((184,64))


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
    skillbar.blit(skillbar_base,(0,0))
    skillbar.blit(player.skill_cd_surface,(0,0))
    gameSurface.blit(skillbar,(0,578))
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