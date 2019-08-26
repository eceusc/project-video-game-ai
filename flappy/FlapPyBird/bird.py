from pprint import pformat
from FlapPyBird.constants import *




class Bird:
    """
    Defines a single bird for the flappy bird AI. Instance this class to create a population.
    """
    num_birds = 0
    ''' stores default values for all the fields'''
    default_player_values = {
        'vel_y'      : -9,  # Velocity along Y axis
        'max_vel_y'  : 10,  # Max descend speed
        'min_vel_y'  : -8,  # Max ascend speed
        'acc_y'      : 1,  # Gravity/Downward acc
        'rot'        : 45,  # Rotation
        'vel_rot'    : 3,  # Rotation velocity
        'rot_thresh' : 20,  # Rotation threshold
        'flap_acc'   : -9,  # Speed on flapping
        'flapped'    : False,  # True when player flaps
        'ai_enabled' : False,  # True if AI agent is playing the bird
        'pos_x'      : SCREENWIDTH // 2,  # starting position, center screen
        'pos_y'      : SCREENHEIGHT // 2,  # starting position, center screen

    }

    lower_pipes = None
    upper_pipes = None

    def set_pipes(self, lower_pipes, upper_pipes):
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

    def __repr__(self):
        """
        String representation of the object.
        Returns: As above.

        """
        return pformat(vars(self))

    def flap(self):
        pass

    def random_height(self):
        """
        Finds a random spawn height for the bird. Automatically takes screen height into consideration.
        :return:
        """
        pass

    def check_crash(self):
        """
        Checks if there was a crash with pipes for the current bird.
        Returns: [crash_pipe, crash_ground].

        """
        # check if the bird is aware of the pipes

        assert Bird.upper_pipes is not None and Bird.lower_pipes is not None, 'Set a reference to the pipes after ' \
                                                                              'initializing the first bird'

        # player = self