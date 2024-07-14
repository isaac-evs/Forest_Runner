import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        player_run_1 = pygame.image.load("graphics/player/player-run-1.png").convert_alpha()
        player_run_2 = pygame.image.load("graphics/player/player-run-2.png").convert_alpha()
        player_run_3 = pygame.image.load("graphics/player/player-run-3.png").convert_alpha()
        player_run_4 = pygame.image.load("graphics/player/player-run-4.png").convert_alpha()
        player_run_5 = pygame.image.load("graphics/player/player-run-5.png").convert_alpha()
        player_run_6 = pygame.image.load("graphics/player/player-run-6.png").convert_alpha()
        self.player_run = [player_run_1, player_run_2, player_run_3, player_run_4, player_run_5, player_run_6]
        self.player_run_index = 0

        player_jump_1 = pygame.image.load("graphics/player/player-jump-1.png").convert_alpha()
        player_jump_2 = pygame.image.load("graphics/player/player-jump-2.png").convert_alpha()
        self.player_jump = [player_jump_1, player_jump_2]
        self.jump_frame_count = 0

        self.image = self.player_run[self.player_run_index]
        self.rect = self.image.get_rect(midbottom =(150, 290))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/audio_jump.mp3")
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 290:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 290:
            self.rect.bottom = 290

    def animation_state(self):
        if self.rect.bottom < 290:
            self.jump_frame_count += 1
            if self.jump_frame_count % 60 < 20:
                self.image = self.player_jump[0]
            else:
                self.image = self.player_jump[1]
        else:
            self.player_run_index += 0.2
            if self.player_run_index >= len(self.player_run): self.player_run_index = 0
            self.image = self.player_run[int(self.player_run_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type):
        super().__init__()

        if type == "eagle":
            eagle1 = pygame.image.load("graphics/eagle/eagle-attack-1.png").convert_alpha()
            eagle2 = pygame.image.load("graphics/eagle/eagle-attack-2.png").convert_alpha()
            eagle3 = pygame.image.load("graphics/eagle/eagle-attack-3.png").convert_alpha()
            eagle4 = pygame.image.load("graphics/eagle/eagle-attack-4.png").convert_alpha()
            self.frames = [eagle1, eagle2, eagle3, eagle4]
            y_pos = randint(150,190)
        else:
            mushroom1 = pygame.image.load("graphics/mushroom/mushroom1.png").convert_alpha()
            mushroom2 = pygame.image.load("graphics/mushroom/mushroom2.png").convert_alpha()
            mushroom3 = pygame.image.load("graphics/mushroom/mushroom3.png").convert_alpha()
            mushroom4 = pygame.image.load("graphics/mushroom/mushroom4.png").convert_alpha()
            mushroom5 = pygame.image.load("graphics/mushroom/mushroom5.png").convert_alpha()
            mushroom6 = pygame.image.load("graphics/mushroom/mushroom6.png").convert_alpha()
            mushroom7 = pygame.image.load("graphics/mushroom/mushroom7.png").convert_alpha()
            mushroom8 = pygame.image.load("graphics/mushroom/mushroom8.png").convert_alpha()
            mushroom9 = pygame.image.load("graphics/mushroom/mushroom9.png").convert_alpha()
            self.frames = [mushroom1, mushroom2, mushroom3, mushroom4, mushroom5, mushroom6, mushroom7, mushroom8, mushroom9]
            y_pos = 293

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.2
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


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

            if obstacle_rect.bottom == 293: screen.blit(npc1_surface, obstacle_rect)
            else: screen.blit(npc2_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

# obstacle collsions
def collisions():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


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
# Music
bg_music = pygame.mixer.Sound("audio/music.mp3")
bg_music.play(loops = -1)
bg_music.set_volume(0.2)

#Player
player = pygame.sprite.GroupSingle()
player.add(Player())

#Obstacles
obstacle_group = pygame.sprite.Group()


# Create a surface
sky1_surface = pygame.image.load("graphics/sky1.png").convert_alpha() # convert into a more efficient file format
sky2_surface = pygame.image.load("graphics/sky2.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

# Mushroom
npc1_frame1 = pygame.image.load("graphics/mushroom/mushroom1.png").convert_alpha()
npc1_frame2 = pygame.image.load("graphics/mushroom/mushroom2.png").convert_alpha()
npc1_frame3 = pygame.image.load("graphics/mushroom/mushroom3.png").convert_alpha()
npc1_frame4 = pygame.image.load("graphics/mushroom/mushroom4.png").convert_alpha()
npc1_frame5 = pygame.image.load("graphics/mushroom/mushroom5.png").convert_alpha()
npc1_frame6 = pygame.image.load("graphics/mushroom/mushroom6.png").convert_alpha()
npc1_frame7 = pygame.image.load("graphics/mushroom/mushroom7.png").convert_alpha()
npc1_frame8 = pygame.image.load("graphics/mushroom/mushroom8.png").convert_alpha()
npc1_frame9 = pygame.image.load("graphics/mushroom/mushroom9.png").convert_alpha()

npc1_frames = [npc1_frame1, npc1_frame2, npc1_frame3, npc1_frame4, npc1_frame5, npc1_frame6, npc1_frame7, npc1_frame8, npc1_frame9]
npc1_frame_index = 0

npc1_surface = npc1_frames[npc1_frame_index]

# Eagle
npc2_frame1 = pygame.image.load("graphics/eagle/eagle-attack-1.png").convert_alpha()
npc2_frame2 = pygame.image.load("graphics/eagle/eagle-attack-2.png").convert_alpha()
npc2_frame3 = pygame.image.load("graphics/eagle/eagle-attack-3.png").convert_alpha()
npc2_frame4 = pygame.image.load("graphics/eagle/eagle-attack-4.png").convert_alpha()

npc2_frames = [npc2_frame1, npc2_frame2, npc2_frame3, npc2_frame4]
npc2_frame_index = 0

npc2_surface = npc2_frames[npc2_frame_index]

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
player_gravity = 0

# Intro screen
player_stand = pygame.image.load("graphics/player/player-idle-1.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 1)
player_stand_rectangle = player_stand.get_rect(center = (400,200))

game_title_surface = font.render("Forest Runner", False, "White")
game_title_rectangle = game_title_surface.get_rect(center = (400,60))

game_message = font.render("Press space to run", False, "White")
game_message_rectangle = game_message.get_rect(center = (400,340))

# obstacle timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# mushroom timer
npc1_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(npc1_animation_timer, 100)

# eagle timer
npc2_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(npc2_animation_timer, 100)

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
                obstacle_group.add(Obstacle(choice(["eagle","mushroom", "mushroom", "mushroom"])))
                #if randint(0,2):
                #    obstacle_rectangle_list.append(npc1_surface.get_rect(midbottom = (randint(900,1100), 293)))
                #else:
                #    obstacle_rectangle_list.append(npc2_surface.get_rect(midbottom = (randint(900,1100), randint(150, 190))))

            if event.type == npc1_animation_timer:
                npc1_frame_index += 1
                if npc1_frame_index >= len(npc1_frames): npc1_frame_index = 0
                npc1_surface = npc1_frames[int(npc1_frame_index)]

            if event.type == npc2_animation_timer:
                npc2_frame_index += 1
                if npc2_frame_index >= len(npc2_frames): npc2_frame_index = 0
                npc2_surface = npc2_frames[int(npc2_frame_index)]


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

        # player
        #player_gravity += 1
        #player_rectangle.bottom += player_gravity
        #if player_rectangle.bottom >= 290: player_rectangle.bottom = 290
        #player_animation()
        #screen.blit(player_surface,player_rectangle)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()


        #obstacle movement
        #obstacle_rectangle_list = obstacle_movement(obstacle_rectangle_list)

        # collision
        game_active = collisions()
        #game_active = collisions(player_rectangle, obstacle_rectangle_list)

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
