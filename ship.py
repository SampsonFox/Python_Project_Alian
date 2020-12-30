import pygame
from pygame.sprite import Sprite
from os import path
import sys

bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
path_to_dat = path.join(bundle_dir, 'image/ship_self.png')

class Ship(Sprite):
    """创建飞船"""

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        """初始化飞船并设置初始位置"""
        self.screen = screen

        """加载图像并获取外接矩形"""
        self.image = pygame.image.load(path_to_dat)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()


        """初始位置"""
        self.rect.centerx = self.screen_rect.centerx
        """"把屏幕矩形的中心设置为飞船矩形的中心"""

        self.rect.bottom = self.screen_rect.bottom
        """把屏幕矩形的底的数值设置为飞船矩形的底的数值"""
        self.ai_settings = ai_settings

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        """指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """调整飞船位置"""

        if self.moving_right:
            if self.rect.right <= self.screen_rect.right:
                self.rect.centerx += self.ai_settings.speed_facter

        if self.moving_left:
            if self.rect.left >= self.screen_rect.left:
                self.rect.centerx -= self.ai_settings.speed_facter

        if self.moving_up:
            if self.rect.top >= self.screen_rect.top:
                self.rect.centery -= self.ai_settings.speed_facter

        if self.moving_down:
            if self.rect.bottom <= self.screen_rect.bottom:
                self.rect.centery += self.ai_settings.speed_facter

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom



class Flash():
    def __init__(self, ship, ai_settings, screen):
        """初始化飞船并设置初始位置"""
        self.screen = screen

        """显示开火标志"""
        self.fire_image = pygame.image.load('image/ship_fire.png')
        self.fire_rect = self.fire_image.get_rect()
        self.screen_rect = screen.get_rect()

        """初始位置"""
        self.fire_rect.centerx = self.screen_rect.centerx
        """"把屏幕矩形的中心设置为飞船矩形的中心"""
        self.fire_rect.bottom = self.screen_rect.bottom
        """把屏幕矩形的底的数值设置为飞船矩形的底的数值"""
        self.ai_settings = ai_settings

        self.ship_rect = ship.rect

        self.fire_simble = False

    def blitme(self):
        """指定位置绘制飞船"""###################################
        self.screen.blit(self.fire_image, self.fire_rect)

    def update(self):
        self.fire_rect.centerx = self.ship_rect.centerx
        self.fire_rect.bottom = self.ship_rect.bottom

        if self.fire_simble:
            self.fire_image = pygame.image.load('image/ship_fire.png')
        else:
            self.fire_image = pygame.image.load('image/ship_fire_blank.png')


