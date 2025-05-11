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
window = pygame.display.set_mode((width, height))
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
        self.x = width // 2
        self.y = height // 2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (
            self.x + self.cosine * self.w // 2,
            self.y - self.sine * self.h // 2,
        )

    def draw(self, window):
        window.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (
            self.x + self.cosine * self.w // 2,
            self.y - self.sine * self.h // 2,
        )

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (
            self.x + self.cosine * self.w // 2,
            self.y - self.sine * self.h // 2,
        )

    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (
            self.x + self.cosine * self.w // 2,
            self.y - self.sine * self.h // 2,
        )

    def updateLocation(self):
        if self.x > width + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = width
        elif self.y < -50:
            self.y = height
        elif self.y > height + 50:
            self.y = 0


class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self):
        if self.x < -50 or self.x > width or self.y < -50 or self.y > height:
            return True


class asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid_small
        elif self.rank == 2:
            self.image = asteroid_med
        else:
            self.image = asteroid_big
        self.w = 50 * rank
        self.h = 50 * rank
        self.randomPoint = random.choice(
            [
                (
                    random.randrange(0, width - self.w),
                    random.choice([0, height - self.h]),
                ),
                (
                    random.choice([-1 * self.w - 5, width + 5]),
                    random.randrange(0, height - self.h),
                ),
            ]
        )
        self.x, self.y = self.randomPoint
        if self.x < width // 2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < height // 2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1, 3)
        self.yv = self.ydir * random.randrange(1, 3)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))


class Star(object):
    def __init__(self):
        self.img = star
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.randomPoint = random.choice([(random.randrange(0, width - self.w), random.choice([-1 * self.h - 5, height + 5])),
                                       (random.choice([-1 * self.w - 5, width + 5]), random.randrange(0, height - self.h))])
        self.x, self.y = self.randomPoint
        if self.x < width//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < height//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2
    def draw(self,window):
        window.blit(self.img, (self.x, self.y))

class Alien(object):
    def __init__(self):
        self.img = alien_ship
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.randomPoint = random.choice([(random.randrange(0, width - self.w), random.choice([-1 * self.h - 5, height + 5])),
                                       (random.choice([-1 * self.w - 5, width + 5]), random.randrange(0, height - self.h))])
        self.x, self.y = self.randomPoint
        if self.x < width//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < height//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self,window):
        window.blit(self.img, (self.x, self.y))

class AlienBullet(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 4
        self.dx, self.dy = player.x - self.x, player.y - self.y
        self.dis = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx/self.dis, self.dy/self.dis
        self.xv = self.dx * 5
        self.yv = self.dy * 5
    
    def draw(self, window):
        pygame.draw.rect(window, (255,255,255), [self.x, self.y, self.w, self.h])

def redrawWindow():
    window.blit(bg, (0,0))
    font = pygame.font.SysFont('times new roman', 30)
    lives_txt = font.render("Lives: " + str(lives),1,(255,255,255))
    playagain_txt = font.render ("Press Tab to play again",1, (255,255,255))
    score_txt = font.render ("Score: " + str(score),1, (255,255,255))
    highscore_txt = font.render ("High Score: " + str(score),1, (255,255,255))


player = Player()
