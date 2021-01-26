import pygame
import sys
import time
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_status import GameStatus
from gameover import Gameover

class AlienInvasion:
    '''管理游戏行为和资源的类'''

    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('外星人入侵')
        # 设置游戏背景颜色
        self.bg_color = self.settings.bg_color

        # 实例化飞船，并将主程序作为对象传入
        self.ship = Ship(self)
        # 实例化子弹编组
        self.bullets = pygame.sprite.Group()
        # 实例化外星人编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.status = GameStatus(self)
        self.gameover = Gameover(self)


    def run_game(self):
        '''开始游戏主循环'''
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()


    def _check_events(self):
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keydown_events(self, event):
        # 监听按下按键事件
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self, event):
        # 监听松开按键事件
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False

    def _fire_bullet(self):
        '''创建一颗子弹并将其加入到编组中'''
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # 更新子弹
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        # print(len(self.bullets))

    def _check_bullet_alien_collisions(self):
        # 射杀外星人
        collosions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # 生成新的外星人
        if not self.aliens:
            self.settings.alien_speed += 1
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        '''创建外星人群'''
        # 一行可以容纳外星人数量
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avaliable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avaliable_space_x // (2 * alien_width)
        # 可以容纳的外星人行数
        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = avaliable_space_y // (2 * alien_height)
        # 创建多行外星人
        for row_number in range(number_rows):
            # 创建一行外星人
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        # 检查外星人是否撞到边缘
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''向下移动一格并改变外星人方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print('ship hit!!!')
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        # 判断外星人是否到达底部
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        '''响应飞船碰撞'''
        if self.status.ships_left > 0:
            self.status.ships_left -= 1
            # 清空外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建新的外星人群
            self._create_fleet()
            self.ship.ship_center()
            time.sleep(0.5)
        else:
            self.status.game_active = False
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            self.gameover.blitme()
            self.settings.fleet_drop_speed = 0
            self.settings.alien_speed = 0
            self.ship.move_right = False
            self.ship.move_left = False
            pygame.display.flip()

    def _update_screen(self):
        # 每次循环重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # 让绘制的屏幕可见
        pygame.display.flip()

if __name__ == '__main__':
    # 创建游戏实例并以主程序方式运行
    ai = AlienInvasion()
    ai.run_game()