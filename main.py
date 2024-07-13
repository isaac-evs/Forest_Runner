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
sky1_surface = pygame.image.load("graphics/sky1.png").convert_alpha() # convert into a more efficient file format
sky2_surface = pygame.image.load("graphics/sky2.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()
score_surface = font.render("Score", False, "White")
score_rectangle = score_surface.get_rect(center = (400, 50) )

# Characters
npc1_surface = pygame.image.load("graphics/mushroom/mushroom1.png").convert_alpha()
npc1_rectangle = npc1_surface.get_rect(midbottom = (800, 290))

player_surface = pygame.image.load("graphics/player/player-run-1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (80, 290))


# Game loop
while True:
    # get every event anc check user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if mouse collides with player rectangle print collision
        if event.type == pygame.MOUSEMOTION:
            if player_rectangle.collidepoint(event.pos): print("collision")

    # display surface on screen
    screen.blit(sky1_surface,(0,0)) # 1
    screen.blit(sky2_surface,(0,-40)) # 2
    screen.blit(ground_surface,(0, 0)) # 3 ...
    # draw an rectangle
    pygame.draw.rect(screen, "cadetblue2", score_rectangle)
    screen.blit(score_surface,score_rectangle)

    # display pig in a loop
    npc1_rectangle.x -= 4
    if npc1_rectangle.right <= 0: npc1_rectangle.left = 800
    screen.blit(npc1_surface, npc1_rectangle )

    # player
    screen.blit(player_surface,player_rectangle)
    # Check collition

    #if player_rectangle.colliderect(npc1_rectangle):
    #    print("collision")


    #update screen surface
    pygame.display.update()
    # framerate ceiling
    clock.tick(60)
