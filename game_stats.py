class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start game is an inactive state
        self.game_active = False

        self.score = 0

        # High scores
        self.first_place = 0
        self.second_place = 0
        self.third_place = 0
        self.read_highscore()

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def read_highscore(self):
        """Reads in numbers from highscores.txt"""
        file = open("highscores.txt", "r")
        self.first_place = int(file.readline())
        self.second_place = int(file.readline())
        self.third_place = int(file.readline())
        file.close()
