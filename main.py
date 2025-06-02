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
rapid_fire = False
rfStart = -1
isSoundOn = True
player_bullets = []
asteroids = []
count = 0
stars = []
aliens = []
alien_bullets = []
run = True


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
    player.draw(window)
    for a in asteroids:
        a.draw(window)
    for b in player_bullets:
        b.draw(window)
    for s in stars:
        s.draw(window)
    for a in aliens:
        a.draw(window)
    for a in alien_bullets:
        a.draw(window)
    if rapid_fire:
        pygame.draw.rect(window, (0,0,0),[width//2-51, 19, 102, 22])
        pygame.draw.rect(window,(255,255,255),[width//2 - 50, 20, 100-100*(count-rfStart)/500,20])
    if game_over:
        window.blit(playagain_txt, (width//2 - playagain_txt.get_width()//2, height//2 - playagain_txt.get_height()//2))
    window.blit(score_txt, (width-score_txt.get_width()-25,25))
    window.blit(lives_txt, (25,25))
    window.blit(highscore_txt, (width - highscore_txt.get_width()-25, 35 + score_txt.get_height()))
    pygame.display.update()



player = Player()
while run:
    clock.tick(60)
    count += 1
    if not game_over:
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(asteroid(ran))
        if count % 1000 == 0:
            stars.append(Star())
        if count % 750 == 0:
            aliens.append(Alien())
        for i, a in enumerate(aliens):
            a.x += a.xv
            a.y += a.yv
            if a.x > width + 150 or a.x + a.w < - 100 or a.y > height + 150 or a.y + a.h < -100:
                aliens.pop(i)
            if count % 60 == 0:
                alien_bullets.append(AlienBullet(a.x+a.w//2,a.y+a.h//2))
            for b in player_bullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x +a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y +b.h >= a.y and b.y + b.h <= a.y + a.h:
                        aliens.pop(i)
                        if isSoundOn:
                            bangLarge.play()
                        score += 50
                        break
        for i, a in enumerate(alien_bullets):
            a.x += a.xv
            a.y += a.yv
            if (a.x>=player.x-player.w//2 and a.x <= player.x + player.w//2) or a.x + a.w >= player.x - player.w//2 and a.x + a.w <= player.x + player.w//2:
                if (a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or a.y + a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2:
                    lives -= 1
                    alien_bullets.pop(i)
                    break
        player.updateLocation()
        for b in player_bullets:
            b.move()
            if b.checkOffScreen():
                player_bullets.pop(player_bullets.index(b))
        for a in asteroids:
            a.x += a.xv
            a.y += a.yv
            if (a.x>=player.x-player.w//2 and a.x <= player.x + player.w//2) or a.x + a.w >= player.x - player.w//2 and a.x + a.w <= player.x + player.w//2:
                if (a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or a.y + a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2:
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    break
            for p in player_bullets:
                if (p.x >= a.x and p.x <= a.x + a.w) or p.x + p.w >= a.x and p.x + p.w <= a.x +a.w:
                    if (p.y >= a.y and p.y <= a.y + a.h) or p.y +p.h >= a.y and p.y + p.h <= a.y + a.h:
                        if (a.rank == 3):
                            if isSoundOn:
                                bangLarge.play()
                            score += 10
                            na1 = asteroid(2)
                            na2 = asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            if isSoundOn:
                                bangSmall.play()
                            score += 20
                            na1 = asteroid(1)
                            na2 = asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                            if isSoundOn:
                                bangSmall.play()
                        asteroids.pop(asteroids.index(a))
                        player_bullets.pop(player_bullets.index(p))
                        break
        for s in stars:
            s.x += s.xv
            s.y += s.yv
            if s.x < - 100 - s.w or s.x > width + 100 or s.y > height + 100 or s.y < -100 - s.h:
                stars.pop(stars.index(s))
                break
            for b in player_bullets:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x +s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y +b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapid_fire = True
                        rfStart = count
                        stars.pop(stars.index(s))
                        player_bullets.pop(player_bullets.index(b))
                        break
        if lives <= 0:
            game_over = True
        if rfStart != -1:
            if count - rfStart > 500:
                rapid_fire = False
                rfStart = -1

        



        
