from statistics import mean

from pygame.constants import QUIT, KEYDOWN, K_UP, K_ESCAPE, K_SPACE, K_1

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

        # initialize some game variables
        self.upper_pipes = None
        self.lower_pipes = None
        self.pipe_vel_x = None
        self.ai_enabled = False

        # pygame code
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

    ''' main game logic here'''

    def main_game_loop(self):
        """
        Processes the main game logic in the loop.

        Returns: None.

        """
        self.create_pipes()

        while True:
            # handle input events
            for event in pygame.event.get():
                # game exit
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # flap players on keypress
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    self.map_players_to(Bird.flap)

                # enable the ai
                if event.type == KEYDOWN and event.key == K_1:
                    self.ai_enabled = not self.ai_enabled
                    print('AI enabled :', self.ai_enabled)

            # handle the AI logic
            self.map_players_to(Bird.ai)

            # check for crash
            self.map_players_to(Bird.check_crash)

            # check if we should disable birds that crashed
            self.map_players_to(Bird.handle_crash)

            # score the birds
            self.map_players_to(Bird.check_score)

            # rotate and move players
            self.map_players_to(Bird.animate_player)

            # move the pipes and create new ones if needed
            self.move_pipes()

            # render the background
            self.render_background()

            # render the score
            self.show_score()

            # render the player
            self.map_players_to(Bird.render_player_sprite)

            # pygame stuff
            FPSCLOCK.tick(FPS)
            pygame.display.update()

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
            self.map_players_to(Bird.animate_player_welcome_screen)

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

    ''' helper functions for main functions'''

    def render_background(self):
        """
        Draws the background and pipe sprites.
        Returns:

        """
        # draw sprites
        SCREEN.blit(IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(self.upper_pipes, self.lower_pipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

    def create_pipes(self):
        """
        Creates a list of upper and lower pipes and assigns them to the instance of the FlappyBirdGame object.

        Also communicates with the player population and sets the Bird class' pipes as well.
        Returns: In-place.

        """
        # get and add pipes to a list
        new_pipe_1 = get_random_pipe()
        new_pipe_2 = get_random_pipe()

        # list of upper pipes
        self.upper_pipes = [
            {'x': SCREENWIDTH + 200, 'y': new_pipe_1[0]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe_2[0]['y']},
        ]

        # list of lower pipes
        self.lower_pipes = [
            {'x': SCREENWIDTH + 200, 'y': new_pipe_1[1]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': new_pipe_2[1]['y']},
        ]

        # communicate with Bird class
        Bird.lower_pipes = self.lower_pipes
        Bird.upper_pipes = self.upper_pipes

    def move_pipes(self):
        """
        Appears to move the pipes left. Will add new ones if they go off-screen.
        Returns:

        """
        # move pipes to left
        for uPipe, lPipe in zip(self.upper_pipes, self.lower_pipes):
            uPipe['x'] += self.pipe_vel_x
            lPipe['x'] += self.pipe_vel_x

        # add new pipes as required
        self.add_new_pipes()

    def add_new_pipes(self):
        """
        Adds new pipes if they disappear off-screen.
        Returns:

        """
        # add new pipe when first pipe is about to touch left of screen
        if 0 < self.upper_pipes[0]['x'] < 5:
            newPipe = get_random_pipe()
            self.upper_pipes.append(newPipe[0])
            self.lower_pipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if self.upper_pipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            self.upper_pipes.pop(0)
            self.lower_pipes.pop(0)

    def map_players_to(self, func):
        """
        Maps a given function to the entire player population. May help organize things better. (Bascially a wrapper)/
        Args:
            func: function to map over the player population.

        Returns: population after modification. Will not apply changes in-place.

        """
        return map(func, self.players)

    def show_score(self):
        """
        Renders the score to the game screen.
        Returns:

        """
        # find the mean score of the population
        score = mean([x.score for x in self.players])

        scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0  # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += IMAGES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - totalWidth) / 2

        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
            Xoffset += IMAGES['numbers'][digit].get_width()
