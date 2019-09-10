import pygame
import os
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
spritesheet = pygame.image.load(os.path.join(img_folder, 'spritesheet.png'))
charsheet = pygame.image.load(os.path.join(img_folder, 'characters.png'))
doorsheet = pygame.image.load(os.path.join(img_folder, 'doors.png'))

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def x17(x):
    return x*17

def dirt(self):
    self.image.blit(spritesheet, (0,0), (x17(10),x17(8),16,16))

def wall(self):
    self.image.blit(spritesheet, (0,0), (x17(10),x17(2),16,16))

def void(self):
    self.image.fill(BLACK)
def doors(self):
    self.image.blit(spritesheet, (0,0), (x17(10),x17(8),16,16))
    self.image.blit(doorsheet, (0,0), (x17(42),x17(2), 16,16))