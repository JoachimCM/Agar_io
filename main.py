# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:37:45 2023

"""
import pygame, sys, random, math

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = (800,500)
PLATFORM_SIZE = 2000
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
GRID_SIZE = 25
SIZE_OF_FOOD = 10
NB_FOOD = 4000

pygame.display.set_caption("Agar.io")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)
    
def drawText(message,pos,color=(0,0,0)):
    SCREEN.blit(font.render(message, 1, color), pos)

def getDistance(a, b):
    x = math.fabs(a[0]-b[0])
    y = math.fabs(a[1]-b[1])
    return ((x**2)+(y**2))**(0.5)

class Drawable:
    
    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera
        
    def draw(self):
        pass
    
class Grid(Drawable):
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = (255,255,255)
        
        
    def draw(self, ):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0, PLATFORM_SIZE + 1, GRID_SIZE):
            pygame.draw.line(self.surface, self.color, (x, i * zoom + y),
                                ((PLATFORM_SIZE + 1) * zoom + x, i * zoom + y), 3)
            pygame.draw.line(self.surface, self.color, (i * zoom + x, y),
                                (i * zoom + x, (PLATFORM_SIZE + 1) * zoom + y), 3)


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
            
    def scrounch(self, miams):
        for miam in miams:
            if getDistance((miam.x, miam.y), (self.x, self.y)) <= self.mass/2:
                self.mass += 0.1
                miams.remove(miam)
    
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
        front_width, front_height = font.size(self.name)
        drawText(self.name, (self.x * zoom + x - int(front_width / 2), 
                             self.y * zoom + y - int(front_height / 2)),
                             Player.NAME_COLOR)
    
class Food(Drawable):
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = [random.random() * 255, random.random() * 255, random.random() * 255]
        self.x = (random.random() * (PLATFORM_SIZE - (SIZE_OF_FOOD * 4))) + SIZE_OF_FOOD * 2
        self.y = (random.random() * (PLATFORM_SIZE - (SIZE_OF_FOOD * 4))) + SIZE_OF_FOOD * 2
    
    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        pygame.draw.circle(
            self.surface,
            self.color, 
            [self.x * zoom + x, self.y * zoom + y], 
            SIZE_OF_FOOD)
    
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
        self.center(player)
        
class Painter:

    def __init__(self):
        self.paintings = []

    def add(self, drawable):
        self.paintings.append(drawable)

    def paint(self):
        for drawing in self.paintings:
            drawing.draw()

def draw_all_food(surface, camera):
    pantry = []
    random.seed(random.random())
    for i in range(0, NB_FOOD):
        new_food = Food(surface, camera)
        pantry.append(new_food)
    return pantry

camera = Camera()
grid = Grid(SCREEN, camera)
player = Player(SCREEN, camera, "Oeuf au plat")

pantry = draw_all_food(SCREEN, camera)
nb_food = NB_FOOD

painter = Painter()
painter.add(grid)
for food in pantry:
    painter.add(food)
painter.add(player)

player_movement = False
event_key = 0

while True:
    
    clock.tick(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            player_movement = True
            event_key = event.key
        if event.type == pygame.KEYUP:
            player_movement = False
    
    if player_movement:
        player.move(event_key)
        pantry = draw_all_food(SCREEN, camera)
    
    camera.update(player)
    SCREEN.fill((0,0,0))
    painter.paint()
    pygame.display.flip()
