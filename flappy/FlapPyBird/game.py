from pygame.constants import QUIT, KEYDOWN, K_UP, K_ESCAPE, K_SPACE

from FlapPyBird.bird import Bird
from FlapPyBird.helpers import *


class FlappyBirdGame:
    def __init__(self):
        """
            Sets up and runs the game.

            Initializes pygame, screen and assets.

            Shows welcome animation. On exit, launches main game loop.

            Finally handles endgame logic and restarts.

            """

        global SCREEN, FPSCLOCK

        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

        pygame.display.set_caption('Flappy Bird')

        load_assets()

        # start the game loops
        while True:
            # select random assets
            randomize_assets()

            self.welcome_screen()
            self.main_game_loop()
            self.game_over()

    def main_game_loop(self):
        """
        Processes the main game logic in the loop.

        Returns: None.

        """
        pass

    def map_players_to(self, func):
        """
        Maps a given function to the entire player population. May help organize things better. (Bascially a wrapper)/
        Args:
            func: function to map over the player population.

        Returns: population after modification. Will not apply changes in-place.

        """
        return map(func, self.players)

    def welcome_screen(self):
        """
        Shows the welcome animation and starts the bird populations.
        Returns: None.

        Note: this will most likely be removed in favor of training without interruptions.
        """
        # initialize player here

        self.players = [Bird()]

        message_x = int(SCREENWIDTH - IMAGES['message'].get_width()) / 2
        message_y = int(SCREENHEIGHT * 0.12)
        while True:
            # handle events, quitting and starting
            for event in pygame.event.get():

                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    self.map_players_to(add_shm_val_to_pos)
                    # in this case, start the game
                    break

            # handle animating the players
            self.map_players_to(Bird.animate_player)

            # handle rendering player sprites
            self.map_players_to(Bird.render_player_sprite)

            # handle rendering the background and message sprites
            SCREEN.blit(IMAGES['background'], (0, 0))
            SCREEN.blit(IMAGES['message'], (message_x, message_y))

            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def game_over(self):
        """
        Shows the game-over animation screen and ends the bird populations.
        Returns: None.

        Note: this will most likely be removed in favor of training without interruptions.
        """
        pass
