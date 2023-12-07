import pygame
from random import random

class Food:
    
    def __init__(self, size, screen_weight, screen_height, screen):
        self.size = size
        self.color = [random() * 255, random() * 255, random() * 255]
        self.position = [(random() * (screen_weight-(size*4))) + size*2, (random() * (screen_height-(size*4))) + size * 2]
        pygame.draw.circle(
            screen, 
            self.color, 
            self.position, 
            self.size)