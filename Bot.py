import random, math

from Drawable import *
from config import *
from Player import *

class Bot(Drawable):
    
    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(100, PLATFORM_SIZE-100)
        self.y = random.randint(100, PLATFORM_SIZE-100)
        self.mass = DEFAULT_MASS_BOT
        self.speed = 5
        self.color = (random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255))
        self.outline_color = (random.randint(0, 255),
                                random.randint(0, 255),
                                random.randint(0, 255))

    def move_to_eat(self, miams, bots, player):
        is_traking_player = False
        
        distance_min, x_min, y_min = getDistance_and_direction((miams[0].x, miams[0].y), (self.x, self.y))
        for miam in miams:
            distance, x, y = getDistance_and_direction((miam.x, miam.y), (self.x, self.y))
            if distance < distance_min:
                distance_min = distance
                x_min = x
                y_min = y

        distance_player, x_player, y_player = getDistance_and_direction((player.x, player.y), (self.x, self.y))
        if self.mass > player.mass + DIFF_TO_EAT + 1 and distance_player < distance_min*5:
            distance_min = distance_player
            x_min = x_player
            y_min = y_player
            is_traking_player = True

        for bot in bots:
            distance_bot, x_bot, y_bot = getDistance_and_direction((bot.x, bot.y), (self.x, self.y))
            if  (is_traking_player and \
                    distance_bot < distance_min and \
                    self.mass > bot.mass + DIFF_TO_EAT + 1) \
                or \
                (is_traking_player == False and \
                    distance_bot < distance_min*5 and \
                    self.mass > bot.mass + DIFF_TO_EAT + 1):
                distance_min = distance_bot
                x_min = x_bot
                y_min = y_bot

        futur_x = self.x + (x_min * self.speed)
        futur_y = self.y + (y_min * self.speed)

        if  (futur_x + (self.mass/2)) < PLATFORM_SIZE and \
                (futur_x - (self.mass/2)) > 0:
            self.x = futur_x
        if (futur_y + (self.mass/2)) < PLATFORM_SIZE and \
                (futur_y - (self.mass/2)) > 0:
            self.y = futur_y

    def check_if_out(self):
            if  (self.x + (self.mass/2)) >= PLATFORM_SIZE:
                self.x -= (self.x + (self.mass/2)) - PLATFORM_SIZE
            if (self.x - (self.mass/2)) < 0:
                self.x -= (self.x - (self.mass/2))
            if (self.y + (self.mass/2)) >= PLATFORM_SIZE:
                self.y -= (self.y + (self.mass/2)) - PLATFORM_SIZE
            if (self.y - (self.mass/2)) < 0:
                self.y -= (self.y - (self.mass/2))

    def scrounch(self, miams):
        for miam in miams:
            if getDistance((miam.x, miam.y), (self.x, self.y)) <= self.mass/2:
                self.mass += 0.4 / (self.mass/20)
                self.check_if_out()
                miams.remove(miam)
                miams.append(Miam(self.surface, self.camera))

    def canibalism(self, bots):
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
                    bot.mass += self.mass*0.5
                    self.check_if_out()
                    bots.remove(self)

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