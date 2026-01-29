
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