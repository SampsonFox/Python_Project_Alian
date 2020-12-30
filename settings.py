class Settings():
    """初始化静态设置"""
    """储存设置"""
    def __init__(self):
        """屏幕参数"""
        self.game_title = 'Alian War'
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (6, 80, 165)


        """子弹参数"""
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = [123, 255, 255]

        """外星人设置"""
        self.fleet_drop_speed = 10
        #fleet_direction = -1 时向左移动
        self.fleet_direction = 1

        """飞船设置"""
        self.ship_limit = 3

        """以什么样的速度加快游戏"""
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.speed_facter = 2
        self.bullet_speed = 5
        self.alien_speed_factor = 1

        self.fleet_direction = 1

        '''积分'''
        self.alien_point = 50

    def increase_speed(self):
        """提高速度"""
        self.speed_facter *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_point = int(self.alien_point * self.score_scale)








