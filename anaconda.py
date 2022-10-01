import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *
import random
from anaconda import *

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
        if self.x_coord + 30 > screen.get_width():
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
        
class Text():
    def __init__(self, text, font, size, color):
        self.localFont = pygame.font.Font(font, size)
        self.localText = self.localFont.render(text, True, color)
        
    def renderText(self, screen, x, y):
        screen.blit(self.localText,(x, y))