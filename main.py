import pygame
from sys import exit

# Score function
def display_score():
    time = int(pygame.time.get_ticks() / 1000) - int(start_time / 1000)
    score_surface = font.render(f"Score: {time}", False, "White")
    score_rectangle = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rectangle)
    return time

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
# Game state
game_active = False
start_time = 0
score = 0

# Create a surface
sky1_surface = pygame.image.load("graphics/sky1.png").convert_alpha() # convert into a more efficient file format
sky2_surface = pygame.image.load("graphics/sky2.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()
#score_surface = font.render("Score", False, "gray30")
#score_rectangle = score_surface.get_rect(center = (400, 50) )

# Characters
npc1_surface = pygame.image.load("graphics/mushroom/mushroom1.png").convert_alpha()
npc1_rectangle = npc1_surface.get_rect(midbottom = (800, 290))

# Player
player_surface = pygame.image.load("graphics/player/player-run-1.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (80, 290))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load("graphics/player/player-idle-1.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rectangle = player_stand.get_rect(center = (400,200))

game_title_surface = font.render("Forest Runner", False, "White")
game_title_rectangle = game_title_surface.get_rect(center = (400,60))

game_message = font.render("Press space to run", False, "White")
game_message_rectangle = game_message.get_rect(center = (400,340))

# Game loop
while True:
    # get every event anc check user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active == True:

            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom >= 290:
                if player_rectangle.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 290:
                    player_gravity = -20

        else:

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                npc1_rectangle.left = 800
                start_time = pygame.time.get_ticks()


    if game_active == True:

        # display surface on screen
        screen.blit(sky1_surface,(0,0)) # 1
        screen.blit(sky2_surface,(0,-40)) # 2
        screen.blit(ground_surface,(0, 0)) # 3 ...

        # draw an rectangle
        #pygame.draw.rect(screen, "palegreen3", score_rectangle)
        #screen.blit(score_surface,score_rectangle)
        score = display_score()

        # display npc in a loop
        npc1_rectangle.x -= 5
        if npc1_rectangle.right <= 0: npc1_rectangle.left = 800
        screen.blit(npc1_surface, npc1_rectangle )

        # player
        player_gravity += 1
        player_rectangle.bottom += player_gravity

        # ground collision
        if player_rectangle.bottom >= 290: player_rectangle.bottom = 290
        screen.blit(player_surface,player_rectangle)

        # enemy collision
        if npc1_rectangle.colliderect(player_rectangle):
            game_active = False

    else:
        screen.fill("#88b07b")
        screen.blit(player_stand, player_stand_rectangle)
        screen.blit(game_title_surface, game_title_rectangle)
        score_message = font.render(f"Your score: {score}", False, "White")
        score_message_rectangle = score_message.get_rect(center = (400, 340))

        if score == 0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)

    #update screen surface
    pygame.display.update()

    # framerate ceiling
    clock.tick(60)
