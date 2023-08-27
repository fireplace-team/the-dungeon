import pygame, sys
import heapq
# import pathfind, threading

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((800,600))

# tilemap = [
#     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
#     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
#     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
# ]

tilemap = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

# print(path)

oldstart = pygame.Vector2(-1,-1)
oldgoal = pygame.Vector2(-1,-1)

path = []

curset = False
curset1 = 0

while True:
    dt = clock.tick(75) / 1000
    
    # if oldgoal != pygame.Vector2(-1,-1): 
        # path = pathfind.shortest_path(tilemap,(1,1),(int(oldgoal.y),int(oldgoal.x)))
        # print(path)
    # else: path = (None,[])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if oldgoal != pygame.Vector2(-1,-1) and curset1 >= 2:
                if curset: tilemap[int(oldgoal.y)][int(oldgoal.x)] = 0
                else: tilemap[int(oldstart.y)][int(oldstart.x)] = 0
            if not curset: tilemap[pygame.mouse.get_pos()[1] // 40][pygame.mouse.get_pos()[0] // 40] = 3
            else: tilemap[pygame.mouse.get_pos()[1] // 40][pygame.mouse.get_pos()[0] // 40] = 4
            curset = not curset
            curset1 += 1 if curset1 < 2 else 0
            if not curset:
                oldgoal.x = pygame.mouse.get_pos()[0] // 40
                oldgoal.y = pygame.mouse.get_pos()[1] // 40
            else:
                oldstart.x = pygame.mouse.get_pos()[0] // 40
                oldstart.y = pygame.mouse.get_pos()[1] // 40

    window.fill((220,190,0))
    pygame.draw.rect(window,(0,255,0),(pygame.mouse.get_pos()[0] // 40 * 40,pygame.mouse.get_pos()[1] // 40 * 40,40,40))
   
        

    for y, row in enumerate(tilemap):
        
        for x, tile in enumerate(row):
            if tile == 1: pygame.draw.rect(window,(0,220,190),(x * 40,y * 40, 40, 40))
            if tile == 3: pygame.draw.rect(window,(255,0,0),(x * 40,y * 40, 40, 40))
            if tile == 4: pygame.draw.rect(window,(0,190,0),(x * 40,y * 40, 40, 40))
            pygame.draw.line(window,(0,0,0),(x * 40,0),(x * 40,window.get_height()),2)

        if y:
            # print("A")
            pygame.draw.line(window,(0,0,0),(0,y * 40),(window.get_width(),y * 40),2)
    
    # pygame.draw.rect(window,(0,255,0),(pygame.mouse.get_pos()[0] // 40 * 40,pygame.mouse.get_pos()[1] // 40 * 40,40,40))

    if len(path) != 0:
        # print(path[1])
        for i in path:
            pygame.draw.rect(window,(0,0,220),(i[1] * 40,i[0] * 40,40,40))

    pygame.display.flip()