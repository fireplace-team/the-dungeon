import pygame, sys, math, random
import time, weapons
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((720,480),pygame.RESIZABLE)
window = pygame.Surface((720,480))
pygame.display.set_caption("the-dungeon")
pygame.display.set_icon(pygame.image.load("icon.png"))

def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

def distance(pos1 : pygame.Vector2,pos2 : pygame.Vector2) -> float:
    return math.sqrt((pos2.x - pos1.x) ** 2 + (pos2.y - pos1.y) ** 2)


playerrect = pygame.FRect(window.get_width() / 2 - 12,window.get_height() / 2 - 12,24,24)
playervelocity = pygame.Vector2()
playeroffset = pygame.Vector2()
playerknockback = pygame.Vector2()
playerhealth = 100
playermaxhealth = 100
playerimmunity = 0

gunsprites = []

gunsprite1 = pygame.Surface((256,256))
gunsprite1.fill((1,1,1)); gunsprite1.set_colorkey((1,1,1))
pygame.draw.rect(gunsprite1,(0,0,40),(128-8,128-6,26,8))
pygame.draw.rect(gunsprite1,(0,0,40),(128-8,128-2,32,4))

stock = pygame.Surface((24,24)); stock.fill((1,1,1)); stock.set_colorkey((1,1,1)); stock.fill((0,0,0),(6,12-4,12,8))
stocka = rot_center(stock,75,128-6,128+2)
gunsprite1.blit(stocka[0],stocka[1])

stock = pygame.Surface((24,24)); stock.fill((1,1,1)); stock.set_colorkey((1,1,1)); stock.fill((0,0,0),(12-6,12-3,12,6))
stocka = rot_center(stock,-75,128+6,128+2)
gunsprite1.blit(stocka[0],stocka[1])

gunsprite = pygame.Surface((256,256))
gunsprite.fill((1,1,1)); gunsprite.set_colorkey((1,1,1))

pygame.draw.lines(gunsprite,(255,255,255),False,pygame.mask.from_surface(gunsprite1).outline(),5)
gunsprite.blit(gunsprite1,(0,0))

gunsprites.append(gunsprite)

gunsprite1 = pygame.Surface((256,256))
gunsprite1.fill((1,1,1)); gunsprite1.set_colorkey((1,1,1))
pygame.draw.rect(gunsprite1,(0,0,40),(128-8,128-6,26,8))
# pygame.draw.rect(gunsprite1,(0,0,40),(128-8,128-2,32,4))

stock = pygame.Surface((24,24)); stock.fill((1,1,1)); stock.set_colorkey((1,1,1)); stock.fill((0,0,0),(6,12-4,12,8))
stocka = rot_center(stock,50,119,130)
gunsprite1.blit(stocka[0],stocka[1])

pygame.draw.rect(gunsprite1,(0,230,230),(128+2,128,12,4))

# stock.fill((1,1,1)); stock.fill((0,0,0),(12-6,12-3,12,6))
# stocka = rot_center(stock,-75,128+6,128+2)
# gunsprite1.blit(stocka[0],stocka[1])

gunsprite = pygame.Surface((256,256))
gunsprite.fill((1,1,1)); gunsprite.set_colorkey((1,1,1))

pygame.draw.lines(gunsprite,(255,255,255),False,pygame.mask.from_surface(gunsprite1).outline(),5)
gunsprite.blit(gunsprite1,(0,0))
gunsprites.append(gunsprite)

### pistol

gunsprite1 = pygame.Surface((256,256))
gunsprite1.fill((1,1,1)); gunsprite1.set_colorkey((1,1,1))
pygame.draw.rect(gunsprite1,(0,0,40),(128-12,128-6,24,8))
# pygame.draw.rect(gunsprite1,(0,0,40),(128-8,128-2,32,4))

stock = pygame.Surface((24,24)); stock.fill((1,1,1)); stock.set_colorkey((1,1,1)); stock.fill((0,0,0),(12 - 8,12-4,16,8))
stocka = rot_center(stock,80,119,128)
gunsprite1.blit(stocka[0],stocka[1])

# stock.fill((1,1,1)); stock.fill((0,0,0),(12-6,12-3,12,6))
# stocka = rot_center(stock,-75,128+6,128+2)
# gunsprite1.blit(stocka[0],stocka[1])

gunsprite = pygame.Surface((256,256))
gunsprite.fill((1,1,1)); gunsprite.set_colorkey((1,1,1))

pygame.draw.lines(gunsprite,(255,255,255),False,pygame.mask.from_surface(gunsprite1).outline(),5)
gunsprite.blit(gunsprite1,(0,0))
gunsprites.append(gunsprite)

worldoffset = pygame.Vector2()

gundelay = 0
recoil = 0
blackholedelay = 0.5
blholeadditive = False

def getroom(index) -> list:
    # print(index)
    if index == 0:
        return [
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        ]
    if index == 1:
        return [
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,1,1],
            [3,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,3],
            [3,2,0,1,0,0,0,0,4,0,0,0,0,0,4,0,0,0,0,1,0,2,3],
            [3,2,0,1,0,0,0,0,4,0,0,8,0,0,4,0,0,0,0,1,0,2,3],
            [3,2,0,1,0,0,0,0,4,0,0,0,0,0,4,0,0,0,0,1,0,2,3],
            [3,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,3],
            [1,1,0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        ]
    if index == 2:
        return [
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [3,2,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,8,1,1,1,1,1,1,1,1,0,2,3],
            [3,2,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,2,3],
            [3,2,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,2,3],
            [1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        ]
    if index == 3:
        return [
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [3,2,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,1,0,8,0,1,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,2,3],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        ]

    if index == 4:
        return [
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1],
            [1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1],
            [3,2,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,2,3],
            [3,2,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,3],
            [3,2,0,0,0,1,0,0,0,0,0,8,0,0,0,0,0,1,0,0,0,2,3],
            [3,2,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,3],
            [3,2,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,2,3],
            [1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1],
            [1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        ]
    if index == 5:
        return [
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,4,4,4,0,1,1],
            [1,1,0,4,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,4,0,1,1],
            [1,1,0,4,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,4,0,1,1],
            [3,2,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,2,3],
            [1,1,0,4,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,4,0,1,1],
            [1,1,0,4,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,4,0,1,1],
            [1,1,0,4,4,4,0,0,0,0,0,0,0,0,0,0,0,4,4,4,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        ]

    if index == 6:
        return [
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        ]
    if index == 7:
        return [
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,1,1],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        ]
    if index == 8:
        return [
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,3],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        ]
    return [
        [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [3,2,0,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,0,0,0,2,3],
        [3,2,0,0,0,0,0,0,0,1,1,0,1,0,1,0,1,0,0,0,0,2,3],
        [3,2,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,2,3],
        [3,2,0,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,2,3],
        [3,2,0,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,0,0,0,2,3],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,1,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,3,3,3,3,3,1,1,1,1,1,1,1,1,1],
    ]


rooms = [
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1]
]
roomsbeat = [
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1]
]
roomcord = random.choice([pygame.Vector2(2,0),pygame.Vector2(2,4),pygame.Vector2(0,2),pygame.Vector2(4,2)])

                
generations = random.randint(4,6)
curgenpos = roomcord.copy()
oldgenpos = roomcord.copy()
rooms[int(curgenpos.y)][int(curgenpos.x)] = 8
roombeat = [[0 for _ in range(len(rooms))] for _ in range(len(rooms[0]))]

roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
roomenemies = [[[[pygame.Rect(random.randint(100,600),random.randint(100,400),24,24),pygame.Vector2(2,2),0,100,12,pygame.Vector2(0,0),100] for i in range(random.randint(3,10)) if not rooms[y][x] in [0,7,8]] for x in range(5)] for y in range(5)]
endx, endy = -1, -1

if endx == -1:
    rooms[int(roomcord.y)][int(roomcord.x)] = 0

for i in range(generations):
    if i == 0:
        if curgenpos == pygame.Vector2(2,4):
            curgenpos = pygame.Vector2(curgenpos.x,curgenpos.y - 1)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
        elif curgenpos == pygame.Vector2(2,0):
            curgenpos = pygame.Vector2(curgenpos.x,curgenpos.y + 1)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
        elif curgenpos == pygame.Vector2(4,2):
            curgenpos = pygame.Vector2(curgenpos.x - 1,curgenpos.y)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
        elif curgenpos == pygame.Vector2(0,2):
            curgenpos = pygame.Vector2(curgenpos.x + 1,curgenpos.y)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
    elif i < generations - 1:
        choices = []
        try: 
            if rooms[int(curgenpos.y - 1)][int(curgenpos.x)] == -1 and curgenpos.y - 1 > 0: choices.append(pygame.Vector2(curgenpos.x,curgenpos.y - 1))
        except: pass
        try: 
            if rooms[int(curgenpos.y + 1)][int(curgenpos.x)] == -1 and curgenpos.y + 1 < len(rooms): choices.append(pygame.Vector2(curgenpos.x,curgenpos.y + 1))
        except: pass
        try: 
            if rooms[int(curgenpos.y)][int(curgenpos.x - 1)] == -1 and curgenpos.x - 1 > 0: choices.append(pygame.Vector2(curgenpos.x - 1,curgenpos.y))
        except: pass
        try: 
            if rooms[int(curgenpos.y)][int(curgenpos.x + 1)] == -1 and curgenpos.x + 1 < len(rooms[0]): choices.append(pygame.Vector2(curgenpos.x + 1,curgenpos.y))
        except: pass
        try: 
            curgenpos = random.choice(choices)
            # print(curgenpos)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
        except Exception as e: pass# print(e)
    else:
    
        try: 
            curgenpos = random.choice(choices)
            # curgenpos = choices
            # print(curgenpos,"a")
            rooms[int(curgenpos.y)][int(curgenpos.x)] = 7
            roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
            # roomenemies[int(curgenpos.y)][int(curgenpos.x)] = []
        except Exception as e: 
            try: 
                if rooms[int(oldgenpos.y - 1)][int(oldgenpos.x)] == -1: rooms[int(oldgenpos.y - 1)][int(oldgenpos.x)] = 7
                break
            except: pass
            try: 
                if rooms[int(oldgenpos.y + 1)][int(oldgenpos.x)] == -1: rooms[int(oldgenpos.y + 1)][int(oldgenpos.x)] = 7
                break
            except: pass
            try: 
                if rooms[int(oldgenpos.y)][int(oldgenpos.x - 1)] == -1: rooms[int(oldgenpos.y)][int(oldgenpos.x - 1)] = 7
                break
            except: pass
            try: 
                if rooms[int(oldgenpos.y)][int(oldgenpos.x + 1)] == -1: rooms[int(oldgenpos.y)][int(oldgenpos.x + 1)] = 7
                break
            except: pass
            try: roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
            except: pass
            # try: roomenemies[int(curgenpos.y)][int(curgenpos.x)] = []
            # except: pass
            




font = pygame.font.SysFont("Source Code Pro",24,True)
fontsmall = pygame.font.SysFont("Source Code Pro",12)
fontmedium = pygame.font.SysFont("Source Code Pro",16)

# [position, room, type, speed, size, velocity]
enemies = [[pygame.Rect(random.randint(100,200),random.randint(100,200),24,24),pygame.Vector2(2,2),0,150,12,pygame.Vector2(0,0)]]
# [position, room, side, type, speed, size, angle, vel]
bullets = []
# [position, velocity, size, shape, lifespan(s)]
particles = []

rooms[2][2] = 1

minimap = pygame.Surface((150,150)); minimap.fill((255,255,255)); minimap.set_alpha(70)

sounds = [
    pygame.mixer.Sound("hurt.wav"),
    pygame.mixer.Sound("explosion.wav"),
    pygame.mixer.Sound("laserShoot.wav"),#pygame.mixer.Sound("Pew.mp3"),pygame.mixer.Sound("laserShoot.wav"),
    pygame.mixer.Sound("enterroom.wav"),
    pygame.mixer.Sound("powerUp.wav")
]

for i in sounds:
    i.set_volume(1)

# 608 416

tutorialkeyoffset = 0
tutorialinventoryoffset = 0

names = {
    "rifle": "Assault Rifle",
    "shotgun": "Shotgun",
    "pistol": "Pistol"
}
types = {
    1: "rifle",
    2: "shotgun",
    3: "pistol"
}

guncolors = {
    " common ": (255,255,255),
    " [blue]rare[/blue] ": (0,0,220),
    " [purple]epic[/purple] ": (220,0,220),
    "[orange_red1]legendary[/orange_red1]": (220,190,0),
    " [bright_yellow]mythical[/bright_yellow] ": (255,255,0),
    " [red]unreal[/red] ": (255,0,0),
    " [bright_cyan]godly[/bright_cyan] ": (0,255,255)
}

inventory = [
    [0,weapons.Weapon(pygame.Surface((255,255)),"empty").getrarity()], 
    [0,weapons.Weapon(pygame.Surface((255,255)),"empty").getrarity()]
]
curinvindex = 0
# [position, roomcord, itemid, itemdata]
items = []

finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

inpopup = False
popup = pygame.Surface((256,256))

rooms[int(roomcord.y)][int(roomcord.x)] = 0
for y, row in enumerate(rooms):
    for x, tile in enumerate(row):
        if tile == 7:
            endx, endy = x, y
            roomenemies[y][x] = []

reloadtimer = [0 for i in range(len(inventory))]
curbullets = [inventory[i][1]["magsize"] for i in range(len(inventory))]

while True:
    dt = clock.tick(60) / 1000
    mousepos = pygame.Vector2(pygame.mouse.get_pos())
    # # print(roomcord)
    numenemies = 0
    for y, row in enumerate(roomenemies):
        for x, tile in enumerate(row):
            if rooms[y][x] != -1:
                numenemies += len(tile)

    if gundelay > 0: gundelay -= dt
    elif gundelay < 0: gundelay = 0

    if reloadtimer[curinvindex] > 0: 
        reloadtimer[curinvindex] -= dt
        if recoil <= 3: recoil = 360
    elif reloadtimer[curinvindex] < 0:
        curbullets[curinvindex] = inventory[curinvindex][1]["magsize"]
        reloadtimer[curinvindex] = 0
    

    if recoil > 0: recoil += ((0 - recoil) / 0.2) * dt

    if blholeadditive: blackholedelay += dt
    else: blackholedelay -= dt

    if blackholedelay < 0: blholeadditive = True
    elif blackholedelay > 0.5: blholeadditive = False

    keys = pygame.key.get_pressed()

    if playerknockback.x != 0: playerknockback.x += ((0 - playerknockback.x) / 0.08) * dt
    if playerknockback.y != 0: playerknockback.y += ((0 - playerknockback.y) / 0.08) * dt

    if 2 > playerknockback.x > -2: playerknockback.x = 0
    if 2 > playerknockback.y > -2: playerknockback.y = 0

    if playerimmunity > 0: playerimmunity -= dt
    elif playerimmunity < 0: playerimmunity = 0
    
    # print(playerknockback)

    # curroom = defrooms[0].copy()

    curroom = getroom(rooms[int(roomcord.y)][int(roomcord.x)])
    
    # # print(curroom)

    if roombeat[int(roomcord.y)][int(roomcord.x)] != 0:

        if (0 < roomcord.x and rooms[int(roomcord.y)][int(roomcord.x - 1)] == -1) or roomcord.x == 0: 
            for i in range(6,11):    
                curroom[i][0] = 1
                curroom[i][1] = 1


        if (roomcord.x < len(rooms[0]) - 1 and rooms[int(roomcord.y)][int(roomcord.x + 1)] == -1) or roomcord.x == len(rooms[0]) - 1: 
            for i in range(6,11):    
                curroom[i][22] = 1
                curroom[i][21] = 1

        if (0 < roomcord.y and rooms[int(roomcord.y - 1)][int(roomcord.x)] == -1) or roomcord.y == 0: 
            for i in range(9,14):    
                curroom[0][i] = 1
                curroom[1][i] = 1


        if (roomcord.y < len(rooms) - 1 and rooms[int(roomcord.y + 1)][int(roomcord.x)] == -1) or roomcord.y == len(rooms) - 1: 
            for i in range(9,14):    
                curroom[16][i] = 1
                curroom[15][i] = 1
    else:  
        if (0 < roomcord.x and rooms[int(roomcord.y)][int(roomcord.x - 1)] == -1) or roomcord.x == 0: 
            for i in range(6,11):    
                curroom[i][0] = 3
                curroom[i][1] = 1
        else:
            for i in range(6,11):    
                curroom[i][0] = 3
                curroom[i][1] = 4


        if (roomcord.x < len(rooms[0]) - 1 and rooms[int(roomcord.y)][int(roomcord.x + 1)] == -1) or roomcord.x == len(rooms[0]) - 1: 
            for i in range(6,11):    
                curroom[i][22] = 3
                curroom[i][21] = 1
        else:
            for i in range(6,11):    
                curroom[i][22] = 3
                curroom[i][21] = 4

        if (0 < roomcord.y and rooms[int(roomcord.y - 1)][int(roomcord.x)] == -1) or roomcord.y == 0: 
            for i in range(9,14):    
                curroom[0][i] = 3
                curroom[1][i] = 1
        else:
            for i in range(9,14):    
                curroom[0][i] = 3
                curroom[1][i] = 4


        if (roomcord.y < len(rooms) - 1 and rooms[int(roomcord.y + 1)][int(roomcord.x)] == -1) or roomcord.y == len(rooms) - 1: 
            for i in range(9,14):    
                curroom[16][i] = 1
                curroom[15][i] = 1
        else:
            for i in range(9,14):    
                curroom[16][i] = 2
                curroom[15][i] = 4

    curroominv = [[(1 if i > 0 else 0) for i in row] for row in curroom]

    grid = Grid(matrix=curroominv.copy())

    oldoffset = pygame.Vector2(worldoffset.x,worldoffset.y)
    # worldoffset.x += playervelocity.x * dt
    playerrect.x -= playervelocity.x * dt

    
    playerrect.x += playerknockback.x * dt

    for y, row in enumerate(curroom):
        for x, tile in enumerate(row):
            if tile in [1,4] and playerrect.colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32):
                if playervelocity.x < 0 or playerknockback.x > 0: 
                    playerrect.right = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).left
                elif playervelocity.x > 0 or playerknockback.x < 0: 
                    playerrect.left = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).right
            elif tile == 3 and playerrect.colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32):
                if playerrect.x < window.get_width() / 2:
                    playerrect.x = window.get_width() - 80
                    roomcord.x -= 1
                    # print(roomcord)
                elif playerrect.x > window.get_width() / 2:
                    playerrect.x = 60
                    roomcord.x += 1
                    # print(roomcord)
                sounds[3].play()
            elif tile == 7 and playerrect.colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32) and numenemies == 0:
                items = []

                for y, row in enumerate(rooms):
                    for x, tile in enumerate(row):
                        if tile == 7:
                            endx, endy = x, y
                            roomenemies[y][x] = []

                rooms = [
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1]
                ]
                roomsbeat = [
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1]
                ]
                roomcord = random.choice([pygame.Vector2(2,0),pygame.Vector2(2,4),pygame.Vector2(0,2),pygame.Vector2(4,2)])

                                
                generations = random.randint(4,6)
                curgenpos = roomcord.copy()
                oldgenpos = roomcord.copy()
                rooms[int(curgenpos.y)][int(curgenpos.x)] = 8
                roombeat = [[0 for _ in range(len(rooms))] for _ in range(len(rooms[0]))]

                roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
                roomenemies = [[[[pygame.Rect(random.randint(100,600),random.randint(100,400),24,24),pygame.Vector2(2,2),0,100,12,pygame.Vector2(0,0),100] for i in range(random.randint(3,10)) if not rooms[y][x] in [0,7,8]] for x in range(5)] for y in range(5)]
                endx, endy = -1, -1

                if endx == -1:
                    rooms[int(roomcord.y)][int(roomcord.x)] = 0

                for i in range(generations):
                    if i == 0:
                        if curgenpos == pygame.Vector2(2,4):
                            curgenpos = pygame.Vector2(curgenpos.x,curgenpos.y - 1)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
                        elif curgenpos == pygame.Vector2(2,0):
                            curgenpos = pygame.Vector2(curgenpos.x,curgenpos.y + 1)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
                        elif curgenpos == pygame.Vector2(4,2):
                            curgenpos = pygame.Vector2(curgenpos.x - 1,curgenpos.y)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
                        elif curgenpos == pygame.Vector2(0,2):
                            curgenpos = pygame.Vector2(curgenpos.x + 1,curgenpos.y)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
                    elif i < generations - 1:
                        choices = []
                        try: 
                            if rooms[int(curgenpos.y - 1)][int(curgenpos.x)] == -1 and curgenpos.y - 1 > 0: choices.append(pygame.Vector2(curgenpos.x,curgenpos.y - 1))
                        except: pass
                        try: 
                            if rooms[int(curgenpos.y + 1)][int(curgenpos.x)] == -1 and curgenpos.y + 1 < len(rooms): choices.append(pygame.Vector2(curgenpos.x,curgenpos.y + 1))
                        except: pass
                        try: 
                            if rooms[int(curgenpos.y)][int(curgenpos.x - 1)] == -1 and curgenpos.x - 1 > 0: choices.append(pygame.Vector2(curgenpos.x - 1,curgenpos.y))
                        except: pass
                        try: 
                            if rooms[int(curgenpos.y)][int(curgenpos.x + 1)] == -1 and curgenpos.x + 1 < len(rooms[0]): choices.append(pygame.Vector2(curgenpos.x + 1,curgenpos.y))
                        except: pass
                        try: 
                            curgenpos = random.choice(choices)
                            # print(curgenpos)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                        except Exception as e: pass# print(e)
                    else:
                    
                        try: 
                            curgenpos = random.choice(choices)
                            # curgenpos = choices
                            # print(curgenpos,"a")
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = 7
                            roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
                            # roomenemies[int(curgenpos.y)][int(curgenpos.x)] = []
                        except Exception as e: 
                            try: 
                                if rooms[int(oldgenpos.y - 1)][int(oldgenpos.x)] == -1: rooms[int(oldgenpos.y - 1)][int(oldgenpos.x)] = 7
                                break
                            except: pass
                            try: 
                                if rooms[int(oldgenpos.y + 1)][int(oldgenpos.x)] == -1: rooms[int(oldgenpos.y + 1)][int(oldgenpos.x)] = 7
                                break
                            except: pass
                            try: 
                                if rooms[int(oldgenpos.y)][int(oldgenpos.x - 1)] == -1: rooms[int(oldgenpos.y)][int(oldgenpos.x - 1)] = 7
                                break
                            except: pass
                            try: 
                                if rooms[int(oldgenpos.y)][int(oldgenpos.x + 1)] == -1: rooms[int(oldgenpos.y)][int(oldgenpos.x + 1)] = 7
                                break
                            except: pass
                            try: roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
                            except: pass
                            # try: roomenemies[int(curgenpos.y)][int(curgenpos.x)] = []
                            # except: pass
                

    # worldoffset.y += playervelocity.y * dt
    # playervelocity.y -= 10000 * dt
    playerrect.y -= playervelocity.y * dt
    playerrect.y += playerknockback.y * dt
    for y, row in enumerate(curroom):
        for x, tile in enumerate(row):
            if tile in [1,4] and playerrect.colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32):
                if playervelocity.y > 0 or playerknockback.y < 0: 
                    playerrect.top = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).bottom
                elif playervelocity.y < 0 or playerknockback.y > 0: 
                    playerrect.bottom = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).top
            elif tile == 3 and playerrect.colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32):
                if playerrect.y < window.get_height() / 2:
                    playerrect.y = window.get_height() - 60
                    roomcord.y -= 1
                    # print(roomcord)
                elif playerrect.y > window.get_height() / 2:
                    playerrect.y = 40
                    roomcord.y += 1
                    # print(roomcord)
                sounds[3].play()
            elif tile == 7 and playerrect.colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32) and numenemies == 0:
                items = []
                rooms[int(roomcord.y)][int(roomcord.x)] = 0
                for y, row in enumerate(rooms):
                    for x, tile in enumerate(row):
                        if tile == 7:
                            endx, endy = x, y
                            roomenemies[y][x] = []

                rooms = [
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1]
                ]
                roomsbeat = [
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1]
                ]
                roomcord = random.choice([pygame.Vector2(2,0),pygame.Vector2(2,4),pygame.Vector2(0,2),pygame.Vector2(4,2)])

                                
                generations = random.randint(4,6)
                curgenpos = roomcord.copy()
                oldgenpos = roomcord.copy()
                rooms[int(curgenpos.y)][int(curgenpos.x)] = 8
                roombeat = [[0 for _ in range(len(rooms))] for _ in range(len(rooms[0]))]

                roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
                roomenemies = [[[[pygame.Rect(random.randint(100,600),random.randint(100,400),24,24),pygame.Vector2(2,2),0,100,12,pygame.Vector2(0,0),100] for i in range(random.randint(3,10)) if not rooms[y][x] in [0,7,8]] for x in range(5)] for y in range(5)]
                endx, endy = -1, -1

                if endx == -1:
                    rooms[int(roomcord.y)][int(roomcord.x)] = 0

                for i in range(generations):
                    if i == 0:
                        if curgenpos == pygame.Vector2(2,4):
                            curgenpos = pygame.Vector2(curgenpos.x,curgenpos.y - 1)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
                        elif curgenpos == pygame.Vector2(2,0):
                            curgenpos = pygame.Vector2(curgenpos.x,curgenpos.y + 1)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
                        elif curgenpos == pygame.Vector2(4,2):
                            curgenpos = pygame.Vector2(curgenpos.x - 1,curgenpos.y)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
                        elif curgenpos == pygame.Vector2(0,2):
                            curgenpos = pygame.Vector2(curgenpos.x + 1,curgenpos.y)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                            # rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
                    elif i < generations - 1:
                        choices = []
                        try: 
                            if rooms[int(curgenpos.y - 1)][int(curgenpos.x)] == -1 and curgenpos.y - 1 > 0: choices.append(pygame.Vector2(curgenpos.x,curgenpos.y - 1))
                        except: pass
                        try: 
                            if rooms[int(curgenpos.y + 1)][int(curgenpos.x)] == -1 and curgenpos.y + 1 < len(rooms): choices.append(pygame.Vector2(curgenpos.x,curgenpos.y + 1))
                        except: pass
                        try: 
                            if rooms[int(curgenpos.y)][int(curgenpos.x - 1)] == -1 and curgenpos.x - 1 > 0: choices.append(pygame.Vector2(curgenpos.x - 1,curgenpos.y))
                        except: pass
                        try: 
                            if rooms[int(curgenpos.y)][int(curgenpos.x + 1)] == -1 and curgenpos.x + 1 < len(rooms[0]): choices.append(pygame.Vector2(curgenpos.x + 1,curgenpos.y))
                        except: pass
                        try: 
                            curgenpos = random.choice(choices)
                            # print(curgenpos)
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
                        except Exception as e: pass# print(e)
                    else:
                    
                        try: 
                            curgenpos = random.choice(choices)
                            # curgenpos = choices
                            # print(curgenpos,"a")
                            rooms[int(curgenpos.y)][int(curgenpos.x)] = 7
                            roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
                            # roomenemies[int(curgenpos.y)][int(curgenpos.x)] = []
                        except Exception as e: 
                            try: 
                                if rooms[int(oldgenpos.y - 1)][int(oldgenpos.x)] == -1: rooms[int(oldgenpos.y - 1)][int(oldgenpos.x)] = 7
                                break
                            except: pass
                            try: 
                                if rooms[int(oldgenpos.y + 1)][int(oldgenpos.x)] == -1: rooms[int(oldgenpos.y + 1)][int(oldgenpos.x)] = 7
                                break
                            except: pass
                            try: 
                                if rooms[int(oldgenpos.y)][int(oldgenpos.x - 1)] == -1: rooms[int(oldgenpos.y)][int(oldgenpos.x - 1)] = 7
                                break
                            except: pass
                            try: 
                                if rooms[int(oldgenpos.y)][int(oldgenpos.x + 1)] == -1: rooms[int(oldgenpos.y)][int(oldgenpos.x + 1)] = 7
                                break
                            except: pass
                            try: roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
                            except: pass
                            # try: roomenemies[int(curgenpos.y)][int(curgenpos.x)] = []
                            # except: pass



    if keys[pygame.K_w]: playervelocity.y = 200
    elif keys[pygame.K_s]: playervelocity.y = -200
    else: playervelocity.y = 0
    if keys[pygame.K_a]: playervelocity.x = 200
    elif keys[pygame.K_d]: playervelocity.x = -200
    else: playervelocity.x = 0

    if pygame.mouse.get_pressed()[0] and gundelay == 0:
        curbullets[curinvindex] -= 1
        if curbullets[curinvindex] <= -1 and reloadtimer[curinvindex] == 0:
            reloadtimer[curinvindex] = inventory[curinvindex][1]["reloadtime"] / 10
            curbullets[curinvindex] = 0
        elif curbullets[curinvindex] <= -1:
            curbullets[curinvindex] = 0
        else:
            # sounds[2].play()
            gundelay = inventory[curinvindex][1]["delay"] / 10
        
                # curbullets[curinvindex] = inventory[curinvindex][1]["magsize"]
            # playervelocity.y = -1000
            if recoil < 80: recoil += inventory[curinvindex][1]["bullets"] * 10
            # [position, room, side, type, speed, size, angle, vel, originalcolor]
            inconsistency = random.randint(1,10)
            for h in range(int(inventory[curinvindex][1]["bullets"])): 
                tmp = math.degrees(math.atan2(mousepos.x - playerrect.centerx,mousepos.y - playerrect.centery)) - 90 + (-recoil if math.degrees(math.atan2(mousepos.x - playerrect.centerx,mousepos.y - playerrect.centery)) < -90 else recoil)

                bullets.append([
                    pygame.Vector2(playerrect.center),
                    roomcord.copy(),'player',
                    0,300,4,
                    angle+90,
                    pygame.Vector2(math.sin(math.radians(angle + 90 + h * 5 + inconsistency)) * 300,
                                math.cos(math.radians(angle + 90 + h * 5 + inconsistency)) * 300),
                    (230,220,0),
                    0,
                    0])
                sounds[2].play()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEWHEEL:
            curinvindex += event.y
            if curinvindex > len(inventory) - 1: curinvindex = 0
            elif curinvindex < 0: curinvindex = len(inventory) - 1
            recoil = 360
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_DOWN,pygame.K_UP,pygame.K_RIGHT,pygame.K_LEFT] :
            curinvindex += 1 if event.key in (pygame.K_UP,pygame.K_RIGHT) else -1
            if curinvindex > len(inventory) - 1: curinvindex = 0
            elif curinvindex < 0: curinvindex = len(inventory) - 1
            recoil = 360
        if event.type == pygame.KEYDOWN and event.key in [pygame.K_1,pygame.K_2] :
            curinvindex = 1 if event.key == pygame.K_1 else 0
            recoil = 360
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reloadtimer[curinvindex] = inventory[curinvindex][1]["reloadtime"] / 10
            curbullets[curinvindex] = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            popup = pygame.Surface((window.get_width() / 2,window.get_height() - 50))
            popup.fill((1,0,0)); popup.set_colorkey((1,0,0))
            pygame.draw.rect(popup,(0,0,0),(0,0,popup.get_width(),popup.get_height()),0,4)
            pygame.draw.rect(popup,(255,255,255),(0,0,popup.get_width(),popup.get_height()),4,4)

            text = fontmedium.render("weapon details",True,(255,255,255))
            popup.blit(text,(popup.get_width() / 2 - text.get_width() / 2,20))

            try:
                for ind,i in enumerate(inventory[curinvindex][1].keys()):
                    if i == "rarity":
                        rarity = inventory[curinvindex][1][i]
                        color = (255,255,255)
                        if rarity == " common ": 
                            rarity = "common"
                        elif rarity == " [blue]rare[/blue] ": 
                            rarity = "rare"
                            color = (0,0,220)
                        elif rarity == " [purple]epic[/purple] ":
                            rarity = "epic"
                            color = (220,0,220)
                        elif rarity == "[orange_red1]legendary[/orange_red1]":
                            rarity = "legendary"
                            color = (220,190,0)
                        elif rarity == " [bright_yellow]mythical[/bright_yellow] ":
                            rarity = "mythical"
                            color = (255,255,0)
                        elif rarity ==  " [red]unreal[/red] ":
                            rarity = "unreal"
                            color = (255,0,0)
                        elif rarity == " [bright_cyan]godly[/bright_cyan] ":
                            rarity = "godly"
                            color = (0,255,255)
                        text = fontmedium.render(str(i)+": "+str(rarity),True,color)
                        popup.blit(text,(20,60+ind * 20))
                    else:
                        text = fontmedium.render(str(i)+": "+str(inventory[curinvindex][1][i]),True,(255,255,255))
                        popup.blit(text,(20,60+ind * 20))
            except:
                text = fontmedium.render("could not fetch details",True,(255,255,255))
                popup.blit(text,(popup.get_width() / 2 - text.get_width() / 2,popup.get_height() / 2 - text.get_height() / 2))

            # popup.fill((0,0,0))
            inpopup = not inpopup
            # print(inventory[curinvindex][1])
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            for i in items:
                if pygame.Rect(i[0].x - 5,i[0].y - 5,42,42).collidepoint(pygame.mouse.get_pos()) and i[1] == roomcord:
                    if inventory[curinvindex][0] > 0: 
                        items.append([pygame.Vector2(playerrect.topleft),i[1],inventory[curinvindex][0] - 1,inventory[curinvindex][1].copy(),i[4],i[5],curbullets[curinvindex]])
                        
                    inventory[curinvindex][0] = i[2] + 1
                    # print(i[2])
                    inventory[curinvindex][1] = i[3]
                    curbullets[curinvindex] = i[6]
                    items.remove(i)
                



    window.fill((0,0,0))

    # pygame.draw.rect(window,(0,0,0),(-280-128+worldoffset.x,-256+worldoffset.y,2000,256+8))
    # pygame.draw.rect(window,(0,0,0),(-280-128+worldoffset.x,480-8+worldoffset.y,2000,256+8))
    # pygame.draw.rect(window,(0,0,0),(-280-128+worldoffset.x,worldoffset.y,280+16+128,480))
    # pygame.draw.rect(window,(0,0,0),(720-16+worldoffset.x,worldoffset.y,280+16+1000,480))
    pygame.draw.rect(window,(30,30,30),(60,32,608,416))
    # window.blit(font.render(f"{int(roomcord.x)},{int(roomcord.y)}",True,(45,45,45)),(window.get_width() / 2 - font.render(f"{int(roomcord.x)},{int(roomcord.y)}",True,(45,45,45)).get_width() / 2,window.get_height() / 2 - font.get_height() / 2))
    

    for y, row in enumerate(curroom):
        for x, tile in enumerate(row):
            if tile == 1: 
                pygame.draw.rect(window,(0,0,0),(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32))
            if tile == 2: pygame.draw.rect(window,(30,30,30),(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32))
            if tile == 4: pygame.draw.rect(window,(20,20,20),(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32))
            if tile == 5: pass
            if tile == 6:                 
                pygame.draw.rect(window,(230,0,190),(x * 32 + 60 - 64 - 24 - blackholedelay * 10 - 4,y * 32 + 32 - 64 - 24 - blackholedelay * 10 - 4,48 + blackholedelay * 20 + 8,48 + blackholedelay * 20 + 8))
                pygame.draw.rect(window,(0,0,0),(x * 32 + 60 - 64 - 24,y * 32 + 32 - 64 - 24,48,48))
                

                if numenemies > 0:
                    warning = fontmedium.render("you didnt kill all enemies. remaining: "+str(numenemies),True,(255,0,0))
                    window.blit(warning,(x * 32 + 60 - 64 - warning.get_width() / 2,y * 32 + 32 - 64 - 64,48,48))

            # if tile == 8 and len(roomenemies[int(roomcord.y)][int(roomcord.x)]) > 0:
                # pygame.draw.rect(window,(220,20,20),(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32))
            elif tile == 8 and len(roomenemies[int(roomcord.y)][int(roomcord.x)]) == 0:
                if pygame.Rect(x * 32 + 60 - 64 + 1,y * 32 + 32 - 64 + 1,30,30).collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(window,(255,255,255) if distance(pygame.Vector2(x * 32 + 60 - 65 + 17,y * 32 + 32 - 65 + 17),pygame.Vector2(playerrect.centerx,playerrect.centery)) < 150 else (255,0,0),(x * 32 + 60 - 64 - 1,y * 32 + 32 - 64 - 1,34,34))
                    pygame.draw.rect(window,(0,0,0),(x * 32 - 4 + 8,y * 32 - 64,16,16),0,2)
                    pygame.draw.rect(window,(70,70,70),(x * 32 - 4 + 8,y * 32 - 68 + tutorialkeyoffset,16,16),0,2)
                    rendered = fontsmall.render("e",True,(255,255,255))
                    window.blit(rendered,(x * 32 - 4 + 16 - rendered.get_width() / 2,y * 32 - 68 + tutorialkeyoffset))
                    if tutorialkeyoffset > 2.92: tutorialkeyoffset = 0
                    tutorialkeyoffset += ((3 - tutorialkeyoffset) / 0.4) * dt
                    if keys[pygame.K_e]:
                        rooms[int(roomcord.y)][int(roomcord.x)] = 8
                        # [pos, roomcord, itemid, itemdata, velocity, poscopy]
                        for i in range(2): 
                            random.seed(hash(time.time() + i * 10))
                            idg = random.randint(0,2)
                            items.append([pygame.Vector2(x * 32 + 60 - 64 + 1,y * 32 + 32 - 64 + 1),roomcord.copy(),idg,weapons.Weapon(pygame.Surface((255,255)),types[idg + 1]).getrarity(),pygame.Vector2(random.randint(200,300) * (1 if i % 2 == 0 else -1),random.randint(100,200) * -1),pygame.Vector2(x * 32 + 60 - 64 + 1,y * 32 + 32 - 64 + 1),0])
                            
                else:
                    tutorialkeyoffset = 0
                    # print(tutorialkeyoffset)
                pygame.draw.rect(window,(220,150,0),(x * 32 + 60 - 64 + 1,y * 32 + 32 - 64 + 1,30,30))
                pygame.draw.rect(window,(220,190,0),(x * 32 + 60 - 64 + 1,y * 32 + 32 - 64 + 1,30,14))
                pygame.draw.rect(window,(220,190,0),(x * 32 + 60 - 64 + 1,y * 32 + 32 - 64 + 1 + 10,30,12))
                pygame.draw.rect(window,(0,0,0),(x * 32 + 60 - 64 + 1 + 13,y * 32 + 32 - 64 + 17,6,8))
                pygame.draw.rect(window,(0,0,0),(x * 32 + 60 - 64 + 1,y * 32 + 32 - 64 + 1,30,30),4)
                # pygame.draw.rect(window,(0,0,0),(x * 32 + 60 - 64 + 1,y * 32 + 32 - 64 + 1,30,14),4)
                pygame.draw.rect(window,(0,0,0),(x * 32 + 60 - 64 + 1,y * 32 + 32 - 64 + 1,30,22),4)
                

                # pygame.draw.rect(window,(255,255,0),(x * 32 + worldoffset.x + 60 - 32 - 2,y * 32 + worldoffset.y + 41 - 32,32,32))

    # if roomcord == pygame.Vector2(2,1):
        # pygame.draw.circle(window,(120,0,140),(340,340),18+blackholedelay * 5)
        # pygame.draw.circle(window,(0,0,0),(340,340),16)

    for ry, row in enumerate(roomenemies):
        for rx, tile in enumerate(row):
            if roomenemies[ry][rx] == [-1] and not rooms[ry][rx] in [0,7,8]:
                rooms[ry][rx] = 0
                roombeat[ry][rx] = 1 
                roomenemies[ry][rx] = []
            else:
                for i in tile:
                    # [position, room, type, speed, size]100
                    if pygame.Vector2(rx,ry) == roomcord:
                        
                        # rect = i[0]

                        # i[5] = pygame.Vector2(0,0)
                        # i[5] = pygame.Vector2(random.randint(30,70),random.randint(30,70))
                        
                        if i[5].x < 0: i[0].left += i[5].x * dt 
                        else: i[0].right += i[5].x * dt 

                        for ry1, row in enumerate(roomenemies):
                            for rx1, tile in enumerate(row):
                                for a in tile:
                                    if pygame.Vector2(rx1,ry1) == roomcord and a != i and a[0].colliderect(i[0]):
                                        if i[5].x > 0: 
                                            i[0].right = a[0].left
                                        elif i[5].x < 0: 
                                            i[0].left = a[0].right



                        for y, row in enumerate(curroom):
                            for x, tile in enumerate(row):
                                if tile in [1,4,3] and i[0].colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32):
                                    if i[5].x > 0: 
                                        i[0].right = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).left
                                        # print(i[0].right,"x")
                                    elif i[5].x < 0: 
                                        i[0].left = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).right
                                        # print(i[0].left,"x+")

                        if i[5].y > 0: i[0].bottom += i[5].y * dt 
                        else: i[0].top += i[5].y * dt 

                        for ry1, row in enumerate(roomenemies):
                            for rx1, tile in enumerate(row):
                                for a in tile:
                                    if pygame.Vector2(rx1,ry1) == roomcord and a != i and a[0].colliderect(i[0]):
                                        if i[5].y < 0: 
                                            i[0].top = a[0].bottom
                                        elif i[5].y > 0: 
                                            i[0].bottom = a[0].top

                        for y, row in enumerate(curroom):
                            for x, tile in enumerate(row):
                                if tile in [1,4,3] and i[0].colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32):
                                    if i[5].y < 0: 
                                        i[0].top = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).bottom
                                        # print(i[0].top,"y")
                                    elif i[5].y > 0: 
                                        i[0].bottom = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).top
                                        # print(i[0].bottom,"y+")

                        # i[0] = pygame.Vector2(rect.left,rect.top)

                        if abs(distance(pygame.Vector2(playerrect.x,playerrect.y),pygame.Vector2(i[0].x,i[0].y))) > 3:
                            angle = math.atan2(playerrect.x - i[0].x,playerrect.y - i[0].y)
                            i[5].x, i[5].y = math.sin(angle) * i[3], math.cos(angle) * i[3]
                        else:
                            i[5] = pygame.Vector2(0,0)

                        if i[0].colliderect(playerrect) and playerimmunity <= 0:
                            angle = math.atan2(playerrect.x - i[0].x,playerrect.y - i[0].y)
                            playerknockback.x = math.sin(angle) * i[3] * 3
                            playerknockback.y = math.cos(angle) * i[3] * 3
                            playerhealth -= 10
                            playerimmunity = 1
                            sounds[0].play()
                        
                        for a in bullets:
                            if i[0].collidepoint(a[0]):
                                # print(ry)
                                i[6] -= inventory[curinvindex][1]["damage"]

                                for b in range(10):
                                    speed = 1
                                    random.seed(hash(time.time()))
                                    particles.append([a[0].copy(),
                                                pygame.Vector2(random.randint(4,8) * random.choice([1,-1]) + b,
                                                                random.randint(4,10) * random.choice([1,-1]) + b),
                                                4,
                                                'rect',
                                                1,
                                                a[8],
                                                pygame.Vector2(),
                                                roomcord.copy()])
                                sounds[0].play()
                                bullets.remove(a)

                        if i[2] == 0: 
                            pygame.draw.rect(window,(255,0,0),i[0],i[4])
                            # pygame.draw.rect(window,(128,0,0),(i[0].x,i[0].y,(i[0].width / 100) * i[6],i[0].height),i[4])
                            if i[6] < 100: pygame.draw.rect(window,(128,0,0),(i[0].x,i[0].y,(i[0].width / 100) * i[6],i[0].height),i[4])
                            if i[6] <= 0:
                                for b in range(10):
                                    particles.append([pygame.Vector2(i[0].center),
                                                    pygame.Vector2(random.randint(4,8) * random.choice([1,-1]) + b,
                                                                    random.randint(4,10) * random.choice([1,-1]) + b),
                                                    5,
                                                    'rect',
                                                    5,
                                                    (255,0,0),
                                                    pygame.Vector2(),
                                                    roomcord.copy()])
                                sounds[1].play()
                                roomenemies[ry][rx].remove(i)
                                if roomenemies[ry][rx] == []:
                                    # sounds[4].play()
                                    roomenemies[ry][rx].append(-1)
                                    break
                                print(roomenemies[ry][rx])

                            angle = math.atan2(playerrect.x - i[0].x,playerrect.y - i[0].y)
                            pygame.draw.line(window,(0,255,0),i[0].center,(i[0].centerx + math.sin(angle) * 20,i[0].centery + math.cos(angle) * 20))
                        pygame.draw.circle(window,(0,255,0),i[0].center,3)

    for i in bullets:
        # [position, room, side, type, speed, size, angle, vel]
        if i[1] == roomcord:
            pygame.draw.circle(window,i[8],i[0],i[5])
            # vel = pygame.Vector2(math.sin(math.radians(i[6])) * i[4],math.cos(math.radians(i[6])) * i[4])
            # i[7] = pygame.Vector2(math.sin(math.radians(i[6])) * i[4],math.cos(math.radians(i[6])) * i[4])
            i[0].x += i[7].x * dt
            col = False
            for y, row in enumerate(curroom):
                for x, tile in enumerate(row):
                    if tile in [1, 4] and pygame.FRect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).collidepoint(i[0]): 
                        # [position, velocity, size, shape, lifespan(s), color]

                        for a in range(10):
                            curangle = random.randint(0,180)
                            speed = random.randint(0,3)
                            # print(curangle)
                            random.seed(hash(time.time()))
                            particles.append([i[0].copy(),pygame.Vector2(random.randint(4,8) * random.choice([1,-1]) + a,random.randint(4,10) * random.choice([1,-1]) + a),2,'rect',1,i[8],pygame.Vector2(math.sin(math.radians(curangle)) * speed,math.cos(math.radians(curangle)) * speed),roomcord.copy()])
                            curangle = 0
                        
                        sounds[0].play()

                        bullets.remove(i)
                        col = True
                    elif tile == 4 and pygame.FRect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).collidepoint(i[0]):
                        bullets.remove(i)
                        col = True

            if col: continue

                        # i[7].x *= -1
                        # i[0].x += i[7].x * dt
                        # col = True
            # for a in bullets:
                # if a != i and distance(i[0],a[0]) <= a[5]:
                    # a[7].x *= -1
                    # i[7].x *= -1
                    # print("a")
                # pass

                        
            i[0].y += i[7].y * dt
            for y, row in enumerate(curroom):
                for x, tile in enumerate(row):
                    if tile in [1, 4] and pygame.FRect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).collidepoint(i[0]): 
                        # i[7].y *= -1
                        # i[0].y += i[7].y * dt
                        for a in range(10):
                            curangle = random.randint(0,180)
                            speed = random.randint(0,3)
                            # print(curangle)
                            random.seed(hash(time.time()))
                            particles.append([i[0].copy(),
                                              pygame.Vector2(random.randint(4,8) * random.choice([1,-1]) + a,
                                                             random.randint(4,10) * random.choice([1,-1]) + a),
                                              2,
                                              'rect',
                                              1,
                                              i[8],
                                              pygame.Vector2(),
                                              roomcord.copy()])
                            curangle = 0
                        sounds[0].play()


                        try: bullets.remove(i)
                        except: pass
                    elif tile == 3 and pygame.FRect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).collidepoint(i[0]):
                        try: bullets.remove(i)
                        except: pass

            # for a in bullets:
                # if a != i and distance(i[0],a[0]) < a[5]:
                    # a[7].y *= -1
                    # a[7].y *= -1
                    # print("b")
                # pass
                

            # if i[7].x > 0: i[7].x -= 80 * dt
            # elif i[7].x < 0: i[7].x += 80 * dt
            # if i[7].y > 0: i[7].y -= 80 * dt
            # elif i[7].y < 0: i[7].y += 80 * dt

            # if -0.05 < i[7].x * dt < 0.05 and -0.05 < i[7].y * dt < 0.05: bullets.remove(i)

    # print(len(particles))

    for i in items:
        if i[1] == roomcord:
        # [position, roomcord, itemid, itemdata, velocity]
            #     if inventory[curinvindex][0] != 0: items.append([i[0],i[1],inventory[curinvindex][0],inventory[curinvindex][1],i[4],i[5]])
            #     inventory[curinvindex][0] = i[2]
            #     print(i[2])
            #     inventory[curinvindex][1] = i[3]
            i[0] += i[4] * dt
            i[4].x += ((0 - i[4].x) / 0.2) * dt
            i[4].y += 1000 * dt
            if i[0].y > i[5].y: i[4].y = 0

            if pygame.Rect(i[0].x - 5,i[0].y - 5,42,42).collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(window,guncolors[i[3]["rarity"]],(i[0].x - 5,i[0].y - 5,42,42),4)

                # weaptext = fontsmall.render(names[types[i[2] + 1]],True,(255,255,255))
                window.blit(fontsmall.render(names[types[i[2] + 1]],True,guncolors[i[3]["rarity"]]),(i[0].x + 19 - fontsmall.render(names[types[i[2] + 1]],True,(255,255,255)).get_width() / 2,i[0].y - 24))

                pygame.draw.rect(window,(0,0,0),(i[0].x - 4 + 12,i[0].y - 64,16,16),0,2)
                pygame.draw.rect(window,(70,70,70),(i[0].x - 4 + 12,i[0].y - 64 - 4 + tutorialkeyoffset,16,16),0,2)
                rendered = fontsmall.render("q",True,(255,255,255))
                window.blit(rendered,(i[0].x + 12,i[0].y - 68 + tutorialkeyoffset))
                if tutorialkeyoffset > 2.92: tutorialkeyoffset = 0
                else: tutorialkeyoffset += ((3 - tutorialkeyoffset) / 0.4) * dt

                # if keys[pygame.K_t]:
                #     if inventory[curinvindex][0] != 0: items.append([i[0],i[1],inventory[curinvindex][0],inventory[curinvindex][1],i[4],i[5]])
                #     inventory[curinvindex][0] = i[2]
                #     print(i[2])
                #     inventory[curinvindex][1] = i[3]

            window.blit(gunsprites[i[2]],i[0] + pygame.Vector2(-128+16,-128+16))




    for i in particles:
        # [position, velocity, size, shape, lifespan(s), color, roompos]
        if i[7] == roomcord:
            i[0] += i[1] * dt
            
            # if (i[6].x > 0 and i[1].x < 0) or (i[6].x < 0 and i[1].x > 0): i[1].x = 0
            # if (i[6].y > 0 and i[1].y < 0) or (i[6].y < 0 and i[1].y > 0): i[1].y = 0

            # if i[6].x > 0 and i[1].x > 0: i[1].x -= 20 * dt
            # elif i[6].x < 0 and i[1].x > 0: i[1].x += 20 * dt
            # if i[6].y > 0 and i[1].y > 0: i[1].y -= 20 * dt
            # elif i[6].y < 0 and i[1].y < 0: i[1].y += 20 * dt
            
            
            
            i[4] -= dt
            if i[4] <= 0: particles.remove(i)

            if i[3] == 'rect':
                pygame.draw.rect(window,i[5],(i[0].x - i[2],i[0].y - i[2],i[2] * 2,i[2] * 2))

    # pygame.draw.circle(window,(0,255,0),playerrect.center,4)

    # pygame.draw.rect(window,(255,0,0),(playerrect.x-128+12,playerrect.y-128+12,256,256))
    
    if int(playerimmunity * 10) % 2 == 0:
        pygame.draw.rect(window,(0,0,255),playerrect)
    
        angle = math.degrees(math.atan2(mousepos.x - playerrect.centerx * (display.get_width() / window.get_width()),mousepos.y - playerrect.centery * (display.get_width() / window.get_width()))) - 90
        if inventory[curinvindex][0] > 0:
            rotgun = rot_center(pygame.transform.flip(gunsprites[inventory[curinvindex][0] - 1],False,True) if angle < -90 else gunsprites[inventory[curinvindex][0] - 1],angle + (-recoil if angle < -90 else recoil),playerrect.centerx,playerrect.centery)
        # print(math.degrees(math.atan2(mousepos.x-playerrect.centerx,mousepos.y-playerrect.centery)) - 90)
        # window.blit(gunsprite,playerrect.topleft - pygame.Vector2(128,128) + pygame.Vector2(12,12))
            window.blit(rotgun[0],rotgun[1])
            if reloadtimer[curinvindex] > 0:
                overlay = pygame.transform.invert(pygame.mask.from_surface(rotgun[0]).to_surface())
                overlay.set_colorkey((255,255,255)); overlay.set_alpha((255 / (inventory[curinvindex][1]["reloadtime"] / 10)) * reloadtimer[curinvindex])
                window.blit(overlay,rotgun[1])

    # debug

    window.blit(fontsmall.render(f"== DEBUG MENU ==",True,(255,255,255),(128,0,128)),(0,0))
    window.blit(fontsmall.render(f"FPS: {round(clock.get_fps(),2)}",True,(255,255,255),(0,0,128)),(0,16))
    window.blit(fontsmall.render(f"ENTITIES: {len(bullets) + len(particles) + len(roomenemies[int(roomcord.y)][int(roomcord.x)])}",True,(255,255,255),(0,128,0)),(0,32))
    window.blit(fontsmall.render(f"ROOM POS: {int(roomcord.x)} | {int(roomcord.y)}",True,(255,255,255),(0,128,128)),(0,48))



    # minimap.fill((0,0,0))
    window.blit(fontsmall.render(f"{int(roomcord.x)} {int(roomcord.y)}",True,(255,255,255)),(window.get_width()-4-16-fontsmall.render(f"{int(roomcord.x)} {int(roomcord.y)}",True,(255,255,255)).get_width(),160 - fontsmall.get_height() - 2 + 20 + 12))
    window.blit(minimap,(window.get_width()-150-16,10))

    pygame.draw.rect(window,(128,128,128),(window.get_width() - 20 - 64, 160 + 20 - fontsmall.get_height(),64,8))
    pygame.draw.rect(window,(255,0,0),(window.get_width() - 20 - 64, 160 + 20 - fontsmall.get_height(),(64 / playermaxhealth) * playerhealth,8))

    # 28
    for y in range(len(rooms)):
        for x in range(len(rooms[0])):
            if pygame.Vector2(x,y) == roomcord:pygame.draw.rect(window,(0,255,0),(x*28 + 5 + window.get_width()-20 - 150 + 8,y*28 + 19,20,20))
            elif rooms[y][x] != -1: pygame.draw.rect(window,(255,255,255),(x*28 + 5 + window.get_width()-20 - 150 + 8,y*28 + 19,20,20))
            if rooms[y][x] != -1: window.blit(fontsmall.render(str(int(rooms[y][x])),True,(255,0,0)),(x*28 + 5 + window.get_width()-20 - 150 + 8,y*28 + 19))

    for i, gun in enumerate(inventory):
        window.blit(pygame.transform.scale(minimap,(42,42)),(window.get_width() - 4 - 42 - i * 46 ,window.get_height() - 46))
        # print(gun)
        if gun[0] > 0: 
            window.blit(gunsprites[gun[0] - 1],(window.get_width() - 42 - i * 46 + (-128+16) - (4 if gun[0] == 1 else (-2 if gun[0] == 3 else 2)),window.get_height() - 42 + (-128+16)))

    pygame.draw.rect(window,(255,255,255),(window.get_width() - 46 - 2 - curinvindex * 46 ,window.get_height() - 46 - 2,46,46),4)

    pygame.draw.rect(window,(0,0,0),(window.get_width() - 46 - 2 - curinvindex * 46 ,window.get_height() - 46 - 2 + 4 - 64,46,12),0,2)
    pygame.draw.rect(window,(70,70,70),(window.get_width() - 46 - 2 - curinvindex * 46 ,window.get_height() - 46 - 2 - 64 + tutorialinventoryoffset,46,12),0,2)#(x * 32 - 4 + 8,y * 32 - 68 + tutorialinventoryoffset,16,16),0,2)
    rendered = fontsmall.render("spc",True,(255,255,255))
    window.blit(rendered,(window.get_width() - 46 - 2 - curinvindex * 46 + rendered.get_width() / 2,window.get_height() - 50 - 64 + tutorialinventoryoffset,46,46))#(x * 32 - 4 + 16 - rendered.get_width() / 2,y * 32 - 68 + tutorialinventoryoffset))
    if tutorialinventoryoffset > 2.92: tutorialinventoryoffset = 0
    tutorialinventoryoffset += ((3 - tutorialinventoryoffset) / 0.4) * dt

    window.blit(fontmedium.render(str(curbullets[curinvindex]) + "/" + str(inventory[curinvindex][1]["magsize"]),True,(255,255,255)),(10,window.get_height() - 10 - fontmedium.get_height()))

    if inpopup:
            window.blit(popup,(window.get_width() / 2 - popup.get_width() / 2,window.get_height() / 2 - popup.get_height() / 2))

    # display.blit(pygame.transform.scale(pygame.transform.invert(window),(display.get_width(),display.get_height())),(0,0))
    display.blit(pygame.transform.scale(window,(display.get_width(),display.get_height())),(0,0))


    # print(display.get_width() / window.get_width())

    pygame.display.flip()