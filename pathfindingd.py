import pygame, sys
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import AStarFinder

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

matrix = [[1 - i for i in row] for row in tilemap]

grid = Grid(matrix=matrix)

finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

# nodemap = [
#     [Node(bool(i),pygame.Vector2(x,y)) for x, i in enumerate(row)] for y, row in enumerate(tilemap)
# ]

# print(path)

oldstart = pygame.Vector2(-1,-1)
oldgoal = pygame.Vector2(-1,-1)

path = []

curset = False
curset1 = 0

while True:
    # pygame.display.set_icon(window)
    dt = clock.tick(10) / 1000
    
    if oldgoal != pygame.Vector2(-1,-1) and oldstart != pygame.Vector2(-1,-1): 
        try:
            end = grid.node(int(oldgoal.x),int(oldgoal.y))
            start = grid.node(int(oldstart.x), int(oldstart.y))
            if len(path) == 0: path, runs = finder.find_path(start, end, grid)
        except:
            pass

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

            path = []
            # if oldgoal != pygame.Vector2(-1,-1) and oldstart != pygame.Vector2(-1,-1): 
                
                # print(path)

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
            # print(i)
            pygame.draw.rect(window,(0,0,220),(i.x * 40,i.y * 40,40,40))

    pygame.display.flip()