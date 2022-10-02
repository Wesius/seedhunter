import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *
import sys
from seedHunterClasses import *

gitTest = 0

# Colors
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
score = 0
chocolateLst = []
seedLst = []

pygame.init()
pygame.font.init()

# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()

chocolateSound = pygame.mixer.Sound("data/pickupCoin.wav")
gameOverSound = pygame.mixer.Sound("data/gameOver.wav")
victorySound = pygame.mixer.Sound("data/victory.wav")

gameOverC = Text("Game over!", "data/baloo2.ttf", 60, RED)
startTextC = Text("Start", "data/baloo2.ttf", 60, RED)

# Splash Screen
splashScreen = Background('data/splashScreen.png', [0, 0])
screen.blit(splashScreen.image,
            (splashScreen.rect.left, splashScreen.rect.top))
pygame.display.flip()
pygame.time.delay(1500)

startScreen = Background('data/startScreen.png', [0, 0])


# Initializing player
p = Player()

# Spawning in chocolates and seeds
[chocolateLst.append(Chocolate(int(p.y_coord))) for i in range(difficulty)]
[seedLst.append(Seed(int(p.y_coord))) for i in range(INITIAL_SEED_COUNT)]

p.y_coord -= 500

mouseX = 0
mouseY = 0

# Initializing backgrounds
bg = [Background('data/bg.png', [0, 0]), Background('data/bg.png',
                                                    [0, -500]), Background('data/bg.png', [0, -1000]), Background('data/bg.png', [0, 500]), Background('data/bg.png', [0, 1000])]



#######################################################################################
#******************************** Main game loop***************************************
#######################################################################################
while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and gameStarted == False:
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            if mouseX > 225 and mouseX < 475 and mouseY > 350 and mouseY < 450:
                gameStarted = True

    if gameStarted == True:
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
            if back.rect.bottom < p.y_coord - 250:
                back.rect.bottom += 1000

        # Removes chocolates below the player
        chocolateLst = [
            chocolate for chocolate in chocolateLst if not p.y_coord < chocolate.y_coord - 300]

        # Removes seeds that are colliding with player and seeds far below the player
        seedLst = [
            seed for seed in seedLst if not p.Rect.colliderect(seed.Rect)]
        seedLst = [seed for seed in seedLst if not p.y_coord <
                   seed.y_coord - 300]

        if len(chocolateLst) < difficulty:
            chocolateLst.append(Chocolate(int(p.y_coord)))

        if len(seedLst) < INITIAL_SEED_COUNT:
            seedLst.append(Seed(int(p.y_coord)))
            difficulty += 1 

        if gameOver == True:
            scoreText = Text("Score: " + str(score), "data/baloo2.ttf", 50, RED)
            p.x_coord = 1000
            p.y_coord = -1000
            p.kill()
            for chocolate in chocolateLst:
                chocolate.kill()
            for seed in seedLst:
                seed.kill()
            for b in bg:
                b.kill()
            gameOverC.renderText(screen, screen.get_width() // 2 - 150, screen.get_height()//2 - 50)
            scoreText.renderText(screen, 0, 0)
            pygame.display.flip()
            pygame.time.delay(5000)
            done = True
            # TODO Go back to start screen

        [screen.blit(chocolate.image, (chocolate.x_coord, chocolate.y_coord + camOffset))
         for chocolate in chocolateLst]
        [screen.blit(seed.image, (seed.x_coord, seed.y_coord + camOffset))
         for seed in seedLst]
        screen.blit(p.image, (p.x_coord, p.y_coord + camOffset))

        # Two gameover conditions
        for chocolate in chocolateLst:
            if p.Rect.colliderect(chocolate.rect):
                pygame.mixer.Sound.play(gameOverSound)
                gameOver = True
        
        for seed in seedLst:
            if p.Rect.colliderect(seed.rect):
                #FIXME Score getting higher too fast.
                score += 1
                print("hit")

        if p.y_coord > screen.get_height() + camOffset:
            pygame.mixer.Sound.play(gameOverSound)
            p.x_coord = 10000
            p.y_coord = -10000
            gameOver = True

    else:
        screen.blit(startScreen.image,
                    (startScreen.rect.left, startScreen.rect.top))
        pygame.draw.rect(screen, PINK, Rect(225, 350, 250, 100))
        startTextC.renderText(screen, 280, 350)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()