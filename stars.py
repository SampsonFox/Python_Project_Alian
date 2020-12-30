import pygame
from pygame.sprite import Sprite
from os import path
import sys

bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
path_to_dat = path.join(bundle_dir, 'image/star25.png')

class Star(Sprite):
    """创建星星"""
    def __init__(self,ai_settings, screen):
        super(Star, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        self.image = pygame.image.load(path_to_dat)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        #self.rect.x += 1
        self.rect.y += 1



