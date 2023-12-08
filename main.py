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

icone = pygame.image.load ('Agar_io_icone.png')
neutral_background = pygame.image.load ('Agar_io_in_game.png')
banner = pygame.image.load('Agar_io.png')
pygame.display.set_caption("Agar.io")
pygame.display.set_icon(icone)
clock = pygame.time.Clock()


class Game :
    def __init__(self):
        self.is_playing=False
        self.to_be_started=True
        
            
        
def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((150, 0, 0))
    return surf

game = Game() 

running =True


while running:  
     
    clock.tick(50)

    if game.is_playing==False:
        
        playing_song = pygame.mixer_music.load("i-wanna-feel-110039.ogg")
        pygame.mixer_music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        SCREEN.blit(banner,(-30,0))
        pygame.display.flip()
        
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 running= False
                 pygame.quit()
                 sys.exit()
        
             if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_SPACE :
                        if game.to_be_started :
                                game.is_playing=True 
                                print ("Le partie a commencé ! Bonne chance!")
                                pygame.display.flip()
                                game.to_be_started= False
                                pygame.mixer.music.fadeout(0.3)
                                pygame.mixer_music.unload()
                                banner_song = pygame.mixer_music.load("stranger-things-124008.ogg")
                                pygame.mixer_music.play(-1)
                                pygame.mixer.music.set_volume(5)
         
                                camera = Camera()
                                grid = Grid(SCREEN, camera)
                                miams = Miams(SCREEN, camera, NB_FOOD)
                                player = Player(SCREEN, camera, "Oeuf au plat")
                                painter = Painter()

                                player_movement = False
                                event_key = 0
                                particles = []    

                                painter.add(grid)
                                painter.add(miams)
                                painter.add(player)
                                
                                
                                
                        else:
                                print ("Ne quittez pas,une partie va recommencer !")
            
                    
        
        
        
    
    else :

    
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 running= False
                 pygame.quit()
                 sys.exit()
        
             if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_SPACE :
                        if game.is_playing==False and game.to_be_started :
                                game.is_playing=True 
                                print ("Le partie a commencé ! Bonne chance!")
                                pygame.display.flip()
                        else:
                                print ("Ne quittez pas,une partie va recommencer !")
            
                    else:
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

