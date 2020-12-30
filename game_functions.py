import pygame
import sys
from bullet import Bullet
from pygame.sprite import Sprite
from alien import Alien
from stars import Star
from random import randint
from time import sleep
from game_stats import GameStats

def check_key_down(event, ai_settings, screen, ship, bullets, flash):

    if event.key == pygame.K_RIGHT:
        """向右移动"""
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        """向左移动"""
        ship.moving_left = True

    elif event.key == pygame.K_UP:
        """向up移动"""
        ship.moving_up = True

    elif event.key == pygame.K_DOWN:
        """向down移动"""
        ship.moving_down = True

    elif event.key == pygame.K_SPACE:
        """发射"""
        new_bullet = Bullet(ai_settings , screen, ship)
        bullets.add(new_bullet)
        flash.fire_simble = True

    elif event.key == pygame.K_q:
        """quit"""
        sys.exit()

def check_key_up(event, ship, flash):
    """结束向left移动"""
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

    elif event.key == pygame.K_RIGHT:
        """结束向right移动"""
        ship.moving_right = False

    elif event.key == pygame.K_UP:
        """结束向上移动"""
        ship.moving_up = False

    elif event.key == pygame.K_DOWN:
        """结束向down移动"""
        ship.moving_down = False

    elif event.key == pygame.K_SPACE:
        flash.fire_simble = False


def check_event(ai_settings, screen, ship, bullets, flash, stats, play_button, aliens, sb):
    """监视键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down(event, ai_settings, screen, ship, bullets, flash)

        elif event.type == pygame.KEYUP:
            check_key_up(event, ship, flash)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y,ai_settings, screen, aliens, ship, bullets, sb)

def check_play_button(stats, play_button, mouse_x, mouse_y,ai_settings, screen, aliens, ship, bullets, sb):
    """单击play开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.game_active = True
        stats.reset_stats()

        """重置记分牌"""
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()

        """清空外星人和子弹列表"""
        aliens.empty()
        bullets.empty()

        """创建新的外星人 并重置飞船位置"""
        creat_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()


def update_bullet(ai_settings, screen, aliens, ship, bullets, stats, sb):
    bullets.update()
    """删除屏幕外的子弹"""
    for bullet in bullets.copy():
        if bullet.rect.bottom <= -1:
            bullets.remove(bullet)

    """检测外星人列表是否为空"""
    if not aliens:
        bullets.empty()
        ai_settings.increase_speed()
        creat_fleet(ai_settings, screen, aliens, ship)
        stats.level += 1
        sb.prep_level()

    """更新子弹的位置后检测子弹和外星人是否有碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    if collisions:
        aliens = collisions.values()
        for alien in aliens:
            stats.score += ai_settings.alien_point * len(alien)
            sb.prep_score()
        check_high_score(stats, sb)

def check_high_score(stats, sb):
    """检查是否有新的高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_star(stars, ai_settings):
    for star in stars.copy():
        if star.rect.centerx >= ai_settings.screen_width or star.rect.bottom >= ai_settings.screen_height:
                stars.remove(star)

def check_fleet_egdes(ai_settings, aliens):
    """只要有一个外星人到达边缘就采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """整体下移并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, aliens, ship, bullets, stats, screen, sb):
    check_fleet_egdes(ai_settings, aliens)
    aliens.update()

    """检测外星人与飞船的碰撞"""
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, aliens, ship, bullets, stats, screen, sb)

    """检查是否有alien到达屏幕底端"""
    check_alien_bottom(ai_settings, aliens, ship, bullets, stats, screen, sb)

def check_alien_bottom(ai_settings, aliens, ship, bullets, stats, screen, sb):
    """检查是否有外星人到达屏幕底端"""
    for alien in aliens.sprites():
        if alien.rect.bottom >= ai_settings.screen_height:
            ship_hit(ai_settings, aliens, ship, bullets, stats, screen, sb)
            break

def ship_hit(ai_settings, aliens, ship, bullets, stats, screen, sb):
    """响应被撞到的飞船 飞船-1"""
    if stats.ship_left > 0:
        stats.ship_left -= 1

        """清空外星人和子弹列表"""
        aliens.empty()
        bullets.empty()

        """创建新的外星人 并重置飞船位置"""
        creat_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        sb.prep_ship()

        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_screen(bg_color, ship, screen, bullets, flash, aliens, stars, ai_settings, play_button, stats, sb):
    """更新屏幕"""
    screen.fill(bg_color)
    stars.draw(screen)
    ship.blitme()
    flash.blitme()
    aliens.draw(screen)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw()

    if not stats.game_active:
        play_button.draw_button()

    """让最近绘制的屏幕可见"""
    pygame.display.update()


def get_alien_number_x(ai_settings, alien_width):
    '''得到每行外星人的数量'''
    # 创建一个外星人并计算一行能容纳的外星人数
    # 外星人间距为外星人宽度

    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_of_aliens_x = int(available_space_x / (2 * alien_width))
    return number_of_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''得到外星人的行数'''
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    numer_rows = int(available_space_y / (2 * alien_height))
    return numer_rows

def creat_alien(ai_settings, aliens, screen, alien_width, alien_number, row_unmber):
    """创建一个alien并加入当前行"""
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_unmber
    aliens.add(alien)

def creat_fleet(ai_settings, screen, aliens, ship):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_of_aliens_x = get_alien_number_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
    #创建第一行外星人
        for alien_number in range(number_of_aliens_x):
            creat_alien(ai_settings, aliens, screen, alien_width, alien_number, row_number)

def get_star_number_x(star, ai_settings):
    number_x = (ai_settings.screen_width / (2 * star.rect.width))
    return  int(number_x)

def get_star_row_number(star, ai_settings):
    number_row = (ai_settings.screen_height / (2 * star.rect.height))
    return int(number_row)

def creat_star(ai_settings, screen, star_y, star_x, star_width, star_height, stars):
    star = Star(ai_settings, screen)
    star.rect.x = (star_width + 5 * star_width * star_x + randint(-20, 20))
    star.rect.y = -(star_height + 5 * star_height * star_y + randint(-20, 20))
    stars.add(star)

def creat_bg(ai_settings, screen, stars):

    star = Star(ai_settings, screen)
    star_width = star.rect.width
    number_rows = get_star_row_number(star, ai_settings)
    star_numbers = get_star_number_x(star, ai_settings)

    if len(stars) <= 400:
        for star_y in range(number_rows):
            for star_x in range(star_numbers):
                creat_star(ai_settings, screen, star_y, star_x, star.rect.width, star.rect.height, stars)






