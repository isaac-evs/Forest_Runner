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
        self.player_jump_index = 0

        player_hurt_1 = pygame.image.load("graphics/player/player-hurt-1.png").convert_alpha()
        player_hurt_2 = pygame.image.load("graphics/player/player-hurt-2.png").convert_alpha()
        self.player_hurt = [player_hurt_1, player_hurt_2]
        self.player_hurt_index = 0

        self.is_hurt = False

        self.image = self.player_run[self.player_run_index]
        self.rect = self.image.get_rect(midbottom =(150, 290))

        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/audio_jump.mp3")
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if death_animation_executed == False:
            if keys[pygame.K_SPACE] and self.rect.bottom >= 290:
                self.gravity = -20
                self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 290:
            self.rect.bottom = 290

    def animation_state(self):
        if self.is_hurt:
            self.player_hurt_index += 0.2
            if self.player_hurt_index >= len(self.player_hurt):
                self.player_hurt_index = 0
            self.image = self.player_hurt[int(self.player_hurt_index)]
        elif self.rect.bottom < 290:
            self.player_jump_index += 0.05
            if self.player_jump_index >= len(self.player_jump):
                self.player_jump_index = 0
            self.image = self.player_jump[int(self.player_jump_index)]
        else:
            self.player_run_index += 0.2
            if self.player_run_index >= len(self.player_run):
                self.player_run_index = 0
            self.image = self.player_run[int(self.player_run_index)]
            self.player_jump_index = 0

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

    def destroy(self):
        if self.rect.x <= -100: self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()


def display_score():
    time = int(pygame.time.get_ticks() / 1000) - int(start_time / 1000)
    score_surface = font.render(f"Score: {time}", False, "White")
    score_rectangle = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rectangle)
    return time

def collisions():
    collide_callable = pygame.sprite.collide_rect_ratio(0.5)

    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False, collided=collide_callable):
        player.sprite.is_hurt = True
        hurt_time = pygame.time.get_ticks()
        return False
    else:
        player.sprite.is_hurt = False
        return True

def time_since_hurt():
    if hurt_time == 0:
        return 0
    else:
        return pygame.time.get_ticks() - hurt_time

pygame.init()

screen = pygame.display.set_mode((800,400))

pygame.display.set_caption("Game")

clock = pygame.time.Clock()

font = pygame.font.Font("font/pixeltype.ttf", 50)

game_active = False

start_time = 0
score = 0

hurt_time = 0

death_animation_executed = False


bg_music = pygame.mixer.Sound("audio/music.mp3")
bg_music.play(loops = -1)
bg_music.set_volume(0.2)

#Player
player = pygame.sprite.GroupSingle()
player.add(Player())

#Obstacles
obstacle_group = pygame.sprite.Group()

# Surfaces
sky1_surface = pygame.image.load("graphics/sky1.png").convert_alpha()
sky2_surface = pygame.image.load("graphics/sky2.png").convert_alpha()
ground_surface = pygame.image.load("graphics/ground.png").convert_alpha()

# Surface position
sky1_x_pos = 0
sky2_x_pos = 0
ground_x_pos = 0
sky_speed = 1

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
initial_obstacle_interval = 2000
obstacle_interval = initial_obstacle_interval
pygame.time.set_timer(obstacle_timer,obstacle_interval)

# Game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active == True:

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["eagle","mushroom", "mushroom", "mushroom"])))

        else:
            if death_animation_executed == False:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()


    if game_active == True:

        sky1_x_pos -= sky_speed
        sky2_x_pos -= sky_speed * 1.5
        ground_x_pos -= sky_speed * 2.5

        if sky1_x_pos <= -800:
            sky1_x_pos = 0
        if sky2_x_pos <= -800:
            sky2_x_pos = 0
        if ground_x_pos <= -800:
            ground_x_pos = 0

        # Display surfaces
        screen.blit(sky1_surface, (sky1_x_pos, 0))
        screen.blit(sky1_surface, (sky1_x_pos + 800, 0))

        screen.blit(sky2_surface, (sky2_x_pos, -40))
        screen.blit(sky2_surface, (sky2_x_pos + 800, -40))

        screen.blit(ground_surface, (ground_x_pos, 0))
        screen.blit(ground_surface, (ground_x_pos + 800, 0))

        score = display_score()

        if score >= 20 and obstacle_interval > 1500:
            obstacle_interval = 1500
            pygame.time.set_timer(obstacle_timer, obstacle_interval)
        elif score >= 40 and obstacle_interval > 1000:
            obstacle_interval = 1000
            pygame.time.set_timer(obstacle_timer, obstacle_interval)
        elif score >= 60 and obstacle_interval > 800:
            obstacle_interval = 800
            pygame.time.set_timer(obstacle_timer, obstacle_interval)


        player.update()
        player.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        game_active = collisions()

    else:

        pygame.time.set_timer(obstacle_timer, 2000)

        if score == 0:
            screen.fill("#88b07b")
            screen.blit(player_stand, player_stand_rectangle)
            screen.blit(game_title_surface, game_title_rectangle)
            score_message = font.render(f"Your score: {score}", False, "White")
            score_message_rectangle = score_message.get_rect(center = (400, 340))

            if score == 0:
                screen.blit(game_message, game_message_rectangle)
            else:
                screen.blit(score_message, score_message_rectangle)

        if player.sprite.is_hurt:


            screen.blit(sky1_surface, (sky1_x_pos, 0))
            screen.blit(sky1_surface, (sky1_x_pos + 800, 0))

            screen.blit(sky2_surface, (sky2_x_pos, -40))
            screen.blit(sky2_surface, (sky2_x_pos + 800, -40))

            screen.blit(ground_surface, (ground_x_pos, 0))
            screen.blit(ground_surface, (ground_x_pos + 800, 0))

            obstacle_group.update()
            obstacle_group.draw(screen)

            player.update()
            player.draw(screen)

            if death_animation_executed == False:
                player.sprite.gravity = -20
                death_animation_executed = True

            hurt_time += 1

            if hurt_time >= 120:
                hurt_time = 0
                player.sprite.is_hurt = False
                death_animation_executed = False
                obstacle_group.empty()
                screen.fill("#88b07b")
                screen.blit(player_stand, player_stand_rectangle)
                screen.blit(game_title_surface, game_title_rectangle)
                score_message = font.render(f"Your score: {score}", False, "White")
                score_message_rectangle = score_message.get_rect(center = (400, 340))

                if score == 0:
                    screen.blit(game_message, game_message_rectangle)
                else:
                    screen.blit(score_message, score_message_rectangle)

    pygame.display.update()

    # framerate ceiling
    clock.tick(60)
