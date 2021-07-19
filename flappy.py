import pygame
import random
from pygame.locals import *

FPS = 30
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED= 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 

        self.images = [
            pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
            pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
            pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
        ]

        self.speed = SPEED

        self.currentImage = 0

        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2
        
    def update(self):
        self.currentImage = (self.currentImage + 1) % 3
        self.image = self.images[self.currentImage]

        self.speed += GRAVITY

        self.rect[1] += self.speed
    
    def bump(self):
        self.speed = -SPEED


class Pipe(pygame.sprite.Sprite):
    
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        
        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.image.load('assets/sprites/base.png')
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def offScreen(sprite):
    return sprite.rect[0] < (-sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipeInverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipeInverted)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('assets/sprites/background-day.png').convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

birdGroup = pygame.sprite.Group()
bird = Bird()
birdGroup.add(bird)

groundGroup = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    groundGroup.add(ground)

pipeGroup = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipeGroup.add(pipes[0])
    pipeGroup.add(pipes[1])

clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird')

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()
 
    screen.blit(BACKGROUND, (0,0))

    if offScreen(groundGroup.sprites()[0]):
        groundGroup.remove(groundGroup.sprites()[0])

        newGround = Ground(GROUND_WIDTH - 20)
        groundGroup.add(newGround)

    if offScreen(pipeGroup.sprites()[0]):
        pipeGroup.remove(pipeGroup.sprites()[0])
        pipeGroup.remove(pipeGroup.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)
        pipeGroup.add(pipes[0])
        pipeGroup.add(pipes[1])

    birdGroup.update()
    groundGroup.update()
    pipeGroup.update()

    birdGroup.draw(screen)
    pipeGroup.draw(screen)
    groundGroup.draw(screen)
    
    pygame.display.update()

    if (pygame.sprite.groupcollide(birdGroup, groundGroup, False, False, pygame.sprite.collide_mask)
    or pygame.sprite.groupcollide(birdGroup, pipeGroup, False, False, pygame.sprite.collide_mask)) :
        #Game over
        pygame.display.update()
        break
