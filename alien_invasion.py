import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from  ship import Flash
from pygame.sprite import Group
import game_functions as gf
from bullet import Bullet
from button import Button
from scoreboard import Scoreboard
from stars import Star
from os import path
import sys

bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
path_to_dat = path.join(bundle_dir, 'image')

def run_game():
    """初始化游戏并创建屏幕对象"""

    ai_settings = Settings()
    #不能直接用类调用 需要用实例调用

    pygame.init()
    screen = pygame.display.set_mode((
        ai_settings.screen_width,
        ai_settings.screen_height))
    pygame.display.set_caption(
        ai_settings.game_title)

    """创建play按钮"""
    play_button = Button(ai_settings, screen, 'Play')

    bg_color = ai_settings.bg_color

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    flash = Flash(ship, ai_settings, screen)

    #bullet
    bullets = Group()

    #alien
    aliens = Group()
    gf.creat_fleet(ai_settings, screen, aliens, ship)

    #stars
    stars = Group()
    #gf.creat_bg(ai_settings, screen, stars)


    """开始游戏循环"""
    while True:

        gf.check_event(ai_settings, screen, ship, bullets, flash, stats, play_button, aliens, sb)
        stars.update()
        gf.update_star(stars, ai_settings)
        if stats.game_active:
            ship.update()
            flash.update()
            gf.update_bullet(ai_settings, screen, aliens, ship, bullets, stats, sb)
            gf.update_aliens(ai_settings, aliens, ship, bullets, stats, screen, sb)

        gf.creat_bg(ai_settings, screen, stars)
        gf.update_screen(bg_color, ship, screen, bullets, flash,
                         aliens, stars, ai_settings, play_button, stats, sb)

run_game()




#pyinstaller -D alien_invasion.py -p alien.py -p button.py -p bullet.py -p alien.py -p game_functions.py -p game_stats.py -p settings.py -p ship.py -p stars.py -p image
