
import pygame 
import random
import math
import time
from pygame import time
from pygame import mixer
from threading import Thread
import Game

class Spritesheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
            image = pygame.Surface((width, height)).convert_alpha()
            image.blit(self.sheet, (0, 0), ((frame*width), 0, width, height))
            image = pygame.transform.scale(image, (width*scale, height*scale))
            image.set_colorkey(colour)

            return image
        
  