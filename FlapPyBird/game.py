from pygame.constants import QUIT, KEYDOWN, K_UP, K_ESCAPE, K_SPACE, K_1

from FlapPyBird.bird import Bird
from FlapPyBird.helpers import *
from FlapPyBird import constants


def debugger(param):
    return
    print([x.alive for x in param['self'].players])


class FlappyBirdGame:
    """
    This class runs an instance of the flappy bird game.
    """
    population_size = -1  # should be set in init, this val should cause an error
    genomes = None

    def __init__(self, genomes):
        """
            Sets up and runs the game.

            Initializes pygame, screen and assets.

            Shows welcome animation. On exit, launches main game loop.

            Finally handles endgame logic and restarts.

            """

        global SCREEN, FPSCLOCK

        # enable ai here
        self.ai_enabled = True

        # initialize some game variables
        self.upper_pipes = None
        self.lower_pipes = None
        self.pipe_vel_x = -4

        constants.genomes_to_run = genomes
        FlappyBirdGame.population_size = len(genomes)

        # initialize players
        self.players = [Bird() for _ in range(FlappyBirdGame.population_size)]

        # pygame code
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        # send the screen to Bird for rendering
        Bird.SCREEN = SCREEN

        pygame.display.set_caption('Flappy Bird')

        load_assets()

        # start the game loops (for now, loop should only execute once)
        while True:
            # select random assets
            randomize_assets()

            # generate hitmasks
            populate_hitmasks()

            # self.welcome_screen()
            self.main_game_loop()

            # when game is over, reset the state
            FlappyBirdGame.reset_state()
            break
            # self.game_over()

    ''' main game logic here'''

    def main_game_loop(self):
        """
        Processes the main game logic in the loop.

        Returns: None.

        """
        # set the base shift
        self.base_shift = IMAGES['base'].get_width() - IMAGES['background'].get_width()
        self.create_pipes()

        while True:

            debugger(locals())

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
            if self.ai_enabled: self.map_players_to(Bird.ai)

            # check for crash
            self.map_players_to(Bird.check_crash)

            # check if we should disable birds that crashed
            self.map_players_to(Bird.handle_crash)

            # if all birds are dead then end the game
            if all(self.map_players_to(lambda x: not x.alive)):
                return

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

            # render the number alive
            # print('Num_alive', self.num_alive())

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
                    return

            # handle animating the players
            self.map_players_to(Bird.animate_player_welcome_screen)

            # handle rendering player sprites
            self.map_players_to(Bird.render_player_sprite_no_transform)

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

    def map_players_to(self, func, data=None):
        """
        Maps a given function to the entire player population. May help organize things better. (Bascially a wrapper)/
        Args:
            data: extra function arguments to pass. Currently only one arg supported.
            func: function to map over the player population.

        Returns: population after modification. Will not apply changes in-place.

        """
        if data is not None:
            assert len(data) == len(self.players), "Not enough extra arguments for entire population"
            return list((map(func, zip(self.players, data))))
        return list((map(func, self.players)))

    def show_score(self):
        """
        Renders the score to the game screen.
        Returns:

        """
        # find the mean score of the population
        score = max([x.score for x in self.players])

        score_digits = [int(x) for x in list(str(score))]
        total_width = 0  # total width of all numbers to be printed

        for digit in score_digits:
            total_width += IMAGES['numbers'][digit].get_width()

        x_offset = (SCREENWIDTH - total_width) / 2

        for digit in score_digits:
            SCREEN.blit(IMAGES['numbers'][digit], (x_offset, SCREENHEIGHT * 0.1))
            x_offset += IMAGES['numbers'][digit].get_width()

    ''' ai logic here'''

    def map_population_to_genome(self, genome):
        """
        Takes in a population of birds and maps it to a genome.
        Args:
            genome:

        Returns:

        """
        pass

    @classmethod
    def reset_state(cls):
        # reset the bird class vars
        Bird.num_birds = 0
        Bird.lower_pipes = None
        Bird.upper_pipes = None

    def num_alive(self):
        return sum([1 if x.alive else 0 for x in self.players])
