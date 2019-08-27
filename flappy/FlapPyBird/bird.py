from itertools import cycle
from pprint import pformat

from FlapPyBird.helpers import *


class Bird:
    """
    Defines a single bird for the flappy bird AI. Instance this class to create a population.
    """
    num_birds = 0
    ''' stores default values for all the fields'''
    default_player_values = {
        'score'           : 0,  # Number of pipes passed
        'vel_y'           : -9,  # Velocity along Y axis
        'max_vel_y'       : 10,  # Max descend speed
        'min_vel_y'       : -8,  # Max ascend speed
        'rot'             : 45,  # Rotation
        'rot_vel'         : 3,  # Rotation velocity
        'rot_thresh'      : 20,  # Rotation threshold
        'acc_flap'        : -9,  # Speed on flapping
        'acc_y'           : 1,  # Gravity/Downward acc
        'flapped'         : False,  # True when player flaps
        'ai_enabled'      : False,  # True if AI agent is playing the bird
        'pos_x'           : SCREENWIDTH * 0.2,  # starting position, left of screen
        'pos_y'           : SCREENHEIGHT // 2,  # starting position, center screen
        'loop_iter'       : 0,  # Used to change player_index after every 5th frame
        'player_index'    : 0,  # index of which player image to render
        'player_index_gen': cycle([0, 1, 2, 1]),  # cycle to animate the images
        'shm'             : {'val': 0, 'dir': 1},  # object to track motion of bird
        'base_x'          : 0,  # coordinate of base???
        'base_shift'      : IMAGES['base'].get_width() - IMAGES['background'].get_width(),  # max shift amount
        'crash_test'      : (True, False),  # helps track if the bird crashed, and how
        'alive'           : True,  # helps track if the bird is alive in the population

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

        # increment Bird counter
        Bird.num_birds += 1

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

    @staticmethod
    def random_height():
        """
        Finds a random spawn height for the bird. Automatically takes screen height into consideration.
        Returns: [crash_pipe, crash_ground].
        """
        # will pick a number in this interval, so that the bird doesnt spawn absolutely at the edges of the screen.
        interval = [0.2, 0.8]
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
            playerRect = pygame.Rect(pos_x, pos_y, player_width, player_height)

            pipe_width = IMAGES['pipe'][0].get_width()
            pipe_height = IMAGES['pipe'][0].get_height()

            for uPipe, lPipe in zip(upper_pipes, lower_pipes):
                # upper and lower pipe rects
                uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipe_width, pipe_height)
                lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipe_width, pipe_height)

                # player and upper/lower pipe hitmasks
                pHitMask = HIT_MASKS['player'][player_index]
                uHitmask = HIT_MASKS['pipe'][0]
                lHitmask = HIT_MASKS['pipe'][1]

                # if bird collided with upipe or lpipe
                uCollide = pixel_collision(playerRect, uPipeRect, pHitMask, uHitmask)
                lCollide = pixel_collision(playerRect, lPipeRect, pHitMask, lHitmask)

                if uCollide or lCollide:
                    self.crash_test = True, False
                    return

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
        # adjust playery, playerIndex, basex
        if (self.loop_iter + 1) % 5 == 0:
            self.playerIndex = next(self.player_index_gen)
        self.loopIter = (self.loop_iter + 1) % 30
        self.base_x = -((-self.base_x + 4) % self.base_shift)
        self.simple_harmonic_motion()

    def render_player_sprite(self):
        """
        Renders the players sprite to the SCREEN global variable. Is called to render the player on the welcome screen.
        Returns: None. Blits sprites.

        """
        global SCREEN
        SCREEN.blit(IMAGES['player'][self.player_index], (self.pos_x, self.pos_y + self.shm['val']))
        SCREEN.blit(IMAGES['base'], (self.base_x, BASE_Y))

    def check_score(self):
        """
        Checks if the bird passed a pipe. If it did, it increment's that bird's score.
        Returns: In-place.

        """
        assert Bird.upper_pipes is not None and Bird.lower_pipes is not None, 'Set a reference to the pipes after ' \
                                                                              'initializing the first bird'

        player_width = IMAGES['player'][0].get_width() / 2
        player_mid_position = self.pos_x + player_width

        pipe_width = IMAGES['pipe'][0].get_width() / 2

        for pipe in self.upper_pipes:
            pipe_mid_position = pipe['x'] + pipe_width
            if pipe_mid_position <= player_mid_position < pipe_mid_position + 4:
                self.score += 1

    def ai(self):
        """
        This function is called if the AI is enabled every game tick.
        Returns:

        """
        # check if bird is dead. Dead ai doesn't work.
        pass

    def handle_crash(self):
        assert not self.alive, 'Something is wrong, dead bird is dying again'

