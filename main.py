import pygame, sys, math, random
import time

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
            [3,2,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,2,3],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,1,1],
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
            [1,1,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,1,1],
            [1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1],
            [3,2,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,2,3],
            [3,2,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,3],
            [3,2,0,0,0,1,0,0,0,0,0,8,0,0,0,0,0,1,0,0,0,2,3],
            [3,2,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,3],
            [3,2,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,2,3],
            [1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1],
            [1,1,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,1,0,0,1,1],
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
            [1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1],
            [1,1,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,1,1],
            [1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1],
            [3,2,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,2,3],
            [3,2,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,1,1,0,8,0,1,1,0,0,0,0,0,0,2,3],
            [3,2,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,2,3],
            [3,2,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,2,3],
            [1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1],
            [1,1,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,1,1],
            [1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1],
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
rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
roombeat = [[0 for _ in range(len(rooms))] for _ in range(len(rooms[0]))]

roombeat[int(curgenpos.y)][int(curgenpos.x)] = 1
roomenemies = [[[[pygame.Rect(random.randint(100,600),random.randint(100,400),24,24),pygame.Vector2(2,2),0,150,12,pygame.Vector2(0,0),100] for i in range(random.randint(3,10)) if not rooms[y][x] in [0,7]] for x in range(5)] for y in range(5)]

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
    pygame.mixer.Sound("laserShoot.wav"),
    pygame.mixer.Sound("powerUp.wav")
]

for i in sounds:
    i.set_volume(1)

# 608 416

while True:
    dt = clock.tick(75) / 1000
    mousepos = pygame.Vector2(pygame.mouse.get_pos())
    # # print(roomcord)

    if gundelay > 0: gundelay -= dt
    elif gundelay < 0: gundelay = 0

    if recoil > 0: recoil += ((0 - recoil) / 0.2) * dt

    if blholeadditive: blackholedelay += dt
    else: blackholedelay -= dt

    if blackholedelay < 0: blholeadditive = True
    elif blackholedelay > 0.5: blholeadditive = False

    keys = pygame.key.get_pressed()

    if playerknockback.x != 0: playerknockback.x += ((0 - playerknockback.x) / 0.08) * dt
    if playerknockback.y != 0: playerknockback.y += ((0 - playerknockback.y) / 0.08) * dt

    if 0.3 > playerknockback.x > -0.3: playerknockback.x = 0
    if 0.3 > playerknockback.y > -0.3: playerknockback.y = 0

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
        for i in range(6,11):
            curroom[i][0] = 2
            curroom[i][1] = 4


        for i in range(6,11):    
            curroom[i][22] = 2
            curroom[i][21] = 4

        for i in range(9,14):    
            curroom[0][i] = 2
            curroom[1][i] = 4


        for i in range(9,14):    
            curroom[16][i] = 2
            curroom[15][i] = 4


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



    if keys[pygame.K_w]: playervelocity.y = 200
    elif keys[pygame.K_s]: playervelocity.y = -200
    else: playervelocity.y = 0
    if keys[pygame.K_a]: playervelocity.x = 200
    elif keys[pygame.K_d]: playervelocity.x = -200
    else: playervelocity.x = 0

    if pygame.mouse.get_pressed()[0] and gundelay == 0:
        sounds[2].play()
        gundelay = 0.1
        # playervelocity.y = -1000
        if recoil < 80: recoil += 10
        # [position, room, side, type, speed, size, angle, vel, originalcolor]
        for i in range(1): 
            tmp = math.degrees(math.atan2(mousepos.x - playerrect.centerx,mousepos.y - playerrect.centery)) - 90 + (-recoil if math.degrees(math.atan2(mousepos.x - playerrect.centerx,mousepos.y - playerrect.centery)) < -90 else recoil)

            bullets.append([
                pygame.Vector2(playerrect.center),
                roomcord.copy(),'player',
                0,300,4,
                angle+90-(recoil if tmp < -90 else -recoil),
                pygame.Vector2(math.sin(math.radians(angle + 90 + (random.randint(1,10) if not angle < -90 else -random.randint(1,10)) - (-recoil if angle < -90 else recoil))) * 300,
                               math.cos(math.radians(angle + 90 + (random.randint(1,10) if not angle < -90 else -random.randint(1,10)) - (-recoil if angle < -90 else recoil))) * 300),
                (230,220,0),
                0,
                0])
            sounds[2].play()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                    


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
            if tile == 8 and roomsbeat[int(roomcord.y)][int(roomcord.x)] <= 1:
                pygame.draw.rect(window,(220,20,20),(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32))
            if tile == 8 and roomsbeat[int(roomcord.y)][int(roomcord.x)] == 0:
                pygame.draw.rect(window,(20,220,20),(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32))

                # pygame.draw.rect(window,(255,255,0),(x * 32 + worldoffset.x + 60 - 32 - 2,y * 32 + worldoffset.y + 41 - 32,32,32))

    # if roomcord == pygame.Vector2(2,1):
        # pygame.draw.circle(window,(120,0,140),(340,340),18+blackholedelay * 5)
        # pygame.draw.circle(window,(0,0,0),(340,340),16)

    for ry, row in enumerate(roomenemies):
        for rx, tile in enumerate(row):
            if roomenemies[ry][rx] == []:
                rooms[ry][rx] = 0
                roombeat[ry][rx] = 1 
            for i in tile:
                # [position, room, type, speed, size]100
                if pygame.Vector2(rx,ry) == roomcord:
                    
                    # rect = i[0]

                    # i[5] = pygame.Vector2(0,0)
                    # i[5] = pygame.Vector2(random.randint(30,70),random.randint(30,70))
                    
                    # i[0].centerx += i[5].x * dt 

                    for ry1, row in enumerate(roomenemies):
                        for rx1, tile in enumerate(row):
                            for a in tile:
                                if pygame.Vector2(rx1,ry1) == roomcord and a != i and a[0].colliderect(i[0]):
                                    if i[0].x > a[0].x: i[0].centerx -= i[5].x / 2 * dt
                                    else: i[0].centerx += i[5].x / 2 * dt



                    for y, row in enumerate(curroom):
                        for x, tile in enumerate(row):
                            if tile in [1,4,3] and i[0].colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32):
                                if i[5].x > 0: 
                                    i[0].right = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).left
                                    # print(i[0].right,"x")
                                elif i[5].x < 0: 
                                    i[0].left = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).right
                                    # print(i[0].left,"x+")

                    # i[0].centery += i[5].y * dt 

                    for ry1, row in enumerate(roomenemies):
                        for rx1, tile in enumerate(row):
                            for a in tile:
                                if pygame.Vector2(rx1,ry1) == roomcord and a != i and a[0].colliderect(i[0]):
                                    if i[0].y > a[0].y: i[0].centery -= i[5].y  / 2 * dt
                                    else: i[0].centery += i[5].y / 2 * dt

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
                        playerknockback.x = math.sin(angle) * i[3] * 10
                        playerknockback.y = math.cos(angle) * i[3] * 10
                        playerhealth -= 5
                        playerimmunity = 1
                        sounds[0].play()
                    
                    for a in bullets:
                        if i[0].collidepoint(a[0]):
                            # print(ry)
                            i[6] -= 10

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
                                                10,
                                                (255,0,0),
                                                pygame.Vector2(),
                                                roomcord.copy()])
                            sounds[1].play()
                            roomenemies[ry][rx].remove(i)

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
    
        angle = math.degrees(math.atan2(mousepos.x - playerrect.centerx * display.get_width() / window.get_width(),mousepos.y - playerrect.centery * display.get_width() / window.get_width())) - 90 + (-recoil if math.degrees(math.atan2(mousepos.x - playerrect.centerx * display.get_width() / window.get_width(),mousepos.y - playerrect.centery * display.get_width() / window.get_width())) < -90 else recoil)
        rotgun = rot_center(pygame.transform.flip(gunsprite,False,True) if angle < -90 else gunsprite,angle,playerrect.centerx,playerrect.centery)
        # print(math.degrees(math.atan2(mousepos.x-playerrect.centerx,mousepos.y-playerrect.centery)) - 90)
        # window.blit(gunsprite,playerrect.topleft - pygame.Vector2(128,128) + pygame.Vector2(12,12))
        window.blit(rotgun[0],rotgun[1])

    # debug

    window.blit(fontsmall.render(f"== DEBUG MENU ==",True,(255,255,255),(128,0,128)),(0,0))
    window.blit(fontsmall.render(f"FPS: {round(clock.get_fps(),2)}",True,(255,255,255),(0,0,128)),(0,16))
    window.blit(fontsmall.render(f"ENTITIES: {len(bullets) + len(particles)}",True,(255,255,255),(0,128,0)),(0,32))
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
            if rooms[y][x] != -1: window.blit(fontsmall.render(str(rooms[y][x]),True,(255,0,0)),(x*28 + 5 + window.get_width()-20 - 150 + 8,y*28 + 19))


    display.blit(pygame.transform.scale(window,(display.get_width(),display.get_height())),(0,0))

    # print(display.get_width() / window.get_width())

    pygame.display.flip()