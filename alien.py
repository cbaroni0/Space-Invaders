import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen, value):
        """Initialize the alien and set its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.value = value
        self.counter = 0
        self.bool = False

        # Load the alien image and set its rect attribute
        if self.value == 0:
            self.image = pygame.image.load('images/alien0a.png')
        elif self.value == 1:
            self.image = pygame.image.load('images/alien1a.png')
        else:
            self.image = pygame.image.load('images/alien2a.png')
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        #self.value = 1

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if aliens is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien left or right"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.counter += 1
        if self.counter == 300:
            self.counter = 0
            if self.bool == False:
                if self.value == 0:
                    self.image = pygame.image.load('images/alien0b.png')
                elif self.value == 1:
                    self.image = pygame.image.load('images/alien1b.png')
                else:
                    self.image = pygame.image.load('images/alien2b.png')
                self.bool = True
            else:
                if self.value == 0:
                    self.image = pygame.image.load('images/alien0a.png')
                elif self.value == 1:
                    self.image = pygame.image.load('images/alien1a.png')
                else:
                    self.image = pygame.image.load('images/alien2a.png')
                self.bool = False
            self.image = pygame.transform.scale(self.image, (25, 25))
