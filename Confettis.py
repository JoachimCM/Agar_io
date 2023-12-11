import pygame
import random
from config import*
pygame.init()



clock = pygame.time.Clock()

group = []
class Confettis(pygame.sprite.Sprite):
    "Creates confettis starting from pos with a color"

    def __init__(self, pos, color, turn="off"):
        super(Confettis, self).__init__()
        self.confettis_list = []
        self.pos = pos
        self.color = color
        group.append(self)
        self.turn = turn # this makes the effect visible

    

    def generate_confettis(self):
        self.pos[0] = random.randint(0, SCREEN_WIDTH)

        # setting the data for each confetti
        origin = [self.pos[0], self.pos[1]] # Starting here each confetti
        y_dir = 2
        x_dir = random.randint(0, 20) / 10 - 1
        dirs = [x_dir, y_dir] # movement
        radius = random.randint(4,6) # radius
        # Appending data to the list
        self.confettis_list.append([origin, dirs, radius])
        self.generate_movements()

    def generate_movements(self):
        
        # Moving the coordinates and size of self.confettis_list
        for confetti in self.confettis_list[:]:
            confetti[0][0] += confetti[1][0] # x pos += x_dir
            confetti[0][1] += confetti[1][1] # y pos += y_dir
            confetti[2] -= 0.05 # how fast circles shrinks
            confetti[1][1] += 0.01 # circles speed
            # if confetti[2] <= 0:
            if confetti[2] <= 0:
                self.confettis_list.remove(confetti)
            # do not call draw from here: it slows down the frame rate
            # self.draw()
    
    def draw(self, SCREEN2):
        "Draws confettis based on data in the self.confettis_list"
        if self.turn == "on":
            for confetti in self.confettis_list:
                 pygame.draw.circle(
                    SCREEN2, (self.color),
                (round(confetti[0][0]), round(confetti[0][1])),
                 round(confetti[2]))


def generate(SCREEN2):
    for par in group:
        par.generate_confettis()
        par.draw(SCREEN2)



# Creating the list with confettis ready to be drawn

Confettis([0, 0], color="white")
Confettis([0, 0], color="yellow")
Confettis([0, 0], color="red")
Confettis([0, 0], color="blue")


