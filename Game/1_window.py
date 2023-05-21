import pygame
import os
import random 

pygame.init()

screen_width = 480 
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

game_path = os.path.dirname(__file__)
image_path = os.path.join(game_path, "images")

background = pygame.image.load(os.path.join(image_path, "background.png"))

# Character


running= True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0,0))
    pygame.display.update()


pygame.quit