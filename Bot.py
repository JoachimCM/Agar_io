import random, math

from Drawable import *
from config import *
from Player import *

def getDistance_and_direction(a, b):
    x = a[0]-b[0]
    y = a[1]-b[1]
    
    x_fabs = math.fabs(x)
    y_fabs = math.fabs(y)
    value = ((x_fabs**2)+(y_fabs**2))**(0.5)
    x /= value
    y /= value
    return value, x, y

class Bot(Drawable):
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.mass = DEFAULT_MASS
        self.speed = 5
        self.color = (random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255))
        self.outline_color = (random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255))

    def move_to_eat(self, miams):
        distance_min, x_min, y_min = getDistance_and_direction((miams[0].x, miams[0].y), (self.x, self.y))
        for miam in miams:
            distance, x, y = getDistance_and_direction((miam.x, miam.y), (self.x, self.y))
            if distance < distance_min:
                distance_min = distance
                x_min = x
                y_min = y
        self.x += x_min * self.speed
        self.y += y_min * self.speed

    def scrounch(self, miams):
        for miam in miams:
            if getDistance((miam.x, miam.y), (self.x, self.y)) <= self.mass/2:
                self.mass += 0.4 / (self.mass/20)
                miams.remove(miam)
                # for i in range(0, NB_PARTICLES):
                #     particles.append([[SCREEN_WIDTH/2 , SCREEN_HEIGHT/2], [random.randint(-80, 80) / 10 - 1, random.randint(-80, 80) / 10 - 1], random.randint(6, 11)])
                miams.append(Miam(self.surface, self.camera))

    def canibalism(self, bots):
        for bot in bots:
            if getDistance((bot.x, bot.y), (self.x, self.y)) <= self.mass/2:
                eater = self.mass - bot.mass
                if eater > 1:
                    bots.remove(bot)

    def too_big(self):
        if self.mass > 100:
            self.mass -= 0.01 * (self.mass/100)

    def draw(self):
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))
        pygame.draw.circle(self.surface, self.outline_color, center,
                           int((self.mass / 2 + 3) * zoom))
        pygame.draw.circle(self.surface, self.color, center,
                           int(self.mass / 2 * zoom))