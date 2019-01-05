import pygame
from pygame import Rect
from pygame.locals import *
import random

pygame.init()
fpsClock = pygame.time.Clock()

width = 1024
height = 768

screen = pygame.display.set_mode((width, height), FULLSCREEN)
pygame.display.set_caption('Atari Pong')

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

# sound
playerSound = pygame.mixer.Sound('res/player.wav')
sideSound = pygame.mixer.Sound('res/side.wav')
failSound = pygame.mixer.Sound('res/fail.wav')

# font
font = pygame.font.Font('res/bit5x3.ttf', 180)  # needs to be taller

# game variable
playerPaddle = Rect((60, height/2-20), (8, 70))
aiPaddle = Rect((width - 60, height/2-20), (8, 70))
ball = Rect((width/2+30, height/2), (15, 15))

maxSpeed = 10

player_a = 3
player_speed = 0

ai_v = 3
ai_speed = 0

playerScore = 0
aiScore = 0

speeds_y = [-6, -5, -4, 4, 5, 6]
ball_speed_y = speeds_y[random.randint(0, 5)]
speeds_x = [-6, 6]
ball_speed_x = speeds_x[random.randint(0, 1)]

# allows for holding of key
pygame.key.set_repeat(1, 0)

# this is the game loop
while True:

    isPressed = False

    # player input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.QUIT()
            sys.exit()

        if event.type == KEYDOWN:
            # ESC key QUIT
            if event.key == K_ESCAPE:
                pygame.QUIT()
                sys.exit()
            # F key toggle Full Screen
            if event.key == K_f:
                pygame.display.toggle_fullscreen()
            # press key
            if event.key == K_UP:
                isPressed = True
                if player_speed > -maxSpeed:
                    player_speed -= player_a

            if event.key == K_DOWN:
                isPressed = True
                if player_speed < maxSpeed:
                    player_speed += player_a

        if event.type == MOUSEBUTTONDOWN:
            # press key
            if event.button == 4:
                isPressed = True
                if player_speed > -maxSpeed:
                    player_speed -= player_a*3

            if event.button == 5:
                isPressed = True
                if player_speed < maxSpeed:
                    player_speed += player_a*3

    if not isPressed:
        if player_speed > 0:
            player_speed -= player_a
        elif player_speed < 0:
            player_speed += player_a

    # pure-AI input
    # if ball.x > width/2:
    if ball.y > aiPaddle.centery:
        if ai_speed < maxSpeed:
            ai_speed += player_a
    elif ball.y < aiPaddle.centery:
        if ai_speed > -maxSpeed:
            ai_speed -= player_a
    else:
        if ai_speed > 0:
            ai_speed -= player_a
        elif ai_speed < 0:
            ai_speed += player_a

    # update
    playerPaddle.move_ip(0, player_speed)
    aiPaddle.move_ip(0, ai_speed)
    ball.move_ip(ball_speed_x, ball_speed_y)

    # collisions
    if playerPaddle.y < 0:
        playerPaddle.y = 0
        player_speed = 0

    elif playerPaddle.bottom > height:
        playerPaddle.bottom = height
        player_speed = 0

    if aiPaddle.y < 0:
        aiPaddle.y = 0
        ai_speed = 0

    elif aiPaddle.bottom > height:
        aiPaddle.bottom = height
        ai_speed = 0

    if playerPaddle.colliderect(ball):
        playerSound.play()
        ball_speed_x = -ball_speed_x
        if player_speed == 0:
            ball_speed_y = ball_speed_y/abs(ball_speed_y)
        else:
            ball_speed_y = player_speed

        ball.left = playerPaddle.right + 1

    elif aiPaddle.colliderect(ball):
        playerSound.play()
        ball_speed_x = -ball_speed_x

        # prevent
        if ai_speed == 0:
            ball_speed_y = ball_speed_y/abs(ball_speed_y)
        else:
            ball_speed_y = ai_speed

        ball.right = aiPaddle.x - 1

    if ball.y <= 0:
        sideSound.play()
        ball.y = 0
        ball_speed_y = -ball_speed_y

    elif ball.y+10 >= height:
        sideSound.play()
        ball.y = height-10
        ball_speed_y = -ball_speed_y

    if ball.x < 0 or ball.x > width:
        timePassed = 0.0
        failSound.play()
        if ball.x < 0:
            aiScore += 1
        else:
            playerScore += 1
        ball_speed_x = speeds_x[random.randint(0, 1)]
        ball_speed_y = speeds_y[random.randint(0, 5)]
        ball.x = width/2
        ball.y = height/2

    # draw
    screen.fill(black)
    pygame.draw.rect(screen, white, playerPaddle)
    pygame.draw.rect(screen, white, aiPaddle)
    pygame.draw.rect(screen, white, ball)
    playerF = font.render(str(playerScore), True, white)
    aiF = font.render(str(aiScore), True, white)
    screen.blit(playerF, (width/4, 25))
    screen.blit(aiF, (3*width/4, 25))

    for i in range(20):  # centerline
        pygame.draw.line(screen, white, (width/2, i*40),
                         (width/2, i*40+20), 5)

    for n in range(0, height, 4):  # scanlines
        pygame.draw.line(screen, (10, 10, 10), (0, n), (width, n), 1)

    pygame.display.update()
    fpsClock.tick(50)
