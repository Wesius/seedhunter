import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *
import sys
import random
import os

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (217, 87, 99)

# Gameplay constants
DIFFICULTY_CHANGE_RATE = 1
INITIAL_SEED_COUNT = 2

difficulty = 1

playSound = True
gameOver = False
gameStarted = False
camOffset = 0
chocolateLst = []
seedLst = []

pygame.init()
pygame.font.init()

# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()

font = pygame.font.Font("data/baloo2.ttf", 60)
gameOverText = font.render("Game Over!", True, RED)
startText = font.render("Start", True, RED)

chocolateSound = pygame.mixer.Sound("data/pickupCoin.wav")
gameOverSound = pygame.mixer.Sound("data/gameOver.wav")
victorySound = pygame.mixer.Sound("data/victory.wav")

# *************************** CLASSES ***********************************


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.sprite1 = pygame.image.load("data/bird.png")
        self.sprite2 = pygame.image.load("data/bird2.png")
        self.image = self.sprite1

        self.x_speed = 3
        self.y_speed = 0

        self.x_coord = 350
        self.y_coord = 100

        self.acceleration = 0.1
        self.velocity = 0

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.x_coord, self.y_coord
        self.Rect = pygame.Rect(self.x_coord, self.y_coord, 20, 20)

    def keyCheck(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.y_speed = -3
                    self.velocity = 0

    def move(self, screen):
        if self.x_coord + 20 > screen.get_width():
            self.x_speed = -3
            self.image = self.sprite2
        elif self.x_coord < 0:
            self.x_speed = 3
            self.image = self.sprite1

        self.x_coord += self.x_speed
        self.y_coord += self.y_speed + self.velocity
        self.velocity += self.acceleration

        self.Rect = pygame.Rect(self.x_coord, self.y_coord, 20, 20)


class Interactable(pygame.sprite.Sprite):
    def __init__(self, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)

        self.x_coord = random.randint(0, 700)
        self.y_coord = random.randint(y - 1000, y - 300)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.x_coord, self.y_coord
        self.Rect = pygame.Rect(self.x_coord, self.y_coord, 20, 20)


class Chocolate(Interactable):
    def __init__(self, y):
        super().__init__(y, "data/chocolate.png")


class Seed(Interactable):
    def __init__(self, y):
        super().__init__(y, "data/seed.png")
# ***************************************** CLASSES ***********************************


# Splash Screen
splashScreen = Background('data/splashScreen.png', [0, 0])
screen.blit(splashScreen.image,
            (splashScreen.rect.left, splashScreen.rect.top))
pygame.display.flip()
pygame.time.delay(1500)

startScreen = Background('data/startScreen.png', [0, 0])
while gameStarted == False:
    screen.blit(startScreen.image,
                (startScreen.rect.left, startScreen.rect.top))
    pygame.draw.rect(screen, PINK, Rect(225, 350, 250, 100))
    screen.blit(startText, (280, 350))
    pygame.display.flip()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            if mouseX > 225 and mouseX < 475 and mouseY > 350 and mouseY < 450:
                gameStarted = True
# Initializing player
p = Player()

# Spawning in chocolates and seeds
[chocolateLst.append(Chocolate(int(p.y_coord))) for i in range(difficulty)]
[seedLst.append(Seed(int(p.y_coord))) for i in range(INITIAL_SEED_COUNT)]

p.y_coord -= 500

# Initializing backgrounds
# FIXME Gotta fix the fact that backgrounds vanish when player goes too far down
bg = [Background('data/bg.png', [0, 0]), Background('data/bg.png',
                                                    [0, -500]), Background('data/bg.png', [0, -1000])]
# Main game loop
while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    # Changing camera offset
    camOffset = -p.y_coord + screen.get_height()/2

    # Player functions
    p.keyCheck(events)
    p.move(screen)

    # Background procesing
    if gameOver == False:
        screen.fill((35, 206, 235))

    # Blit
    [screen.blit(back.image, (back.rect.left, back.rect.top + camOffset))
     for back in bg]
    # Background processing
    for back in bg:
        if back.rect.top > p.y_coord + 250:
            back.rect.top -= 1000

    # Removes chocolates below the player
    chocolateLst = [
        chocolate for chocolate in chocolateLst if not p.y_coord < chocolate.y_coord - 300]

    # Removes seeds that are colliding with player and seeds far below the player
    seedLst = [seed for seed in seedLst if not p.Rect.colliderect(seed.Rect)]
    seedLst = [seed for seed in seedLst if not p.y_coord < seed.y_coord - 300]

    if len(chocolateLst) < difficulty:
        chocolateLst.append(Chocolate(int(p.y_coord)))

    if len(seedLst) < INITIAL_SEED_COUNT:
        seedLst.append(Seed(int(p.y_coord)))
        difficulty += 1

    for chocolate in chocolateLst:
        if p.Rect.colliderect(chocolate.rect):
            pygame.mixer.Sound.play(gameOverSound)
            gameOver = True

    if gameOver == True:
        p.x_coord = 1000
        p.y_coord = -1000
        p.kill()
        for chocolate in chocolateLst:
            chocolate.kill()
        for seed in seedLst:
            seed.kill()
        screen.blit(gameOverText, (screen.get_width() //
                    2 - 150, screen.get_height()//2 - 50))
        pygame.display.flip()
        # pygame.time.delay(5000)
        # TODO Go back to start screen

    [screen.blit(chocolate.image, (chocolate.x_coord, chocolate.y_coord + camOffset))
     for chocolate in chocolateLst]
    [screen.blit(seed.image, (seed.x_coord, seed.y_coord + camOffset))
     for seed in seedLst]
    screen.blit(p.image, (p.x_coord, p.y_coord + camOffset))

    if p.y_coord > screen.get_height() + camOffset:
        pygame.mixer.Sound.play(gameOverSound)
        p.x_coord = 10000
        p.y_coord = -10000
        gameOver = True

    pygame.display.flip()
    clock.tick(60)

    gitTest = 10

pygame.quit()
sys.exit()
