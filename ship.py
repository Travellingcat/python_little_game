import pygame
from settings import Settings
class Ship:
    '''管理飞船的类'''

    def __init__(self, ai_game):
        '''初始化飞船，并设置初始位置'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.move_right = False
        self.move_left = False
        self.settings = Settings()

        # 加载飞船图像，并获取外接矩形
        self.image = pygame.image.load('images/ship3.png')
        self.rect = self.image.get_rect()

        # 将每艘飞船放到屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        '''在指定的位置绘制图像'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 响应按键，并限制飞船活动范围
        if self.move_right == True and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        elif self.move_left == True and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed

    def ship_center(self):
        # 飞船居中
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)