# http://blog.naver.com/samsjang/220706335386


import pygame
import random
from time import sleep


white = (255, 255, 255)
red = (255, 0, 0)
pad_width = 740
pad_height = 370
pad_size = (pad_width, pad_height)
background_width = 740


def init_game():
    global gamepad, clock, aircraft, background1, background2

    pygame.init()
    gamepad = pygame.display.set_mode(pad_size)
    pygame.display.set_caption("Py Flying")
    aircraft = pygame.image.load('images\plane.png')
    background1 = pygame.image.load('images\\background.png')
    background2 = background1.copy()

    clock = pygame.time.Clock()
    run_game()


def back(background, x, y):
    global gamepad
    gamepad.blit(background, (x, y))


def airplane(x, y):
    global gamepad, aircraft
    gamepad.blit(aircraft, (x, y))


def run_game():
    global gamepad, clock, aircraft, background1, background2

    x = pad_width * 0.05
    y = pad_height * 0.8
    y_change = 0

    background1_x = 0
    background2_x = background_width

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        y += y_change

        gamepad.fill(white)

        background1_x -= 2
        background2_x -= 2

        if background1_x == -background_width:
            background1_x = background_width
        if background2_x == -background_width:
            background2_x = background_width

        back(background1, background1_x, 0)
        back(background2, background2_x, 0)
        airplane(x, y)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()


init_game()


