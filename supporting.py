import pygame
import os
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
spritesheet = pygame.image.load(os.path.join(img_folder, 'spritesheet.png'))

def x17(x):
    return x*17

def dirt(self):
    self.image.blit(spritesheet, (0,0), (x17(10),x17(8),16,16))

def wall(self):
    self.image.blit(spritesheet, (0,0), (x17(10),x17(2),16,16))