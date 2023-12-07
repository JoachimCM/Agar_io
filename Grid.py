from Drawable import Drawable
from config import *

class Grid(Drawable):
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = (255,255,255)
        
        
    def draw(self, ):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        print(int(((GRID_SIZE) / zoom) / (GRID_SIZE/2)))
        for i in range(0, PLATFORM_SIZE + 1, GRID_SIZE * (1 + int(((GRID_SIZE) / zoom) / (GRID_SIZE/2)))):
            pygame.draw.line(self.surface, self.color, (x, i * zoom + y),
                                ((PLATFORM_SIZE + 1) * zoom + x, i * zoom + y), 3)
            pygame.draw.line(self.surface, self.color, (i * zoom + x, y),
                                (i * zoom + x, (PLATFORM_SIZE + 1) * zoom + y), 3)