import os
import sys

import pygame

"""
Define constants that are singular numbers here.
"""
time_mult = 150
FPS = 30 * time_mult  # (30) framerate. Changing this will mess with game speed.
SCREENWIDTH = int(288 * 1)  # (288) size of screen. Changing it doesn't scale the game automatically.
SCREENHEIGHT = 512  # (512) size of screen. Changing it doesn't scale the game automatically.
PIPE_GAP_SIZE = 120  # (100) gap between upper and lower part of pipe
BASE_Y = SCREENHEIGHT * 0.79  # (* 0.79) min height for the screen to render pipes.

"""
Load in assets into dictionaries here.
"""
IMAGES, SOUNDS, HIT_MASKS = {}, {}, {}

genomes_to_run = None
conf = None
render_all = False
debug_circle = 0, 0


# numbers sprites for score display
def load_assets():
    """
    Load both sounds and images into the appropriate dictionaries.
    :return: None.
    """
    load_images(), load_sound()


def load_images():
    """
    Load image assets into global images dictionary.
    :return: None.
    """
    global IMAGES

    IMAGES['numbers'] = (
        pygame.image.load('FlapPyBird/assets/sprites/0.png').convert_alpha(),
        pygame.image.load('FlapPyBird/assets/sprites/1.png').convert_alpha(),
        pygame.image.load('FlapPyBird/assets/sprites/2.png').convert_alpha(),
        pygame.image.load('FlapPyBird/assets/sprites/3.png').convert_alpha(),
        pygame.image.load('FlapPyBird/assets/sprites/4.png').convert_alpha(),
        pygame.image.load('FlapPyBird/assets/sprites/5.png').convert_alpha(),
        pygame.image.load('FlapPyBird/assets/sprites/6.png').convert_alpha(),
        pygame.image.load('FlapPyBird/assets/sprites/7.png').convert_alpha(),
        pygame.image.load('FlapPyBird/assets/sprites/8.png').convert_alpha(),
        pygame.image.load('FlapPyBird/assets/sprites/9.png').convert_alpha()
    )

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('FlapPyBird/assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('FlapPyBird/assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('FlapPyBird/assets/sprites/base.png').convert_alpha()


def load_sound():
    """
    Loads sounds into the global sounds dictionary.
    :return: None.
    """
    global SOUNDS
    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die'] = pygame.mixer.Sound('FlapPyBird/assets/audio/die' + soundExt)
    SOUNDS['hit'] = pygame.mixer.Sound('FlapPyBird/assets/audio/hit' + soundExt)
    SOUNDS['point'] = pygame.mixer.Sound('FlapPyBird/assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('FlapPyBird/assets/audio/swoosh' + soundExt)
    SOUNDS['wing'] = pygame.mixer.Sound('FlapPyBird/assets/audio/wing' + soundExt)


# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'FlapPyBird/assets/sprites/redbird-upflap.png',
        'FlapPyBird/assets/sprites/redbird-midflap.png',
        'FlapPyBird/assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        'FlapPyBird/assets/sprites/bluebird-upflap.png',
        'FlapPyBird/assets/sprites/bluebird-midflap.png',
        'FlapPyBird/assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'FlapPyBird/assets/sprites/yellowbird-upflap.png',
        'FlapPyBird/assets/sprites/yellowbird-midflap.png',
        'FlapPyBird/assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'FlapPyBird/assets/sprites/background-day.png',
    'FlapPyBird/assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'FlapPyBird/assets/sprites/pipe-green.png',
    'FlapPyBird/assets/sprites/pipe-red.png',
)
