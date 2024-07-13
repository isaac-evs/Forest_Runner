import pygame
from sys import exit
from random import randint

# Score function
def display_score():
    time = int(pygame.time.get_ticks() / 1000) - int(start_time / 1000)
    score_surface = font.render(f"Score: {time}", False, "White")
    score_rectangle = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rectangle)
    return time

# Obstacle movement function
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 290: screen.blit(npc1_surface, obstacle_rect)
            else: screen.blit(npc2_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

# obstacle collsions
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

# player animation
def player_animation():
    global player_surface, player_run_index, player_jump_index, jump_frame_count

    if player_rectangle.bottom < 290:
        jump_frame_count += 1
        if jump_frame_count % 60 < 20:
            player_surface = player_jump[0]
        else:
            player_surface = player_jump[1]

    else:
        player_run_index += 0.2
        if player_run_index >= len(player_run): player_run_index = 0
        player_surface = player_run[int(player_run_index)]
        jump_frame_count = 0

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
# Time and score
start_time = 0
score = 0

# Create a surface
sky1_surface = pygame.image.load("graphics/sky1.png").convert_alpha() # convert into a more efficient file format
sky2_surface = pygame.image.load("graphics/sky2.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

# Obstacles
npc1_surface = pygame.image.load("graphics/mushroom/mushroom1.png").convert_alpha()
npc2_surface = pygame.image.load("graphics/eagle/eagle-attack-1.png").convert_alpha()


obstacle_rectangle_list = []


# Player
player_run_1 = pygame.image.load("graphics/player/player-run-1.png").convert_alpha()
player_run_2 = pygame.image.load("graphics/player/player-run-2.png").convert_alpha()
player_run_3 = pygame.image.load("graphics/player/player-run-3.png").convert_alpha()
player_run_4 = pygame.image.load("graphics/player/player-run-4.png").convert_alpha()
player_run_5 = pygame.image.load("graphics/player/player-run-5.png").convert_alpha()
player_run_6 = pygame.image.load("graphics/player/player-run-6.png").convert_alpha()

player_run = [player_run_1, player_run_2, player_run_3, player_run_4, player_run_5, player_run_6]
player_run_index = 0

player_jump_1 = pygame.image.load("graphics/player/player-jump-1.png").convert_alpha()
player_jump_2 = pygame.image.load("graphics/player/player-jump-2.png").convert_alpha()

player_jump = [player_jump_1, player_jump_2]
player_jump_index = 0
jump_frame_count = 0


player_surface = player_run[player_run_index]


player_rectangle = player_surface.get_rect(midbottom = (150, 290))
player_collision_rectangle = player_rectangle.inflate(-40, -30)


player_gravity = 0

# Intro screen
player_stand = pygame.image.load("graphics/player/player-idle-1.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rectangle = player_stand.get_rect(center = (400,200))

game_title_surface = font.render("Forest Runner", False, "White")
game_title_rectangle = game_title_surface.get_rect(center = (400,60))

game_message = font.render("Press space to run", False, "White")
game_message_rectangle = game_message.get_rect(center = (400,340))

# Costum user event
obstacle_timer = pygame.USEREVENT + 1
# timer
pygame.time.set_timer(obstacle_timer,1500)

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

            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rectangle_list.append(npc1_surface.get_rect(midbottom = (randint(900,1100), 290)))
                else:
                    obstacle_rectangle_list.append(npc2_surface.get_rect(midbottom = (randint(900,1100), randint(150, 190))))
        else:

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()


    if game_active == True:

        # display surface on screen
        screen.blit(sky1_surface,(0,0)) # 1
        screen.blit(sky2_surface,(0,-40)) # 2
        screen.blit(ground_surface,(0, 0)) # 3 ...
        score = display_score()

        # display npc in a loop
        #npc1_rectangle.x -= 5
        #if npc1_rectangle.right <= 0: npc1_rectangle.left = 800
        #screen.blit(npc1_surface, npc1_rectangle)
        #npc1_collision_rectangle.center = npc1_rectangle.center
        #pygame.draw.rect(screen, (255, 0, 0), npc1_collision_rectangle, 2)

        # player
        player_gravity += 1
        player_rectangle.bottom += player_gravity
        if player_rectangle.bottom >= 290: player_rectangle.bottom = 290
        player_animation()
        screen.blit(player_surface,player_rectangle)


        #obstacle movement
        obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        # enemy collision
        game_active = collisions(player_rectangle, obstacle_rectangle_list)

    else:
        screen.fill("#88b07b")
        screen.blit(player_stand, player_stand_rectangle)
        screen.blit(game_title_surface, game_title_rectangle)
        score_message = font.render(f"Your score: {score}", False, "White")
        score_message_rectangle = score_message.get_rect(center = (400, 340))

        obstacle_rectangle_list.clear()
        player_rectangle.midbottom = (80, 290)
        player_gravity = 0

        if score == 0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)

    #update screen surface
    pygame.display.update()

    # framerate ceiling
    clock.tick(60)
