from statistics import mean
from time import time
from itertools import cycle
from pprint import pformat, pprint

import neat

from FlapPyBird import constants
from FlapPyBird.helpers import *


# import keras

class Bird:
    """
    Defines a single bird for the flappy bird AI. Instance this class to create a population.
    """
    num_birds = 0
    ''' stores default values for all the fields'''
    default_player_values = {
        'score'           : 0,  # Number of pipes passed
        'vel_y'           : 0,  # Velocity along Y axis
        'max_vel_y'       : 20,  # Max descend speed
        'min_vel_y'       : -10,  # Max ascend speed
        'rot'             : 45,  # Rotation
        'rot_vel'         : 4,  # Rotation velocity
        'rot_thresh'      : 20,  # Rotation threshold
        'acc_flap'        : -12,  # Speed on flapping
        'acc_y'           : 3,  # Gravity/Downward acc
        'flapped'         : False,  # True when player flaps
        'ai_enabled'      : False,  # True if AI agent is playing the bird
        'pos_x'           : SCREENWIDTH * 0.2,  # starting position, left of screen
        'pos_y'           : SCREENHEIGHT // 2,  # starting position, center screen
        'loop_iter'       : 0,  # Used to change player_index after every 5th frame
        'player_index'    : 0,  # index of which player image to render
        'player_index_gen': cycle([0, 1, 2, 1]),  # cycle to animate the images
        'shm'             : {'val': 0, 'dir': 1},  # object to track motion of bird
        'base_x'          : 0,  # coordinate of base???
        'base_shift'      : -1,  # max shift amount
        'crash_test'      : (True, False),  # helps track if the bird crashed, and how
        'alive'           : True,  # helps track if the bird is alive in the population
        'last_flapped'    : time(),
        'winner'          : False,  # checks if current bird is the best. this is a flag to render.
    }

    lower_pipes = None
    upper_pipes = None

    @staticmethod
    def set_pipes(lower_pipes, upper_pipes):
        """
        Sets the Bird class's class variables to the pipes array from game. This is required for collision testing.
        Args:
            lower_pipes: array of lower pipes
            upper_pipes: array of upper pipes

        Returns:
            None, adjusts in place
        """
        Bird.upper_pipes = upper_pipes
        Bird.lower_pipes = lower_pipes

    def set_instance_vars(self, new_vars=None):
        """
        Sets the object (Bird's) instance variables to new values. By default, sets the values to the default from
        the Github implementation.
        Args:
            new_vars: key-value pairs where keys are the instance variable names, and values are respective values.

        Returns:
            None, in-place.

        """
        if new_vars is None:
            new_vars = Bird.default_player_values

        vars(self).update(new_vars)

    def __init__(self):
        """
        Constructor for the class. Doesn't allow you to set values, see self.set_instance_variables instead.
        """
        # initialize a bird to default values.
        self.set_instance_vars()

        # randomize some parameters, such as starting height
        self.pos_y = self.random_height()

        # tag each bird

        self.identifier = Bird.num_birds

        # create ai net for each bird
        self.initialize_ai()

        # increment Bird counter
        Bird.num_birds += 1

        # remember time of birth
        self.birth_time = 0

    def __repr__(self):
        """
        String representation of the object.
        Returns: As above.

        """
        return pformat(vars(self))

    def flap(self):
        """
        Flaps the bird, if the bird hasn't already flapped.
        Returns: In-place.

        """

        if self.pos_y > -2 * IMAGES['player'][0].get_height():
            self.vel_y = self.acc_flap
            self.flapped = True
            self.last_flapped = time()

    @staticmethod
    def random_height():
        """
        Finds a random spawn height for the bird. Automatically takes screen height into consideration.
        Returns: [crash_pipe, crash_ground].
        """
        # will pick a number in this interval, so that the bird doesnt spawn absolutely at the edges of the screen.
        interval = [0.4, 0.5]
        return int(SCREENHEIGHT * random.uniform(*interval))

    def check_crash(self):
        """
        Checks if there was a crash with pipes for the current bird.
        Returns: [crash_pipe, crash_ground].

        """
        # check if the bird is aware of the pipes

        assert Bird.upper_pipes is not None and Bird.lower_pipes is not None, 'Set a reference to the pipes after ' \
                                                                              'initializing the first bird'

        # player = self
        player_index = self.player_index
        player_width = IMAGES['player'][0].get_width()
        player_height = IMAGES['player'][0].get_height()

        pos_y = self.pos_y
        pos_x = self.pos_x
        upper_pipes = self.upper_pipes
        lower_pipes = self.lower_pipes
        # if player crashes into ground

        if pos_y + player_height >= BASE_Y - 1:
            self.crash_test = True, True
            return

        else:
            player_rect = pygame.Rect(pos_x, pos_y, player_width, player_height)

            pipe_width = IMAGES['pipe'][0].get_width()
            pipe_height = IMAGES['pipe'][0].get_height()

            for uPipe, lPipe in zip(upper_pipes, lower_pipes):
                # upper and lower pipe rects
                u_pipe_rect = pygame.Rect(uPipe['x'], uPipe['y'], pipe_width, pipe_height)
                l_pipe_rect = pygame.Rect(lPipe['x'], lPipe['y'], pipe_width, pipe_height)

                # player and upper/lower pipe hitmasks
                p_hit_mask = HIT_MASKS['player'][player_index]
                u_hitmask = HIT_MASKS['pipe'][0]
                l_hitmask = HIT_MASKS['pipe'][1]

                # if bird collided with upipe or lpipe
                u_collide = pixel_collision(player_rect, u_pipe_rect, p_hit_mask, u_hitmask)
                l_collide = pixel_collision(player_rect, l_pipe_rect, p_hit_mask, l_hitmask)

                if u_collide or l_collide:
                    self.crash_test = True, False
                    return

        self.crash_test = False, False
        return

    def simple_harmonic_motion(self):
        """
        Oscillates value of player SHM between -8, 8.
        Returns: None, in-place modification of self.shm.

        Notes:
            self.shm:
            {
                'val' : value,
                'dir' : value,
            }
        """

        if abs(self.shm['val']) == 8:
            self.shm['dir'] *= -1
        if self.shm['dir'] == 1:
            self.shm['val'] += 1
        else:
            self.shm['val'] -= 1

    def animate_player(self):
        """
        Runs the player sprite through different stages of animation.
        Returns:

        """
        # playerIndex basex change
        if (self.loop_iter + 1) % 3 == 0:
            self.player_index = next(self.player_index_gen)
        self.loopIter = (self.loop_iter + 1) % 30
        self.base_x = -((-self.base_x + 100) % self.base_shift)

        # rotate the player
        if self.rot > -90:
            self.rot -= self.rot_vel

        # rotation has a threshold
        self.visible_rot = self.rot_thresh
        if self.rot <= self.rot_thresh:
            self.visible_rot = self.rot

        # player's movement
        if self.vel_y < self.max_vel_y and not self.flapped:
            self.vel_y += self.acc_y
        if self.flapped:
            self.flapped = False
            # more rotation to cover the threshold (calculated in visible rotation)
            self.rot = 45

        player_height = IMAGES['player'][self.player_index].get_height()
        self.pos_y += min(self.vel_y, BASE_Y - self.pos_y - player_height)

    def animate_player_welcome_screen(self):
        """
        Runs the player sprite through different stages of animation.
        Returns:

        """
        # adjust playery, playerIndex, basex
        if (self.loop_iter + 1) % 5 == 0:
            self.playerIndex = next(self.player_index_gen)
        self.loopIter = (self.loop_iter + 1) % 30
        self.base_x = -((-self.base_x + 4) % self.base_shift)
        self.simple_harmonic_motion()

    def render_player_sprite_no_transform(self):
        """
        Renders the players sprite to the SCREEN global variable. Is called to render the player on the welcome screen.
        Returns: None. Blits sprites.

        """

        Bird.SCREEN.blit(IMAGES['player'][self.player_index], (self.pos_x, self.pos_y + self.shm['val']))

        # todo may be rendering a shit ton of bases
        Bird.SCREEN.blit(IMAGES['base'], (self.base_x, BASE_Y))

    def render_player_sprite(self):
        """
        Renders the players sprite to the SCREEN global variable. Is called to render the player on the welcome screen.
        Returns: None. Blits sprites.

        """
        # dont render dead players
        if not self.alive:
            return

        # only render the base for the winner
        if self.winner:
            Bird.SCREEN.blit(IMAGES['base'], (self.base_x, BASE_Y))

        # if we dont want to render all, then only render the winner
        if not constants.render_all and not self.winner:
            return

        # if in the game, we can start doing the rotations
        player_surface = pygame.transform.rotate(IMAGES['player'][self.player_index], self.visible_rot)
        Bird.SCREEN.blit(player_surface, (self.pos_x, self.pos_y))

    def check_score(self):
        """
        Checks if the bird passed a pipe. If it did, it increment's that bird's score.
        Returns: In-place.

        """
        assert Bird.upper_pipes is not None and Bird.lower_pipes is not None, 'Set a reference to the pipes after ' \
                                                                              'initializing the first bird'

        if not self.alive:
            return

        player_width = IMAGES['player'][0].get_width() / 2
        player_mid_position = self.pos_x + player_width

        pipe_width = IMAGES['pipe'][0].get_width() / 2

        for pipe in self.upper_pipes:
            pipe_mid_position = pipe['x'] + pipe_width
            if pipe_mid_position <= player_mid_position < pipe_mid_position + 4:
                self.score += 1

    def handle_crash(self):
        """
        Handles crash condition if a bird dies.
        :return:
        """
        if self.crash_test[0]:
            # assert self.alive, 'Something is wrong, dead bird is dying again'
            self.alive = False
            # assign the fitness
            self.genome.fitness = self.get_fitness()
            self.crash_test = False, False

    ''' ai helper methods here'''

    def ai(self):
        """
        This function is called if the AI is enabled every game tick.
        Returns:

        """
        if not self.alive:
            return

        assert hasattr(self, 'net'), "Bird has ai enabled but does not appear to have any agents"

        self.birth_time += 1

        activation = self.net.activate(self.get_inputs())[0]

        # if activation > 1e3:
        #     print('unusually high activation of', activation)

        if activation > 0.9:
            self.flap()

    def initialize_ai(self):
        """
        Initializes the ai net for each bird according to configuration rules.
        Args:
            genomes: list of genomes for the population
            conf: configuration object for neat

        Returns:

        """

        self.gid, self.genome = constants.genomes_to_run[self.identifier]
        self.genome.fitness = -1
        self.net = neat.nn.FeedForwardNetwork.create(self.genome, constants.conf)
        # self.net = neat.nn.RecurrentNetwork
        # .create(self.genome, constants.conf)

    def get_inputs(self):
        """
        Gets inputs to run the ai.
        :return: dictionary of named inputs. Use .values() to get input values.
        If the bird is dead, then no inputs are received.
        """
        if not self.alive:
            return None

        # inputs = [self.get_next_pipe_midpoint() - self.pos_y] + self.distance_to_pipe()
        pipe_width = IMAGES['pipe'][0].get_width()

        inputs = list(self.midpoint_of_pipes()) + list(self.distance_to_pipe()) + [self.pos_y, self.vel_y,
                                                                                   self.acc_flap, self.rot]
        inputs = list(self.midpoint_of_pipes()) + list(self.distance_to_pipe()) + [self.pos_y, self.pos_x, self.vel_y,
                                                                                   self.rot,
                                                                                   time() - self.last_flapped]

        # inputs = list(self.midpoint_of_pipes()) + [self.pos_y]
        inputs[0] -= self.pos_y - 0.5 * PIPE_GAP_SIZE + 10
        inputs[0] -= self.pos_y - 0.5 * PIPE_GAP_SIZE + 10
        inputs[-1] *= 10  # convert time to 100ms scale

        # inputs = constants.midpt_1 + [self.pos_y, self.pos_x, self.vel_y, self.rot, time() - self.last_flapped]
        return inputs

    def distance_to_pipe(self):
        return self.upper_pipes[0]['x'] - self.pos_x, self.upper_pipes[1]['x'] - self.pos_x

    def midpoint_of_pipes(self):
        return Bird.lower_pipes[0]['y'] - 0.5 * PIPE_GAP_SIZE, Bird.lower_pipes[1]['y'] - 0.5 * PIPE_GAP_SIZE

    def get_next_pipe_index(self):
        up = Bird.upper_pipes

        dist = [x['x'] - self.pos_x for x in up]

        pipe_index = 0
        while dist[pipe_index] < 0:
            pipe_index += 1

        return pipe_index

    def get_next_pipe_midpoint(self):
        # find distances to all pipes
        up = Bird.upper_pipes

        pipe_index = self.get_next_pipe_index()

        # get midpoint of the pipes
        return Bird.lower_pipes[pipe_index]['y'] - 0.5 * PIPE_GAP_SIZE

    def get_fitness(self):
        """
        Define the fitness function here.
        Returns: real-valued number representing fitness.

        """
        score = self.score - (abs(self.distance_to_pipe()[0])) * 0.3
        score = self.score + 1.5 * 1e-3 * self.birth_time - (abs(self.distance_to_pipe()[0])) * 0.001
        score = self.birth_time * 3 - \
                (abs(Bird.lower_pipes[self.get_next_pipe_index()]['y'] - PIPE_GAP_SIZE // 2 - self.pos_y)) * 0.5
        pipe_width = IMAGES['pipe'][0].get_width()

        constants.debug_circle = Bird.lower_pipes[self.get_next_pipe_index()]['x'] + pipe_width // 1.2, \
                                 Bird.lower_pipes[
                                     self.get_next_pipe_index()]['y'] - PIPE_GAP_SIZE // 10
        constants.debug_circle = tuple(map(int, constants.debug_circle))
        # score *= 1e-1
        # score = self.score
        # if self.score > 1:
        #     print(score)

        score = self.birth_time * 3 - abs(constants.debug_circle[1] - self.pos_y) + 5 * self.score
        return score

    def mse(self, circle):
        return sum([(self.pos_x - circle[0]) ** 2, (self.pos_y - circle[1]) ** 2]) ** 0.5

    def create_sgd_net(self):
        num_inputs = 9
        num_ouputs = 1
