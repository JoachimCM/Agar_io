# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:37:45 2023

"""
import pygame, sys, random, math
from config import *
from Drawable import *
from Grid import *
from Player import *
from Miam import *
from Miams import *
from Camera import * 
from Painter import *

pygame.init()

pygame.display.set_caption("Agar.io")
clock = pygame.time.Clock()

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((150, 0, 0))
    return surf

camera = Camera()
grid = Grid(SCREEN, camera)
miams = Miams(SCREEN, camera, NB_FOOD)
player = Player(SCREEN, camera, "Oeuf au plat")

painter = Painter()
painter.add(grid)
painter.add(miams)
painter.add(player)

player_movement = False
event_key = 0

particles = []

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
        player.move(event.key)

    player.scrounch(miams.list, particles)
    camera.update(player)
    SCREEN.fill((0,0,0))
    painter.paint()
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.15
        pygame.draw.circle(SCREEN, (200, 0, 0), [int(particle[0][0]), 
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

