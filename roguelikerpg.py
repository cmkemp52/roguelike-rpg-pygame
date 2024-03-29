import pygame
import random
import os
from floors import *
from supporting import *

#set up assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
charsheet = pygame.image.load(os.path.join(img_folder, 'characters.png'))
parch = pygame.image.load(os.path.join(img_folder, 'parchment.png'))
abe = pygame.image.load(os.path.join(img_folder, 'abe.png'))
healthsheet = pygame.image.load(os.path.join(img_folder, 'redSheet.png'))
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.init()
soundeff = pygame.mixer.Sound(os.path.join(img_folder, "soundeffect2.ogg"))
song = pygame.mixer.music.load(os.path.join(img_folder, "game song.mp3"))
doorsound = pygame.mixer.Sound(os.path.join(img_folder, "doorsound.ogg"))
armorsound = pygame.mixer.Sound(os.path.join(img_folder, "armor.ogg"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.3)

#Parameters
WIDTH = 800
HEIGHT = 600
FPS = 30
gturn = 0
#font for texts
pygame.font.init()
font = pygame.font.Font(os.path.join(img_folder,"sunflower.otf"),16)
gofont = pygame.font.Font(os.path.join(img_folder,"sunflower.otf"),50)
gotext = gofont.render('Game Over', True, (255,255,255))
gorect = gotext.get_rect()
gorect.center = (WIDTH // 2, HEIGHT // 2)
ywtext = gofont.render('You WIN!!!', True, (255,255,255))
ywrect = ywtext.get_rect()
ywrect.center = (WIDTH // 2, HEIGHT // 2)
#log for text on screen
textlog = []
#enemy locations
enemylocations = []
cfloor = floor1
cmons = floor1mons
bosscord = [[18, 13]]
youwin = 0

itemlocations = []

class Item(pygame.sprite.Sprite):
    def __init__(self):
        #initializing
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 18))
        self.loc = [2, 4]
        self.name = 'healthpack'
        self.rect = self.image.get_rect()
        self.rect.center = [398+self.loc[0]*16,50+self.loc[1]*16]
        #set background
        if cfloor[self.loc[0]][self.loc[1]] == 0:
            dirt(self)
        elif cfloor[self.loc[0]][self.loc[1]] == 1:
            wall(self)
        elif cfloor[self.door[0]][self.loc[1]] == 7:
            doors(self)
        self.image.blit(healthsheet, (0,2), (379,109,14,14))
        #set back to black
        void(self)
        

#Creating the side parchment with image/text
class Sideimg(pygame.sprite.Sprite):
    def __init__(self):
        #initializing
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1000, 1200))
        self.loc = [9999,9999]
        self.name = "parchment"
        #placement
        self.rect = self.image.get_rect()
        self.rect.center = [-50,0]
    def update(self):
        #clears old images
        void(self)
        #sets images
        self.image.blit(parch, (0,0))
        self.image.blit(abe, (580,630), (0,0,200,300))
        #set text
        nametext = font.render('Abraham Lincoln', True, (0,0,0))
        titletext = font.render('President', True, (0,0,0))
        buttext = font.render('But Also', True, (0,0,0))
        slayertext = font.render('Slayer of Goblins', True, (0,0,0))
        self.image.blit(nametext,(660,630))
        self.image.blit(titletext,(670,650))
        self.image.blit(buttext,(690,670))
        self.image.blit(slayertext,(670,690))
        #set health
        Healthtext = font.render(f'Abe\'s health:   {player.currenthealth} / {player.maxhealth}', True, (0,0,0))
        self.image.blit(Healthtext,(580,730))
        
        #set log
        if len(textlog) >0:
            in0text = font.render(textlog[0], True, (0,0,0))
            self.image.blit(in0text,(580,780))
        if len(textlog) >1:
            in1text = font.render(textlog[1], True, (0,0,0))
            self.image.blit(in1text,(580,805))
        if len(textlog) >2:
            in2text = font.render(textlog[2], True, (0,0,0))
            self.image.blit(in2text,(580,830))
        if len(textlog) >3:
            in3text = font.render(textlog[3], True, (0,0,0))
            self.image.blit(in3text,(580,855))
        if len(textlog) >4:
            in3text = font.render(textlog[4], True, (0,0,0))
            self.image.blit(in3text,(580,880))
        if len(textlog) >5:
            in3text = font.render(textlog[5], True, (0,0,0))
            self.image.blit(in3text,(580,905))
        if len(textlog) >6:
            in3text = font.render(textlog[6], True, (0,0,0))
            self.image.blit(in3text,(580,930))
        if len(textlog) >7:
            in3text = font.render(textlog[7], True, (122, 118, 106))
            self.image.blit(in3text,(580,955))
        if len(textlog) >8:
            in4text = font.render(textlog[8], True, (122, 118, 106))
            self.image.blit(in4text,(580,980))
        if len(textlog) >9:
            in4text = font.render(textlog[9], True, (199, 193, 177))
            self.image.blit(in4text,(580,1005))


#function which sets text log
def textset(txt):
    if len(textlog) < 10:
        textlog.insert(0,txt)
    else:
        textlog.insert(0,txt)
        textlog.pop(10)

#main character setup
def charsprite(self):
    #set back to black
    void(self)
    #set background
    if cfloor[self.loc[0]][self.loc[1]] == 0:
        self.image.blit(spritesheet, (0,2), (x17(10),x17(8),16,16))
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
    elif self.armor == 2:
        self.image.blit(charsheet, (0,2), (x17(7),0,16,16))
    #set character pants
    self.image.blit(charsheet, (0,2), (x17(3),17,16,16))
    #set character hair
    self.image.blit(charsheet, (0,2), (x17(22),0,16,16))
    #set character weapon
    if self.weapon == 0:
        self.image.blit(charsheet, (0,2), (x17(49),0,16,16))
    elif self.weapon == 1:
        self.image.blit(charsheet, (0,2), (x17(51),x17(9),16,16))
    elif self.weapon == 2:
        self.image.blit(charsheet, (0,2), (x17(51),x17(7),16,16))
    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #initialize sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 18))
        #set character location
        self.loc = [2,2]
        #set character stats
        self.maxhealth = 30
        self.currenthealth = 30
        self.power = 5
        self.name = "Player"
        self.lineofsight = 4
        self.armor = 0
        self.weapon = 0
        #set location
        self.rect = self.image.get_rect()
        self.rect.center = [398+self.loc[0]*16,50+self.loc[1]*16]
    def weapup(self):
        textset("You find a better weapon")
        self.weapon+=1
        if self.weapon == 1:
            self.power = 10
            self.weapon = 1
        if self.weapon == 2:
            self.power = 15
            self.weapon = 2

    def armup(self):
        armorsound.play()
        textset("You find better armor")
        self.armor+=1
        if self.armor == 1:
            self.maxhealth = 45
            self.currenthealth = 45
        if self.armor == 2:   
            self.maxhealth = 60
            self.currenthealth = 60


    def attack(self,enemy):
        if enemy.name == "goblin":
            enemy.currenthealth-=self.power
            quote=random.randint(1,10)
            if(quote==5):
                textset("I shall kill them all...")
            if(quote==10):
                textset("Die, you mutant greenbeans!")
            textset(f"You do {self.power} damage!")
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

def checkLeft(self,player):
    locations = [[self.loc[0],self.loc[1]-2],[self.loc[0]+1,self.loc[1]-1],[self.loc[0]-1,self.loc[1]-1],[self.loc[0],self.loc[1]-3],[self.loc[0]+1,self.loc[1]-2],[self.loc[0]-1,self.loc[1]-2,[self.loc[0],self.loc[1]-4],[self.loc[0]+1,self.loc[1]-3],[self.loc[0]-1,self.loc[1]-3]]]
    if player.loc in locations:
        return True
    else:
        return False 
def checkRight(self,player):
    locations = [[self.loc[0],self.loc[1]+2],[self.loc[0]+1,self.loc[1]+1],[self.loc[0]-1,self.loc[1]+1],[self.loc[0],self.loc[1]+3],[self.loc[0]+1,self.loc[1]+2],[self.loc[0]-1,self.loc[1]+2,[self.loc[0],self.loc[1]+4],[self.loc[0]+1,self.loc[1]+3],[self.loc[0]-1,self.loc[1]+3]]]
    if player.loc in locations:
        return True
    else:
        return False 
def checkUp(self,player):
    locations = [[self.loc[0]+2,self.loc[1]],[self.loc[0]+1,self.loc[1]+1],[self.loc[0]+1,self.loc[1]-1],[self.loc[0]+3,self.loc[1]],[self.loc[0]+2,self.loc[1]+1],[self.loc[0]+2,self.loc[1]-1,[self.loc[0]+4,self.loc[1]],[self.loc[0]+3,self.loc[1]-1],[self.loc[0]+3,self.loc[1]+1]]]
    if player.loc in locations:
        return True
    else:
        return False 
def checkDown(self,player):
    locations = [[self.loc[0]-2,self.loc[1]],[self.loc[0]-1,self.loc[1]+1],[self.loc[0]-1,self.loc[1]-1],[self.loc[0]-3,self.loc[1]],[self.loc[0]-2,self.loc[1]+1],[self.loc[0]-2,self.loc[1]-1,[self.loc[0]-4,self.loc[1]],[self.loc[0]-3,self.loc[1]-1],[self.loc[0]-3,self.loc[1]+1]]]
    if player.loc in locations:
        return True
    else:
        return False 
def gobattack(self,player):
    near = [[self.loc[0],self.loc[1]-1],[self.loc[0],self.loc[1]+1],[self.loc[0]-1,self.loc[1]],[self.loc[0]+1,self.loc[1]]]
    if player.loc in near and self.currenthealth > 0:
        player.currenthealth-=self.power
        return True
    else:
        return False
def goblinsprite(self):
    #set back to black
    void(self)
    if cfloor[self.loc[0]][self.loc[1]] == 0:
        self.image.blit(spritesheet, (0,2), (x17(10),x17(8),16,16))
    self.image.blit(charsheet, (0,2), (0,x17(3),16,16))

class Goblin(pygame.sprite.Sprite):
    def __init__(self, locat):
        #initialize sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 18))
        self.maxhealth = 6
        self.currenthealth = 6
        self.name = "goblin"
        self.power = 2
        self.loc=locat
        self.lturn = gturn
        self.rect = self.image.get_rect()
        self.rect.center = [398+self.loc[0]*16,50+self.loc[1]*16]
        if cfloor == floor2:
            self.power = 3
            self.maxhealth = 12
            self.currenthealth = 12
        if cfloor == floor3:
            self.power = 5
            self.maxhealth = 15
            self.currenthealth = 15
    def attack(self,enemy):
            enemy.currenthealth-=self.power
        
    def update(self):
        while self.lturn < gturn:
            ranmove = random.randint(1,4)
            #chase after player
            if gobattack(self,player):
                textset(f"Goblin hits you for {self.power}")
            elif checkLeft(self,player):
                if cfloor[self.loc[0]][self.loc[1]-1] == 0 and [self.loc[0],self.loc[1]-1] not in enemylocations:
                    enemylocations.remove(self.loc)
                    self.loc = [self.loc[0],self.loc[1]-1]
                    enemylocations.append(self.loc)
                    self.rect.center = [self.rect.center[0],self.rect.center[1]-16]
            elif checkRight(self,player):
                if cfloor[self.loc[0]][self.loc[1]+1] == 0 and [self.loc[0],self.loc[1]+1] not in enemylocations:
                    enemylocations.remove(self.loc)
                    self.loc = [self.loc[0],self.loc[1]+1]
                    enemylocations.append(self.loc)
                    self.rect.center = [self.rect.center[0],self.rect.center[1]+16]
            elif checkUp(self,player):
                if cfloor[self.loc[0]+1][self.loc[1]] == 0 and [self.loc[0]+1,self.loc[1]] not in enemylocations:
                    enemylocations.remove(self.loc)
                    self.loc = [self.loc[0]+1,self.loc[1]]
                    enemylocations.append(self.loc)
                    self.rect.center = [self.rect.center[0]+16,self.rect.center[1]]
            elif checkDown(self,player):
                if cfloor[self.loc[0]-1][self.loc[1]] == 0 and [self.loc[0]-1,self.loc[1]] not in enemylocations:
                    enemylocations.remove(self.loc)
                    self.loc = [self.loc[0]-1,self.loc[1]]
                    enemylocations.append(self.loc)
                    self.rect.center = [self.rect.center[0]-16,self.rect.center[1]]
            elif ranmove == 1:
                if cfloor[self.loc[0]-1][self.loc[1]] == 0:
                    #if spot has an enemy, attack it
                    if [self.loc[0]-1,self.loc[1]] in enemylocations or [self.loc[0]-1,self.loc[1]]==player.loc:
                        ranmove +=1
                    #else move into that spot
                    else:
                        enemylocations.remove(self.loc)
                        self.loc = [self.loc[0]-1,self.loc[1]]
                        enemylocations.append(self.loc)
                        self.rect.center = [self.rect.center[0]-16,self.rect.center[1]]
                else:
                    ranmove+=1
            elif ranmove == 2:
                if cfloor[self.loc[0]+1][self.loc[1]] == 0:
                    #if spot has an enemy, attack it
                    if [self.loc[0]+1,self.loc[1]] in enemylocations or [self.loc[0]+1,self.loc[1]] == player.loc:
                        ranmove +=1
                    #else move into that spot
                    else:
                        enemylocations.remove(self.loc)
                        self.loc = [self.loc[0]+1,self.loc[1]]
                        enemylocations.append(self.loc)
                        self.rect.center = [self.rect.center[0]+16,self.rect.center[1]]
                else:
                    ranmove+=1
            elif ranmove == 3:
                if cfloor[self.loc[0]][self.loc[1]-1] == 0:
                    #if spot has an enemy, attack it
                    if [self.loc[0],self.loc[1]-1] in enemylocations or [self.loc[0],self.loc[1]-1] == player.loc:
                        ranmove +=1
                    #else move into that spot
                    else:
                        enemylocations.remove(self.loc)
                        self.loc = [self.loc[0],self.loc[1]-1]
                        enemylocations.append(self.loc)
                        self.rect.center = [self.rect.center[0],self.rect.center[1]-16]
                else:
                    ranmove+=1
            elif ranmove == 4:
                if cfloor[self.loc[0]][self.loc[1]+1] == 0:
                    #if spot has an enemy, attack it
                    if [self.loc[0],self.loc[1]+1] in enemylocations or [self.loc[0],self.loc[1]+1] == player.loc:
                        ranmove +=1
                    #else move into that spot
                    else:
                        enemylocations.remove(self.loc)
                        self.loc = [self.loc[0],self.loc[1]+1]
                        enemylocations.append(self.loc)
                        self.rect.center = [self.rect.center[0],self.rect.center[1]+16]
                else:
                    ranmove-=3
            self.lturn +=1
        #updates goblin's current health in healthbar
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
            #goblin dead
            if random.randint(1,10) == 10 and player.armor <2:
                player.armup()
            if random.randint(1,10) == 10 and player.weapon <2:
                player.weapup()
            textset("You kill the goblin!")
            enemylocations.remove(self.loc)
            all_sprites.remove(self)

class BossGoblin(pygame.sprite.Sprite):
    def __init__(self, locat):
        #initialize sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 18))
        self.maxhealth = 20
        self.currenthealth = 20
        self.name = "goblin"
        self.power = 5
        self.loc=locat
        self.lturn = gturn
        self.rect = self.image.get_rect()
        self.rect.center = [398+self.loc[0]*16,50+self.loc[1]*16]
    def update(self):
        while self.lturn < gturn:
            ranmove = random.randint(1,4)
            #chase after player
            if gobattack(self,player):
                textset(f"Boss Goblin hits you for {self.power}")
            elif checkLeft(self,player):
                if cfloor[self.loc[0]][self.loc[1]-1] == 0 and [self.loc[0],self.loc[1]-1] not in enemylocations:
                    enemylocations.remove(self.loc)
                    self.loc = [self.loc[0],self.loc[1]-1]
                    enemylocations.append(self.loc)
                    self.rect.center = [self.rect.center[0],self.rect.center[1]-16]
            elif checkRight(self,player):
                if cfloor[self.loc[0]][self.loc[1]+1] == 0 and [self.loc[0],self.loc[1]+1] not in enemylocations:
                    enemylocations.remove(self.loc)
                    self.loc = [self.loc[0],self.loc[1]+1]
                    enemylocations.append(self.loc)
                    self.rect.center = [self.rect.center[0],self.rect.center[1]+16]
            elif checkUp(self,player):
                if cfloor[self.loc[0]+1][self.loc[1]] == 0 and [self.loc[0]+1,self.loc[1]] not in enemylocations:
                    enemylocations.remove(self.loc)
                    self.loc = [self.loc[0]+1,self.loc[1]]
                    enemylocations.append(self.loc)
                    self.rect.center = [self.rect.center[0]+16,self.rect.center[1]]
            elif checkDown(self,player):
                if cfloor[self.loc[0]-1][self.loc[1]] == 0 and [self.loc[0]-1,self.loc[1]] not in enemylocations:
                    enemylocations.remove(self.loc)
                    self.loc = [self.loc[0]-1,self.loc[1]]
                    enemylocations.append(self.loc)
                    self.rect.center = [self.rect.center[0]-16,self.rect.center[1]]
            elif ranmove == 1:
                if cfloor[self.loc[0]-1][self.loc[1]] == 0:
                    if [self.loc[0]-1,self.loc[1]] in enemylocations or [self.loc[0]-1,self.loc[1]]==player.loc:
                        ranmove +=1
                    else:
                        enemylocations.remove(self.loc)
                        self.loc = [self.loc[0]-1,self.loc[1]]
                        enemylocations.append(self.loc)
                        self.rect.center = [self.rect.center[0]-16,self.rect.center[1]]
                else:
                    ranmove+=1
            elif ranmove == 2:
                if cfloor[self.loc[0]+1][self.loc[1]] == 0:
                    if [self.loc[0]+1,self.loc[1]] in enemylocations or [self.loc[0]+1,self.loc[1]] == player.loc:
                        ranmove +=1
                    else:
                        enemylocations.remove(self.loc)
                        self.loc = [self.loc[0]+1,self.loc[1]]
                        enemylocations.append(self.loc)
                        self.rect.center = [self.rect.center[0]+16,self.rect.center[1]]
                else:
                    ranmove+=1
            elif ranmove == 3:
                if cfloor[self.loc[0]][self.loc[1]-1] == 0:
                    if [self.loc[0],self.loc[1]-1] in enemylocations or [self.loc[0],self.loc[1]-1] == player.loc:
                        ranmove +=1
                    else:
                        enemylocations.remove(self.loc)
                        self.loc = [self.loc[0],self.loc[1]-1]
                        enemylocations.append(self.loc)
                        self.rect.center = [self.rect.center[0],self.rect.center[1]-16]
                else:
                    ranmove+=1
            elif ranmove == 4:
                if cfloor[self.loc[0]][self.loc[1]+1] == 0:
                    if [self.loc[0],self.loc[1]+1] in enemylocations or [self.loc[0],self.loc[1]+1] == player.loc:
                        ranmove +=1
                    else:
                        enemylocations.remove(self.loc)
                        self.loc = [self.loc[0],self.loc[1]+1]
                        enemylocations.append(self.loc)
                        self.rect.center = [self.rect.center[0],self.rect.center[1]+16]
                else:
                    ranmove-=3
            self.lturn +=1
        #updates goblin's current health in healthbar
        void(self)
        self.image.blit(spritesheet, (0,2), (x17(10),x17(8),16,16))
        self.image.blit(charsheet, (0,2), (0,x17(3),16,16))
        self.image.blit(charsheet, (0,2), (x17(8),17,16,16))
        self.image.blit(charsheet, (0,2), (x17(43),x17(9),16,16))
        if self.currenthealth == self.maxhealth:
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,16,2))
        elif self.currenthealth > self.maxhealth/2:
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,12,2))
        elif self.currenthealth > (self.maxhealth/2)/2:
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,8,2))
        elif self.currenthealth > 0:
            self.image.blit(spritesheet, (0,0), (x17(6),x17(12)+5,4,2))
        else:
            #goblin dead
            player.currenthealth = -50324
            all_sprites.remove(self)


class Floorset(pygame.sprite.Sprite):
    def __init__(self,locat):
        #initialize sprite
        self.currenthealth = 9999999
        self.name = "floor"
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((16, 16))
        #floor location
        self.loc = locat
        #set floor sprite location
        self.rect = self.image.get_rect()
        self.rect.center = [400+self.loc[0]*16,50+self.loc[1]*16]
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
                    textset("A goblin appears!!")
                if self.loc in bosscord and cfloor == floor3:
                    bosscord.remove(self.loc)
                    bossgoblin = BossGoblin(self.loc)
                    all_sprites.add(bossgoblin)
                    enemylocations.append(self.loc)
                    textset("You find the goblin leader!")
                if self.loc in cfloor == floor1:
                    item.remove(self.loc)
                    item = Item(self.loc)
                    all_sprites.add(item)
                    itemlocations.append(self.loc)
            else:
                void(self)

def floorcreation():
    #deletes old floor
    for sprite in all_sprites:
        if sprite.name == "floor":
            all_sprites.remove(sprite)
        if sprite.name == "goblin":
            all_sprites.remove(sprite)
    #creates new floor sprites
    for i in range(len(cfloor)):
        for x in range(len(cfloor[i])):
            floorsprite = Floorset([i,x])
            all_sprites.add(floorsprite)
    all_sprites.remove(player)
    all_sprites.add(player)
    player.loc = [2,2]
    player.rect.center = [398+player.loc[0]*16,50+player.loc[1]*16]


#initialize and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Roguelike RPG")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
sb = Sideimg()
all_sprites.add(sb)
player = Player()
item = Item()
all_sprites.add(item)
#creates floor sprites
floorcreation()
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
            gturn +=1
            if event.key == pygame.K_LEFT:
                #if spot is a floor
                if cfloor[player.loc[0]-1][player.loc[1]] == 0:
                    #if spot has an enemy, attack it
                    if [player.loc[0]-1,player.loc[1]] in enemylocations:
                        for goblin in all_sprites:
                            if goblin.loc == [player.loc[0]-1,player.loc[1]] and goblin.name == "goblin":
                                player.attack(goblin)
                                soundeff.play(0)
                    #else move into that spot
                    else:
                        player.loc = [player.loc[0]-1,player.loc[1]]
                        player.rect.center = [player.rect.center[0]-16,player.rect.center[1]]
                #if floor is a door, go to next floor
                elif cfloor[player.loc[0]-1][player.loc[1]] == 7:
                    doorsound.play()
                    if cfloor == floor1:
                        cfloor = floor2
                        cmons = floor2mons
                        textset("You reach the second floor")
                        textset("Goblins are stronger!")
                    elif cfloor == floor2:
                        cmons = floor3mons 
                        cfloor = floor3
                        textset("You reach the final floor")
                    floorcreation()
            if event.key == pygame.K_RIGHT:
                if cfloor[player.loc[0]+1][player.loc[1]] == 0:
                    if [player.loc[0]+1,player.loc[1]] in enemylocations:
                        for goblin in all_sprites:
                            if goblin.loc == [player.loc[0]+1,player.loc[1]] and goblin.name == "goblin":
                                player.attack(goblin)
                                soundeff.play(0)
                    else:
                        player.loc = [player.loc[0]+1,player.loc[1]]
                        player.rect.center = [player.rect.center[0]+16,player.rect.center[1]]
                elif cfloor[player.loc[0]+1][player.loc[1]] == 7:
                    doorsound.play()
                    if cfloor == floor1:
                        cfloor = floor2
                        cmons = floor2mons
                        textset("You reach the second floor")
                        textset("Goblins are stronger!")
                    elif cfloor == floor2:
                        cfloor = floor3
                        cmons = floor3mons 
                        textset("You reach the final floor")
                    floorcreation()
            if event.key == pygame.K_UP:
                if cfloor[player.loc[0]][player.loc[1]-1] == 0:
                    if [player.loc[0],player.loc[1]-1] in enemylocations:
                        for goblin in all_sprites:
                            if goblin.loc == [player.loc[0],player.loc[1]-1] and goblin.name == "goblin":
                                player.attack(goblin)
                                soundeff.play(0)
                    else:
                        player.loc = [player.loc[0],player.loc[1]-1]
                        player.rect.center = [player.rect.center[0],player.rect.center[1]-16]
                elif cfloor[player.loc[0]][player.loc[1]-1] == 7:
                    doorsound.play()
                    if cfloor == floor1:
                        cfloor = floor2
                        cmons = floor2mons
                        textset("You reach the second floor")
                        textset("Goblins are stronger!")
                    elif cfloor == floor2:
                        cfloor = floor3
                        cmons = floor3mons 
                        textset("You reach the final floor")
                    floorcreation()
            if event.key == pygame.K_DOWN:
                if cfloor[player.loc[0]][player.loc[1]+1] == 0:
                    if [player.loc[0],player.loc[1]+1] in enemylocations:
                        for goblin in all_sprites:
                            if goblin.loc == [player.loc[0],player.loc[1]+1] and goblin.name == "goblin":
                                player.attack(goblin)
                                soundeff.play(0)
                                
                    else:
                        player.loc = [player.loc[0],player.loc[1]+1]
                        player.rect.center = [player.rect.center[0],player.rect.center[1]+16]
                elif cfloor[player.loc[0]][player.loc[1]+1] == 7:
                    doorsound.play()
                    if cfloor == floor1:
                        cfloor = floor2
                        cmons = floor2mons
                        textset("You reach the second floor")
                        textset("Goblins are stronger!")
                    elif cfloor == floor2:
                        cfloor = floor3
                        cmons = floor3mons 
                        textset("You reach the final floor")
                    floorcreation()
    
    
    #Update
    all_sprites.update()

    #screen rendering
    screen.fill(BLACK)
    all_sprites.draw(screen)
    if player.currenthealth == -50324:
        screen.fill(BLACK)
        display_surface = pygame.display.set_mode((WIDTH,HEIGHT )) 
        display_surface.blit(ywtext, ywrect)
    elif player.currenthealth <1:
        screen.fill(BLACK)
        display_surface = pygame.display.set_mode((WIDTH,HEIGHT )) 
        display_surface.blit(gotext, gorect)
    pygame.display.flip()

pygame.quit()