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
enemylocations = []
cfloor = floor1
cmons = floor1mons

def charsprite(self):
    #set background
    if cfloor[self.loc[0]][self.loc[1]] == 0:
        dirt(self)
    elif cfloor[self.loc[0]][self.loc[1]] == 1:
        wall(self)
    elif cfloor[self.door[0]][self.loc[1]] == 7:
        doors(self)
    #set character base model
    self.image.blit(charsheet, (0,2), (0,0,16,16))
    #set character armor
    if self.armor == 0:
        self.image.blit(charsheet, (0,2), (x17(10),0,16,16))
    elif self.armor == 1:
        self.image.blit(charsheet, (0,2), (x17(16),17,16,16))
    #set character pants
    self.image.blit(charsheet, (0,2), (x17(3),17,16,16))
    #set character hair
    self.image.blit(charsheet, (0,2), (x17(26),0,16,16))
    #set character weapon
    if self.weapon == 0:
        self.image.blit(charsheet, (0,2), (x17(49),0,16,16))
    elif self.weapon == 1:
        self.image.blit(charsheet, (0,2), (x17(51),x17(9),16,16))
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #initialize sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 18))
        #set character location
        self.loc = [2,2]
        #set character stats
        self.maxhealth = 1
        self.currenthealth = 1
        self.power = 5
        self.lineofsight = 4
        self.armor = 0
        self.weapon = 0
        #set location
        self.rect = self.image.get_rect()
        self.rect.center = [198+self.loc[0]*16,200+self.loc[1]*16]
    def attack(self,enemy):
        enemy.currenthealth-=self.power
    def update(self):
        if self.currenthealth == self.maxhealth:
            charsprite(self)
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,16,2))
        elif self.currenthealth > self.maxhealth/2:
            charsprite(self)
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,12,2))
        elif self.currenthealth > (self.maxhealth/2)/2:
            charsprite(self)
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,8,2))
        else:
            charsprite(self)
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,4,2))

def goblinsprite(self):
    if cfloor[self.loc[0]][self.loc[1]] == 0:
        dirt(self)
    elif cfloor[self.loc[0]][self.loc[1]] == 1:
        wall(self)
    self.image.blit(charsheet, (0,2), (0,x17(3),16,16))

class Goblin(pygame.sprite.Sprite):
    def __init__(self, locat):
        #initialize sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 18))
        self.maxhealth = 30
        self.currenthealth = 30
        self.power = 5
        self.loc=locat
        self.rect = self.image.get_rect()
        self.rect.center = [198+self.loc[0]*16,200+self.loc[1]*16]
    def attack(self,enemy):
        enemy.currenthealth-=self.power
    def update(self):
        if self.currenthealth == self.maxhealth:
            goblinsprite(self)
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,16,2))
        elif self.currenthealth > self.maxhealth/2:
            goblinsprite(self)
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,12,2))
        elif self.currenthealth > (self.maxhealth/2)/2:
            goblinsprite(self)
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,8,2))
        elif self.currenthealth > 0:
            goblinsprite(self)
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,4,2))
        else:
            enemylocations.remove(self.loc)
            all_sprites.remove(self)


class Floorset(pygame.sprite.Sprite):
    def __init__(self,locat):
        #initialize sprite
        self.currenthealth = 9999999
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
                if cfloor[self.loc[0]][self.loc[1]] == 0:
                    dirt(self)
                elif cfloor[self.loc[0]][self.loc[1]] == 1:
                    wall(self)
                elif cfloor[self.loc[0]][self.loc[1]] == 9:
                    void(self)
                elif cfloor[self.loc[0]][self.loc[1]] == 7:
                    doors(self)
                if self.loc in cmons:
                    cmons.remove(self.loc)
                    goblin = Goblin(self.loc)
                    enemylocations.append(self.loc)
                    all_sprites.add(goblin)
            else:
                void(self)




#initialize and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Roguelike RPG")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
#creates floor sprites
for i in range(len(cfloor)):
    for x in range(len(cfloor[i])):
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
                if cfloor[player.loc[0]-1][player.loc[1]] == 0:
                    if [player.loc[0]-1,player.loc[1]] in enemylocations:
                        for goblin in all_sprites:
                            if goblin.loc == [player.loc[0]-1,player.loc[1]]:
                                #goblin.attack(player) is giving the: errorAttributeError: 'Floorset' object has no attribute 'attack'
                                player.attack(goblin)
                    else:
                        player.loc = [player.loc[0]-1,player.loc[1]]
                        player.rect.center = [player.rect.center[0]-16,player.rect.center[1]]
            if event.key == pygame.K_RIGHT:
                if cfloor[player.loc[0]+1][player.loc[1]] == 0:
                    if [player.loc[0]+1,player.loc[1]] in enemylocations:
                        for goblin in all_sprites:
                            if goblin.loc == [player.loc[0]+1,player.loc[1]]:
                                #goblin.attack(player) is giving the: errorAttributeError: 'Floorset' object has no attribute 'attack'
                                player.attack(goblin)
                    else:
                        player.loc = [player.loc[0]+1,player.loc[1]]
                        player.rect.center = [player.rect.center[0]+16,player.rect.center[1]]
            if event.key == pygame.K_UP:
                if cfloor[player.loc[0]][player.loc[1]-1] == 0:
                    if [player.loc[0],player.loc[1]-1] in enemylocations:
                        for goblin in all_sprites:
                            if goblin.loc == [player.loc[0],player.loc[1]-1]:
                                #goblin.attack(player) is giving the: errorAttributeError: 'Floorset' object has no attribute 'attack'
                                player.attack(goblin)
                    else:
                        player.loc = [player.loc[0],player.loc[1]-1]
                        player.rect.center = [player.rect.center[0],player.rect.center[1]-16]
            if event.key == pygame.K_DOWN:
                if cfloor[player.loc[0]][player.loc[1]+1] == 0:
                    if [player.loc[0],player.loc[1]+1] in enemylocations:
                        for goblin in all_sprites:
                            if goblin.loc == [player.loc[0],player.loc[1]+1]:
                                #goblin.attack(player) is giving the: errorAttributeError: 'Floorset' object has no attribute 'attack'
                                player.attack(goblin)
                    else:
                        player.loc = [player.loc[0],player.loc[1]+1]
                        player.rect.center = [player.rect.center[0],player.rect.center[1]+16]
    
    #Update
    all_sprites.update()

    #screen rendering
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()