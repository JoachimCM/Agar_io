import pygame
import random
from pygame.locals import *
from pygame import *
from Food import Food

NB_FOOD = 200
SIZE_OF_FOOD = 10

class App:
    def __init__(self):
        self._running = True
        self.pantry = []
        self.nb_food = NB_FOOD
        self.size = self.weight, self.height = 1840, 980

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill("white")
        self._running = True
        self.draw_all_food()
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        for i in range(self.nb_food, NB_FOOD):
            self.draw_all_food(SIZE_OF_FOOD)
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def draw_food(self, size):
        new_food = Food(size, self.weight, self.height, self.screen)
        self.pantry.append(new_food)

    def draw_all_food(self):
        random.seed(random.random())
        for i in range(0, NB_FOOD):
            self.draw_food(SIZE_OF_FOOD)

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()