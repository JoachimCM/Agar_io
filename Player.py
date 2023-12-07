import math, random, pygame, sys
from Drawable import *
from config import *
from Miam import *

pygame.font.init()
FONT = pygame.font.SysFont("Arial", 20)

def drawText(message,pos,color=(0,0,0)):
    SCREEN.blit(FONT.render(message, 1, color), pos)

def getDistance(a, b):
    x = math.fabs(a[0]-b[0])
    y = math.fabs(a[1]-b[1])
    return ((x**2)+(y**2))**(0.5)

class Player(Drawable):
    NAME_COLOR = (0, 0, 0)
    
    def __init__(self, surface, camera, name=""):
        super().__init__(surface, camera)
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.mass = 15
        self.speed = 5
        self.color = (230, 255, 0)
        self.outline_color = (255, 255, 255)
        self.name = name
        
    def move(self, key):
        
        if key == pygame.K_RIGHT:
            self.x += self.speed
            
        if key == pygame.K_LEFT:
            self.x -= self.speed
        
        if key == pygame.K_UP:
            self.y -= self.speed
            
        if key == pygame.K_DOWN:
            self.y += self.speed
            
    def scrounch(self, miams, particles):
        for miam in miams:
            if getDistance((miam.x, miam.y), (self.x, self.y)) <= self.mass/2:
                self.mass += 0.5
                miams.remove(miam)
                particles.append([[SCREEN_WIDTH/2 , SCREEN_HEIGHT/2], [random.randint(0, 20) / 10 - 1, -5], random.randint(6, 11)])
                miams.append(Miam(self.surface, self.camera))
                
    
    def give_miam(self):
        pass
    
    def split(self):
        pass
    
    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))
        
        pygame.draw.circle(self.surface, self.outline_color, center, 
                           int((self.mass / 2 + 3) * zoom))
        pygame.draw.circle(self.surface, self.color, center, 
                           int(self.mass / 2 * zoom))
        front_width, front_height = FONT.size(self.name)
        drawText(self.name, (self.x * zoom + x - int(front_width / 2), 
                             self.y * zoom + y - int(front_height / 2)),
                             Player.NAME_COLOR)