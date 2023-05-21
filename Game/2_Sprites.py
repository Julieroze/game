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
char = pygame.image.load(os.path.join(image_path, "P_character.png"))
char_size = char.get_rect().size
char_w = char_size[0]
char_h = char_size[1]
char_x = screen_width/2 - char_w/2
char_y = screen_height/2 - char_h/2

char_to_x = 0
char_to_y = 0

char_speed = 0.6





running= True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0,0))
    screen.blit(char, (char_x,char_y))
    pygame.display.update()


pygame.quit