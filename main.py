import pygame
import self as self
from Screen_Settings import *
from sys import exit
import random

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))


class FlappyBird(pygame.sprite.Sprite):
    def __init__(self):  # this initiates the sprite class so that we can access things in the class
        super().__init__()  # this basically accesses inherited methods that have been overridden in a class
        #  without this, the class would be useless because we wouldn't be able to access anything in it
        self.image = pygame.image.load('flappy_bird.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(350, 520))
        self.flappybird_gravity = 0

    def flappybird_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.flappybird_gravity = -20

    def gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity()
        if self.rect.bottom >= 520:
            self.rect.bottom = 520

    def update_game(self):
        self.flappybird_input()
        self.gravity()


flappybird = pygame.sprite.GroupSingle()
flappybird.add(FlappyBird())


class Tubes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.high_tube = pygame.image.load('ceiling_tube.png').convert_alpha()
        self.high_tube_rect = self.image.get_rect(midbottom=(350, 520))
        self.low_tube = pygame.image.load('floor_tube.png').convert_alpha()
        self.low_tube_rect = self.image.get_rect(midbottom=(350, 300))

    tubes_list = [self.high_tube_rect, self.low_tube_rect]


    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def score_func():
    scores = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = Fonts.render('Score: ' + str(scores), False, (250, 250, 250))
    score_rect = score_surface.get_rect(center=(100, 50))
    screen.blit(score_surface, score_rect)
    return scores


def collision_sprite():
    if pygame.sprite.spritecollide(flappybird.sprite, tubes_group, False):
        tubes_group.empty()
        return False
    else:
        return True


# Screen and display

Font = pygame.font.Font(None, 100)
Fonts = pygame.font.Font(None, 75)
pygame.display.set_caption('Flappy Bird')
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
game_active = False
start_time = 0
score_score = 0

# Title
text_surface = Font.render('Flappy Bird', False, (250, 250, 250))
text_rect = text_surface.get_rect(center=(250, 50))

# Groups
flappybird = pygame.sprite.GroupSingle()
flappybird.add(FlappyBird())
tubes_group = pygame.sprite.Group()

# Ground
ground = pygame.image.load('ground.png').convert_alpha()

# Sky
sky = pygame.image.load('sky.jpg').convert_alpha()

# Intro Screen
flappy_smash = pygame.image.load("smash_bird.gif").convert_alpha()
flappy_smash = pygame.transform.scale(flappy_smash, (1040, 720))
flappy_smash_rect = flappy_smash.get_rect(center=(250, 350))
start_screen = Font.render('PRESS SPACE TO START', False, (250, 250, 250))
start_screen_rect = start_screen.get_rect(center=(250, 350))

# Timers
tube_timer = pygame.USEREVENT + 1
pygame.time.set_timer(tube_timer, 1000)  # This gets the timer to set at different intervals

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == tube_timer:
                tubes_group.add(Tubes.(random.choice(tubes_list)))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))

        flappybird.draw(screen)
        flappybird.update()

        tubes_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(flappy_smash, flappy_smash_rect)
        score = score_func()
        score_message = Fonts.render(str("Your score: " + str(score)), False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(start_screen, start_screen_rect)

        if score == 0:
            screen.blit(text_surface, text_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
