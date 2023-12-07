import random
from Drawable import *
from config import *

class Miam(Drawable):
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(SIZE_OF_FOOD*2,PLATFORM_SIZE-SIZE_OF_FOOD*2)
        self.y = random.randint(SIZE_OF_FOOD*2,PLATFORM_SIZE-SIZE_OF_FOOD*2)
        self.mass = SIZE_OF_FOOD
        self.color = (random.randint(0, 255), 
                      random.randint(0, 255), 
                      random.randint(0, 255))
        
    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))
        pygame.draw.circle(self.surface, self.color, center, 
                           int(self.mass * zoom))