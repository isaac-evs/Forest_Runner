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
sky_surface = pygame.image.load("graphics/sky.png")
ground_surface = pygame.image.load("graphics/ground.png")
text_surface = font.render("My game", False, "Black")

# Characters
pig_surface = pygame.image.load("graphics/pig/pig1.png")


# Game loop
while True:
    #get every event anc check user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #display surface on screen
    screen.blit(sky_surface,(0,0))
    screen.blit(ground_surface,(0,0))
    screen.blit(text_surface,(300, 50))
    screen.blit(pig_surface,(400, 200))


    #update screen surface
    pygame.display.update()
    # framerate ceiling
    clock.tick(60)
