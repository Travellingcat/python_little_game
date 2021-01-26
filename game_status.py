
class GameStatus:
    '''跟踪游戏状态信息的类'''

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.game_active = True
        self.reset_status()


    def reset_status(self):
        self.ships_left = self.settings.ship_limit