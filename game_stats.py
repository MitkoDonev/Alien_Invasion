class GameStats:
    # track statistics
    def __init__(self, ai_game):
        # initialize statistics
        self.settings = ai_game.settings
        self.reset_stats()

        # start in an active state
        self.game_active = True

        # high score should not be reset
        self.high_score = 0

    def reset_stats(self):
        # initialize stats that can change during game
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
