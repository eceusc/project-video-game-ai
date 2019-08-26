import random
from itertools import cycle
from pprint import pformat

from FlapPyBird.constants import *


class Bird:
    """
    Defines a single bird for the flappy bird AI. Instance this class to create a population.
    """
    num_birds = 0
    ''' stores default values for all the fields'''
    default_player_values = {
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
        'pos_x'           : SCREENWIDTH // 2,  # starting position, center screen
        'pos_y'           : SCREENHEIGHT // 2,  # starting position, center screen
        'loop_iter'       : 0,  # Used to change player_index after every 5th frame
        'player_index'    : 0,  # index of which player image to render
        'player_index_gen': cycle([0, 1, 2, 1]),  # cycle to animate the images
        'shm'             : {'val': 0, 'dir': 1},  # object to track motion of bird
        'movement_info'  : None, # TODO
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
        pass

    @staticmethod
    def random_height():
        """
        Finds a random spawn height for the bird. Automatically takes screen height into consideration.
        :return: As above.
        """
        # will pick a number in this interval, so that the bird doesnt spawn absolutely at the edges of the screen.
        interval = [0.2, 0.8]
        return int(SCREENHEIGHT * random.uniform(*interval))

    @staticmethod
    def check_crash():
        """
        Checks if there was a crash with pipes for the current bird.
        Returns: [crash_pipe, crash_ground].

        """
        # check if the bird is aware of the pipes

        assert Bird.upper_pipes is not None and Bird.lower_pipes is not None, 'Set a reference to the pipes after ' \
                                                                              'initializing the first bird'

        # player = self

    def simple_harmonic_motion(self):
        """
        Oscillates value of player SHM betweeen -8, 8.
        Returns: None, in-place modification of self.shm.

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
            playerIndex = next(self.player_index_gen)
        loopIter = (self.loop_iter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)

        pass
