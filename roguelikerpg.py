import pygame
import random
import os
from floors import *
from supporting import *

#set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
charsheet = pygame.image.load(os.path.join(img_folder, 'characters.png'))


#Parameters
WIDTH = 800
HEIGHT = 800
FPS = 30

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        #initialize sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 16))
        #set character location
        self.loc = [2,2]
        #set character stats
        self.lineofsight = 4
        self.armor = 0
        self.weapon = 0
        #set background
        if floor1[self.loc[0]][self.loc[1]] == 0:
            dirt(self)
        elif floor1[self.loc[0]][self.loc[1]] == 1:
            wall(self)
        #set character base model
        self.image.blit(charsheet, (0,0), (0,0,16,16))
        #set character armor
        if self.armor == 0:
            self.image.blit(charsheet, (0,0), (x17(10),0,16,16))
        elif self.armor == 1:
            self.image.blit(charsheet, (0,0), (x17(16),17,16,16))
        #set character pants
        self.image.blit(charsheet, (0,0), (x17(3),17,16,16))
        #set character hair
        self.image.blit(charsheet, (0,0), (x17(26),0,16,16))
        #set character weapon
        if self.weapon == 0:
            self.image.blit(charsheet, (0,0), (x17(49),0,16,16))
        elif self.weapon == 1:
            self.image.blit(charsheet, (0,0), (x17(51),x17(9),16,16))
        #set character location
        self.rect = self.image.get_rect()
        self.rect.center = [200+self.loc[0]*16,200+self.loc[1]*16]

class Floorset(pygame.sprite.Sprite):
    def __init__(self,locat):
        #initialize sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 16))
        #floor location
        self.loc = locat
        #set floor sprite location
        self.rect = self.image.get_rect()
        self.rect.center = [200+self.loc[0]*16,200+self.loc[1]*16]
    def update(self):
        #generating vision list
        visible = []
        for i in range(0,player.lineofsight):
            for x in range(0,player.lineofsight):
                visible.append([player.loc[0]+i,player.loc[1]+x])
                visible.append([player.loc[0]-i,player.loc[1]+x])
                visible.append([player.loc[0]+i,player.loc[1]-x])
                visible.append([player.loc[0]-i,player.loc[1]-x])
        #shows floors based on player's line of sight variable
            if self.loc in visible:
                if floor1[self.loc[0]][self.loc[1]] == 0:
                    dirt(self)
                elif floor1[self.loc[0]][self.loc[1]] == 1:
                    wall(self)
            else:
                self.image.fill(BLACK)




#initialize and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Roguelike RPG")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
#creates floor sprites
for i in range(len(floor1)):
    for x in range(len(floor1[i])):
        floorsprite = Floorset([i,x])
        all_sprites.add(floorsprite)
#creates player
all_sprites.add(player)



#the GAME
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)

    #inputs
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if(floor1[player.loc[0]-1][player.loc[1]] == 0):
                    player.loc = [player.loc[0]-1,player.loc[1]]
                    print(player.loc)
                    player.rect.center = [player.rect.center[0]-16,player.rect.center[1]]
            if event.key == pygame.K_RIGHT:
                if(floor1[player.loc[0]+1][player.loc[1]] == 0):
                    player.loc = [player.loc[0]+1,player.loc[1]]
                    print(player.loc)
                    player.rect.center = [player.rect.center[0]+16,player.rect.center[1]]
            if event.key == pygame.K_UP:
                if(floor1[player.loc[0]][player.loc[1]-1] == 0):
                    player.loc = [player.loc[0],player.loc[1]-1]
                    player.rect.center = [player.rect.center[0],player.rect.center[1]-16]
            if event.key == pygame.K_DOWN:
                if(floor1[player.loc[0]][player.loc[1]+1] == 0):
                    player.loc = [player.loc[0],player.loc[1]+1]
                    player.rect.center = [player.rect.center[0],player.rect.center[1]+16]
    
    #Update
    all_sprites.update()

    #screen rendering
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()