
class Settings:
    '''初始化游戏设置的类'''

    def __init__(self):
        '''初始化游戏设置'''
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 254)

        # 飞船设置
        self.ship_speed = 2
        self.ship_limit = 1

        # 子弹设置
        self.bullet_speed = 1.0
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (255, 0, 0)
        self.bullet_allowed = 5

        # 外星人设置
        self.alien_speed = 0.5
        self.fleet_drop_speed = 100
        # 1向右，-1向左
        self.fleet_direction = 1
