import pygame, sys, math, random

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((720,480))
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
for i in range(generations):
    if i == 0:
        if curgenpos == pygame.Vector2(2,4):
            curgenpos = pygame.Vector2(curgenpos.x,curgenpos.y - 1)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
        elif curgenpos == pygame.Vector2(2,0):
            curgenpos = pygame.Vector2(curgenpos.x,curgenpos.y + 1)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
        elif curgenpos == pygame.Vector2(4,2):
            curgenpos = pygame.Vector2(curgenpos.x - 1,curgenpos.y)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
        elif curgenpos == pygame.Vector2(0,2):
            curgenpos = pygame.Vector2(curgenpos.x + 1,curgenpos.y)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = 0
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
            print(curgenpos)
            rooms[int(curgenpos.y)][int(curgenpos.x)] = random.randint(1,6)
        except Exception as e: print(e)
    else:
    
        try: 
            curgenpos = random.choice(choices)
            # curgenpos = choices
            print(curgenpos,"a")
            rooms[int(curgenpos.y)][int(curgenpos.x)] = 7
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



font = pygame.font.SysFont("Source Code Pro",24,True)
fontsmall = pygame.font.SysFont("Source Code Pro",12)


# [position, room, type, speed, size, velocity]
enemies = [[pygame.Vector2(10,10),pygame.Vector2(2,1),0,100,12,pygame.Vector2()]]
# [position, room, side, type, speed, size, angle, vel]
bullets = []
# [position, velocity, size, shape, lifespan(s)]
particles = []

minimap = pygame.Surface((150,150)); minimap.fill((255,255,255)); minimap.set_alpha(70)

# 608 416

while True:
    dt = clock.tick(75) / 1000
    mousepos = pygame.Vector2(pygame.mouse.get_pos())
    # print(roomcord)

    if gundelay > 0: gundelay -= dt
    elif gundelay < 0: gundelay = 0

    if recoil > 0: recoil += ((0 - recoil) / 0.2) * dt

    if blholeadditive: blackholedelay += dt
    else: blackholedelay -= dt

    if blackholedelay < 0: blholeadditive = True
    elif blackholedelay > 0.5: blholeadditive = False

    keys = pygame.key.get_pressed()

    # curroom = defrooms[0].copy()

    curroom = getroom(rooms[int(roomcord.y)][int(roomcord.x)])
    # print(curroom)

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
    oldoffset = pygame.Vector2(worldoffset.x,worldoffset.y)
    # worldoffset.x += playervelocity.x * dt
    playerrect.x -= playervelocity.x * dt

    


    for y, row in enumerate(curroom):
        for x, tile in enumerate(row):
            if tile in [1,4] and playerrect.colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32):
                if playervelocity.x < 0: 
                    playerrect.right = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).left
                elif playervelocity.x > 0: 
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
                

    # worldoffset.y += playervelocity.y * dt
    playerrect.y -= playervelocity.y * dt
    for y, row in enumerate(curroom):
        for x, tile in enumerate(row):
            if tile in [1,4] and playerrect.colliderect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32):
                if playervelocity.y > 0: 
                    playerrect.top = pygame.Rect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).bottom
                elif playervelocity.y < 0: 
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


    if keys[pygame.K_w]: playervelocity.y = 200
    elif keys[pygame.K_s]: playervelocity.y = -200
    else: playervelocity.y = 0
    if keys[pygame.K_a]: playervelocity.x = 200
    elif keys[pygame.K_d]: playervelocity.x = -200
    else: playervelocity.x = 0

    if pygame.mouse.get_pressed()[0] and gundelay == 0:
        gundelay = 0.1
        if recoil < 80: recoil += 10
        # [position, room, side, type, speed, size, angle, vel, originalcolor]
        for i in range(1): bullets.append([pygame.Vector2(playerrect.center),roomcord.copy(),'player',0,300,4,angle+90-recoil,pygame.Vector2(math.sin(math.radians(angle + 90+ random.randint(1,30) - recoil)) * 300,math.cos(math.radians(angle + 90 + random.randint(1,30) - recoil)) * 300),(230,220,0),0,0])


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

    for i in enemies:
        # [position, room, type, speed, size]
        if i[1] == roomcord:
            i[0] += i[5] * dt

            angle = math.atan2(playerrect.x - i[0].x - 60,playerrect.y - i[0].y - 32)
            i[5].x, i[5].y = math.sin(angle) * i[3], math.cos(angle) * i[3]

            if i[2] == 0: pygame.draw.rect(window,(255,0,0),(i[0].x+60-i[4],i[0].y+32-i[4],i[4] * 2, i[4] * 2),i[4])

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
                    if tile in [1] and pygame.FRect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).collidepoint(i[0]): 
                        # [position, velocity, size, shape, lifespan(s), color]

                        for a in range(1):
                            curangle = random.randint(0,180)
                            speed = random.randint(0,3)
                            # print(curangle)
                            particles.append([i[0],pygame.Vector2(math.sin(math.radians(curangle)) * speed,math.cos(math.radians(curangle)) * speed),2,'rect',3,i[8],pygame.Vector2(math.sin(math.radians(curangle)) * speed,math.cos(math.radians(curangle)) * speed),roomcord.copy()])
                            curangle = 0

                        bullets.remove(i)
                        break
                    elif tile == 4 and pygame.FRect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).collidepoint(i[0]):
                        bullets.remove(i)
                        break

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
                    if tile in [1] and pygame.FRect(x * 32 + 60 - 64,y * 32 + 32 - 64,32,32).collidepoint(i[0]): 
                        # i[7].y *= -1
                        # i[0].y += i[7].y * dt
                        for a in range(1):
                            curangle = random.randint(0,180)
                            speed = random.randint(0,3)
                            # print(curangle)
                            particles.append([i[0],pygame.Vector2(math.sin(math.radians(curangle)) * speed,math.cos(math.radians(curangle)) * speed),4,'rect',3,i[8],pygame.Vector2(math.sin(math.radians(curangle)) * speed,math.cos(math.radians(curangle)) * speed),roomcord.copy()])
                            curangle = 0

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

    pygame.draw.circle(window,(0,255,0),playerrect.center,4)

    # pygame.draw.rect(window,(255,0,0),(playerrect.x-128+12,playerrect.y-128+12,256,256))
    pygame.draw.rect(window,(0,0,255),playerrect)
    
    angle = math.degrees(math.atan2(mousepos.x-playerrect.centerx,mousepos.y-playerrect.centery)) - 90 + recoil
    rotgun = rot_center(pygame.transform.flip(gunsprite,False,True) if angle < -90 else gunsprite,angle,playerrect.centerx,playerrect.centery)
    # print(math.degrees(math.atan2(mousepos.x-playerrect.centerx,mousepos.y-playerrect.centery)) - 90)
    # window.blit(gunsprite,playerrect.topleft - pygame.Vector2(128,128) + pygame.Vector2(12,12))
    window.blit(rotgun[0],rotgun[1])

    # debug

    window.blit(fontsmall.render(f"DEBUG MENU",True,(255,255,255),(128,0,128)),(0,0))
    window.blit(fontsmall.render(f"FPS: {round(clock.get_fps(),2)}",True,(255,255,255),(0,0,128)),(0,16))
    window.blit(fontsmall.render(f"ENTITIES: {len(bullets) + len(particles)}",True,(255,255,255),(0,128,0)),(0,32))


    # minimap.fill((0,0,0))
    window.blit(fontsmall.render(f"{int(roomcord.x)} {int(roomcord.y)}",True,(255,255,255)),(window.get_width()-4-16-fontsmall.render(f"{int(roomcord.x)} {int(roomcord.y)}",True,(255,255,255)).get_width(),160 - fontsmall.get_height() - 2 + 20))
    window.blit(minimap,(window.get_width()-150-16,10))

    # 28
    for y in range(len(rooms)):
        for x in range(len(rooms[0])):
            if pygame.Vector2(x,y) == roomcord:pygame.draw.rect(window,(0,255,0),(x*28 + 5 + window.get_width()-20 - 150 + 8,y*28 + 19,20,20))
            elif rooms[y][x] != -1: pygame.draw.rect(window,(255,255,255),(x*28 + 5 + window.get_width()-20 - 150 + 8,y*28 + 19,20,20))
            if rooms[y][x] != -1: window.blit(fontsmall.render(str(rooms[y][x]),True,(255,0,0)),(x*28 + 5 + window.get_width()-20 - 150 + 8,y*28 + 19))


    # window.blit(pygame.transform.invert(window),(0,0))

    pygame.display.flip()