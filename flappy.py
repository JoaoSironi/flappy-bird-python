import pygame
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED= 10
GRAVITY = 1

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
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2
        
    def update(self):
        self.currentImage = (self.currentImage + 1) %3
        self.image = self.images[self.currentImage]

        self.speed += GRAVITY

        #update hieght
        self.rect[1] += self.speed
    
    def bump(self):
        self.speed = -SPEED


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

birdGroup = pygame.sprite.Group()
bird = Bird()
birdGroup.add(bird)

clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()
 
    screen.blit(BACKGROUND, (0,0))

    birdGroup.update()

    birdGroup.draw(screen)
    
    pygame.display.update()
