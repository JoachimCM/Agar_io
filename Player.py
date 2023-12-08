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

def getDistance_and_direction(a, b):
    x = a[0]-b[0]
    y = a[1]-b[1]
    
    x_fabs = math.fabs(x)
    y_fabs = math.fabs(y)
    value = ((x_fabs**2)+(y_fabs**2))**(0.5)
    if value != 0:
        x /= value
        y /= value
    else:
        x = 0
        y = 0
    return value, x, y

class Player(Drawable):
    NAME_COLOR = (0, 0, 0)
    
    def __init__(self, surface, camera, name=""):
        super().__init__(surface, camera)
        self.x = random.randint(100, PLATFORM_SIZE-100)
        self.y = random.randint(100, PLATFORM_SIZE-100)
        self.mass = DEFAULT_MASS
        self.speed = 5
        self.color = (230, 255, 0)
        self.outline_color = (255, 255, 255)
        self.name = name
        
    def move(self, mouse):
        
    
        if mouse == True:
            distance, x, y = getDistance_and_direction((0, 0), (
                pygame.mouse.get_pos()[0]-(SCREEN_WIDTH/2), 
                pygame.mouse.get_pos()[1]-(SCREEN_HEIGHT/2)))
            futur_x = self.x - (x * self.speed)
            futur_y = self.y - (y * self.speed)
            if  (futur_x + (self.mass/2)) < PLATFORM_SIZE and \
                    (futur_x - (self.mass/2)) > 0:
                self.x = futur_x
            if (futur_y + (self.mass/2)) < PLATFORM_SIZE and \
                    (futur_y - (self.mass/2)) > 0:
                self.y = futur_y

    def not_yet(self):
        if (self.x != pygame.mouse.get_pos()[0] or self.y != pygame.mouse.get_pos()[1]):
            return True

    def check_if_out(self):
        if  (self.x + (self.mass/2)) >= PLATFORM_SIZE:
            self.x -= (self.x + (self.mass/2)) - PLATFORM_SIZE
        if (self.x - (self.mass/2)) < 0:
            self.x -= (self.x + (self.mass/2))
        if (self.y + (self.mass/2)) >= PLATFORM_SIZE:
            self.y -= (self.y + (self.mass/2)) - PLATFORM_SIZE
        if (self.y - (self.mass/2)) < 0:
            self.y -= (self.y + (self.mass/2))

    def scrounch(self, miams, particles):
        for miam in miams:
            if getDistance((miam.x, miam.y), (self.x, self.y)) <= self.mass/2:
                self.mass += 0.5 / (self.mass/20)
                self.check_if_out()
                miams.remove(miam)
                for i in range(0, NB_PARTICLES):
                    particles.append([[SCREEN_WIDTH/2 , SCREEN_HEIGHT/2], [random.randint(-80, 80) / 10 - 1, random.randint(-80, 80) / 10 - 1], random.randint(6, 11)])
                miams.append(Miam(self.surface, self.camera))

    def canibal_scrounch(self, bots):
        for bot in bots:
            if self.mass < bot.mass:
                bigger = bot.mass
            else:
                bigger = self.mass
            if getDistance((bot.x, bot.y), (self.x, self.y)) <= bigger/2:
                eater = self.mass - bot.mass
                if eater > DIFF_TO_EAT:
                    self.mass += bot.mass*0.5
                    self.check_if_out()
                    bots.remove(bot)
                elif eater < -DIFF_TO_EAT:
                    return False
        return True
    
    def too_big(self):
        if self.mass > 100:
            self.mass -= 0.01 * (self.mass/100)
    
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
        pygame.draw.rect(self.surface, "white", pygame.Rect(10, 10, 90, 30))
        drawText("score : " + str(int(self.mass)), (15, 15))