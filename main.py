import pygame
from sys import exit

#Initialize pygame library
pygame.init()

# Create a screen (Widht x Height)
screen = pygame.display.set_mode((800,400))
# Name window
pygame.display.set_caption("Game")
# Get clock object
clock = pygame.time.Clock()
# Create font
font = pygame.font.Font("font/pixeltype.ttf", 50)

# Create a surface
sky_surface = pygame.image.load("graphics/sky.png").convert_alpha() # convert into a more efficient file format
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()
text_surface = font.render("My game", False, "Black")

# Characters
pig_surface = pygame.image.load("graphics/pig/pig1.png").convert_alpha()
pig_x_position = 800

player_surface = pygame.image.load("graphics/player/player-run-1.png").convert_alpha()
# creating rectangle
player_rectangle = player_surface.get_rect(midbottom = (80, 275))

# Game loop
while True:
    #get every event anc check user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #display surface on screen
    screen.blit(sky_surface,(0,0)) # 1
    screen.blit(ground_surface,(0, 20)) # 2 ...
    screen.blit(text_surface,(300, 20))

    # display pig in a loop
    pig_x_position -= 4
    if pig_x_position == -120: pig_x_position = 800
    screen.blit(pig_surface,(pig_x_position, 190))

    # player
    screen.blit(player_surface,(player_rectangle))

    #update screen surface
    pygame.display.update()
    # framerate ceiling
    clock.tick(60)
