import pygame
from pygame.sprite import Sprite
from os import path
import sys

bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
path_to_dat = path.join(bundle_dir, 'image/alien_black.png')

class Alien (Sprite):
    """表示单个外星人"""
    def __init__(self, ai_settings, screen):
        """初始化外星人并设置位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        """赋予rect属性"""
        self.image = pygame.image.load(path_to_dat)
        self.rect = self.image.get_rect()

        """初始位置 左上角"""
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        """储存确切位置"""
        self.x = float(self.rect.x)

    def blitme(self):
        """绘制"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        '''碰到边缘返回True'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x