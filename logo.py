import pygame, sys
import heapq
# import pathfind, threading

pygame.init()
clock = pygame.time.Clock()

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

hex

window = pygame.display.set_mode((800,600))

# print(pygame.image.load("/home/vekidev/Documents/bg.png").get_palette())
downrect = pygame.Surface((48,48))
downrect.fill((1,1,1)); downrect.set_colorkey((1,1,1))
pygame.draw.rect(downrect,(1,95,191),(0, 0, 48, 48),0,4)
downrectr = rot_center(downrect,45,window.get_width() / 2,window.get_height() / 2 + 8)

uprect = pygame.Surface((48,48))
uprect.fill((1,1,1)); uprect.set_colorkey((1,1,1))
pygame.draw.rect(uprect,(1,127,255),(0, 0, 48, 48),0,4)
uprectr = rot_center(uprect,45,window.get_width() / 2,window.get_height() / 2 - 8)

upangle, downangle = 45,90
nextangleup, nextangledown = 90, 135
upoffset, downoffset = 0,0
nextupoffset, nextdownoffset = -22,22

loading = True

blackout = pygame.Surface((1920,1080))
blackout.fill((0,0,0))
blackout.set_alpha(0)

loadtimer = 0
font = pygame.font.SysFont("Source Code Pro",16)

curalpha = 0

while True:
    dt = clock.tick(60) / 1000

    if loading: loadtimer += dt

    
    
    upangle += ((nextangleup - upangle) * 5) * dt
    if upangle >= nextangleup - 1 and loading:
        nextangleup += 45
    elif upangle >= nextangleup - 1 and not loading:
        curalpha += ((255 - curalpha) / 0.3) * dt
    # if upangle <= nextangleup + 1 and nextangleup == 45:
    #     nextangleup = 90

    downangle += ((nextangledown - downangle) * 5) * dt
    if downangle >= nextangledown - 1 and loading:
        nextangledown += 45

    downoffset += ((nextdownoffset - downoffset) * 4) * dt
    if downoffset >= nextdownoffset - 1 and loading and nextdownoffset == 22:
        nextdownoffset = 0
    if downoffset <= nextdownoffset + 1 and loading and nextdownoffset == 0:
        nextdownoffset = 22

    upoffset += ((nextupoffset - upoffset) * 4) * dt
    # print(nextupoffset,upoffset)
    if upoffset <= nextupoffset + 1 and loading and nextupoffset == -22:
        nextupoffset = 0
    if upoffset >= nextupoffset - 1 and loading and nextupoffset == 0:
        nextupoffset = -22


    # if downangle <= nextangledown + 1 and nextangledown == 90:
    #     nextangledown = 135

    # if oldgoal != pygame.Vector2(-1,-1): 
        # path = pathfind.shortest_path(tilemap,(1,1),(int(oldgoal.y),int(oldgoal.x)))
        # print(path)
    # else: path = (None,[])

    blackout.set_alpha(curalpha)

    if curalpha >= 250:
        curalpha = 255

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print(nextangleup,nextangledown)
            loading = False
            if nextangleup % 90 == 0: nextangleup += 45
            else: nextangleup += 90
            if nextangledown % 90 == 0: nextangledown += 45
            else: nextangledown += 90
            nextupoffset = 0
            nextdownoffset = 0
            loadtimer = 0


    window.fill((3,48,136))

    uprect.fill((1,1,1))
    pygame.draw.rect(uprect,(1,127,255),(0, 0, 48, 48),0,4)
    uprectr = rot_center(uprect,upangle,window.get_width() / 2,window.get_height() / 2 - 8)

    downrect.fill((1,1,1)); downrect.set_colorkey((1,1,1))
    pygame.draw.rect(downrect,(1,95,191),(0, 0, 48, 48),0,4)
    downrectr = rot_center(downrect,downangle,window.get_width() / 2,window.get_height() / 2 + 8)

    window.blit(downrectr[0],(downrectr[1][0],downrectr[1][1] + downoffset))
    window.blit(uprectr[0],(uprectr[1][0],uprectr[1][1] + upoffset))

    if loadtimer > 5:
        rendered = font.render("hold on tight",True,(1,127,255))
        window.blit(rendered,(window.get_width() / 2 - rendered.get_width() / 2,window.get_height() - font.get_height() - 4))

    window.blit(blackout,(0,0))
    

    pygame.display.flip()