import pygame
from pygame.sprite import Sprite


class Barrier(Sprite):
    def __init__(self, screen, settings):
        super(Barrier, self).__init__()
        self.hit = 0
        self.image = pygame.image.load('images/barrier1.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 50, 50

        self.screen = screen
        self.settings = settings

    def update(self, barriers):
        if self.hit == 0:
            self.image = pygame.image.load("images/barrier2.png")
            self.hit += 1
        elif self.hit == 1:
            self.image = pygame.image.load("images/barrier3.png")
            self.hit += 1
        elif self.hit == 2:
            barriers.remove(self)

    def draw_barrier(self):
        self.screen.blit(self.image, self.rect)
