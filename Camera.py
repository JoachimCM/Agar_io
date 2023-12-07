from config import *
from Player import *

class Camera: 
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.zoom = 0.5
        
    def center(self, element):
        if isinstance(element, Player):
            x, y = element.x, element.y
            self.x = (x - (x * self.zoom)) - x + (SCREEN_WIDTH/2)
            self.y = (y - (y * self.zoom)) - y + (SCREEN_HEIGHT/2)
        elif type(element) == tuple:
            self.x, self.y = element
        
    def update(self, target):
        self.zoom = 100/target.mass+0.5
        self.center(target)