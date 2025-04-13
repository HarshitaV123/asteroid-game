import pygame
import math
import random

pygame.init()

width = 800
height = 800

bg = pygame.image.load("images/bg.png")
rocket = pygame.image.load("images/rocket.png")
star = pygame.image.load("images/star.png")
asteroid_small = pygame.image.load("images/asteroid_small.png")
asteroid_med = pygame.image.load("images/asteroid_med.png")
asteroid_big = pygame.image.load("images/asteroid_big.png")
alien_ship = pygame.image.load("images/alien_ship.png")

shoot = pygame.mixer.Sound("sounds/shoot.wav")
bangSmall = pygame.mixer.Sound("sounds/bangSmall.wav")
bangLarge = pygame.mixer.Sound("sounds/bangLarge.wav")

shoot.set_volume(0.25)
bangSmall.set_volume(0.25)
bangLarge.set_volume(0.25)

pygame.display.set_caption("Asteroid Game")
window = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

game_over = False
score = 0
lives = 3
high_score = 0

class Player(object):
    def __init__(self):
        self.img = rocket
        