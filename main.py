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
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = width//2
        self.y = height//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine*self.w//2, self.y - self.sine*self.h//2)
    
    def draw(self,window):
        window.blit(self.rotatedSurf, self.rotatedRect)
        
    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img,self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine* self.w//2, self.y - self.sine*self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine*self.w//2, self.y - self.sine*self.h//2)
    
    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine*self.w//2, self.y - self.sine*self.h//2)

    def updateLocation(self):
        if self.x > width + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = width
        elif self.y < -50:
            self.y = height
        elif self.y > height + 50:
            self.y = 0