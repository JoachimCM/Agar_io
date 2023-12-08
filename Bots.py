from Drawable import *
from Bot import *

class Bots(Drawable):
    
    def __init__(self, surface, camera, nb_bots):
        super().__init__(surface, camera)
        self.nb_bots = nb_bots
        self.list = []
        for i in range(self.nb_bots):
            self.list.append(Bot(self.surface, self.camera))
            
    def draw(self):
        for bot in self.list: 
            bot.draw()

    def move_bots(self, miams):
        for bot in self.list:
            bot.move_to_eat(miams)

    def scrounchs(self, miams, particles):
        for bot in self.list:
            bot.scrounch(miams, particles)

    def too_bigs(self):
        for bot in self.list:
            bot.too_big()