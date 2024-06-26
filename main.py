import pygame
import sys
import random

# Text Variables
player_score = 0
opponent_score = 0


def ball_animation():
    global ball_speed_x, ball_speed_y
    global opponent_score, player_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        if ball.left <= 0:
            pygame.mixer.Sound.play(score_sound)
            player_score += 1
        else:
            pygame.mixer.Sound.play(score_sound)
            opponent_score += 1
        ball_restart()

    if ball.colliderect(player) and ball_speed_x > 0:
        ball_speed_x *= -1
    if ball.colliderect(opponent) and ball_speed_x < 0:
        ball_speed_x *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    if opponent.top <= ball.y:
        opponent.top += opponent_speed
    if opponent.bottom >= ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Colors
bg_color = pygame.Color("gray8")
player_color = pygame.Color("beige")
ball_color = pygame.Color("darkseagreen4")

# Game Define Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Game Variables
ball_speed_x = 8 * random.choice((1, -1))
ball_speed_y = 8 * random.choice((1, -1))
player_speed = 0
opponent_speed = 8

game_font = pygame.font.Font("freesansbold.ttf", 48)

# Sound
score_sound = pygame.mixer.Sound("score.ogg")
ambient_sound = pygame.mixer.Sound("ambient.ogg")
pygame.mixer.Sound.play(ambient_sound, loops=-1)

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 8
            if event.key == pygame.K_UP:
                player_speed -= 8
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 8
            if event.key == pygame.K_UP:
                player_speed += 8

    ball_animation()
    player_animation()
    opponent_animation()

    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, player_color, player)
    pygame.draw.rect(screen, player_color, opponent)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(
        screen, ball_color, (screen_width / 2, 0), (screen_width / 2, screen_height)
    )

    player_text = game_font.render(f"{player_score}", False, "beige")
    screen.blit(player_text, (880, 60))

    opponent_text = game_font.render(f"{opponent_score}", False, "beige")
    screen.blit(opponent_text, (320, 60))

    # Updating the window
    pygame.display.flip()
    clock.tick(60)
