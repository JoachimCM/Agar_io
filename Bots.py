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

    def move_bots(self, miams, player):
        for bot in self.list:
            bot.move_to_eat(miams, self.list, player)

    def scrounchs(self, miams):
        for bot in self.list:
            bot.scrounch(miams)

    def too_bigs(self):
        for bot in self.list:
            bot.too_big()

    def eat_them_all(self):
        for bot in self.list:
            bot.canibalism(self.list)