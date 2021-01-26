import pygame
class Gameover:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('images/gameover.jpg')
        self.rect = self.image.get_rect()
        self.rect.midtop = self.screen_rect.midtop

    def blitme(self):
        '''在指定的位置绘制图像'''
        self.screen.blit(self.image, self.rect)