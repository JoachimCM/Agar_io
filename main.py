# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:37:45 2023

"""
import pygame, sys, random
from config import *
from Drawable import *
from Grid import *
from Player import *
from Miam import *
from Miams import *
from Camera import * 
from Painter import *
from Bots import *

pygame.init()

random.seed(SEED)

icone = pygame.image.load ('Agar_io_icone.png')
banner = pygame.image.load('Agar_io.png')
win_banner = pygame.image.load('Agar_io_win.png')
lose_banner = pygame.image.load('Agar_io_lose.png')
pygame.display.set_caption("Agar.io")
pygame.display.set_icon(icone)
clock = pygame.time.Clock()


class Game :
    def __init__(self):
        self.is_playing=False
        self.to_be_started=True
        self.is_ending = False
        
    def start(self):
        playing_song = pygame.mixer_music.load("i-wanna-feel-110039.ogg")
        pygame.mixer_music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        SCREEN.blit(banner,(-30,0))
        pygame.display.flip()
        
        while self.is_playing==False:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running= False
                    pygame.quit()
                    sys.exit()
            
                if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_SPACE :
                        self.is_playing=True 
                        print ("Le partie a commencé ! Bonne chance!")
                        pygame.display.flip()
                        pygame.mixer.music.fadeout(3)
                        pygame.mixer_music.unload()
                        banner_song = pygame.mixer_music.load("stranger-things-124008.ogg")
                        pygame.mixer_music.play(-1)
                        pygame.mixer.music.set_volume(0.3)

    def end_win(self):
        playing_song = pygame.mixer_music.load("GODS.ogg")
        pygame.mixer_music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        SCREEN.blit(win_banner,(0,0))
        pygame.display.flip()
        
        while self.is_ending==False:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_ending = True
                    pygame.quit()
                    sys.exit()
            
                if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_SPACE :
                        self.is_ending = True
                        print ("C'est fini !")

    def end_lose(self):
        playing_song = pygame.mixer_music.load("lose_music.ogg")
        pygame.mixer_music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        SCREEN.blit(lose_banner,(0,0))
        pygame.display.flip()
        
        while self.is_ending==False:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_ending = True
                    pygame.quit()
                    sys.exit()
            
                if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_SPACE :
                        self.is_ending = True 
                        print ("C'est fini !")

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((150, 0, 0))
    return surf

game = Game() 
game.start()

camera = Camera()
grid = Grid(SCREEN, camera)
miams = Miams(SCREEN, camera, NB_FOOD)
player = Player(SCREEN, camera, "Oeuf au plat")
bots = Bots(SCREEN, camera, NB_BOTS)
painter = Painter()

player_movement = False
event_key = 0
particles = []

painter.add(grid)
painter.add(miams)
painter.add(player)
painter.add(bots)

pygame.display.flip()

running =True

while running:
    clock.tick(50)
    current_event=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEMOTION:
            player_movement = True
            current_event=pygame.MOUSEMOTION


    player.move(current_event==pygame.MOUSEMOTION or player.not_yet())
    current_event= 0

    player.scrounch(miams.list, particles)
    player.too_big()
    if player.canibal_scrounch(bots.list) == False:
        game.end_lose()
        break
    if len(bots.list) == 0:
        game.end_win()
        break
    bots.move_bots(miams.list, player)
    bots.scrounchs(miams.list)
    bots.eat_them_all()
    bots.too_bigs()
    camera.update(player)
    SCREEN.fill((0,0,0))
    painter.paint()
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.15
        pygame.draw.circle(SCREEN, (random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255)),
                                    [int(particle[0][0]), 
                                        int(particle[0][1])], 
                            int(particle[2]))

        radius = particle[2] * 2
        SCREEN.blit(circle_surf(radius, (20, 20, 60)), 
                        (int(particle[0][0] - radius), 
                        int(particle[0][1] - radius)), 
                        special_flags=pygame.BLEND_RGB_ADD)

        if particle[2] <= 0:
            particles.remove(particle)

    pygame.display.flip()
    pygame.display.update()

