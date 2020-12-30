import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    '''显示得分信息的类'''

    def __init__(self, ai_settings, screen, stats):
        '''初始化属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #字体设置
        self.text_color = [30, 30, 30]
        self.font = pygame.font.SysFont(None, 48)

        #准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    def prep_level(self):
        '''将等级转化为图像'''
        self.level_image = self.font.render('Level ' + str(self.stats.level), True,
                                            self.text_color)

        '''等级放在得分下方'''
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.screen_rect.right - 20

    def prep_score(self):
        '''得分转化为图像'''
        rounded_score = int(round(self.stats.score))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render('Score ' + score_str, True, self.text_color, self.ai_settings.bg_color)

        #得分放在右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render('Top Score ' + high_score_str, True,
                                                 self.text_color, self.ai_settings.bg_color)

        #放在屏幕中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = 20
        self.high_score_rect.centerx = self.screen_rect.centerx

    def show_score(self):
        '''在荧幕上显示得分'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #绘制飞船
        self.ship.draw(self.screen)

    def prep_ship(self):
        self.ship = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.centerx = 50 + ship_number * ship.rect.width
            ship.rect.y = 0
            self.ship.add(ship)
