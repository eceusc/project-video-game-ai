import random

from FlapPyBird.constants import *


def pixel_collision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False


def get_hitmask(image):
    """returns a hit mask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


def select_random_player():
    """
    Loads in a random player sprite into the IMAGES[player] asset.
    Returns: In-place.

    """
    # select random player sprites
    randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
    IMAGES['player'] = (
        pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
        pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
    )


def select_random_pipe():
    """
    Loads in a random pipe sprite into the IMAGES[pipe] asset.
    Returns: In-place.

    """
    # select random pipe sprites
    pipe_index = random.randint(0, len(PIPES_LIST) - 1)

    IMAGES['pipe'] = (
        pygame.transform.flip(
            pygame.image.load(PIPES_LIST[pipe_index]).convert_alpha(), False, True),
        pygame.image.load(PIPES_LIST[pipe_index]).convert_alpha(),
    )


def select_random_background():
    """
    Loads in a random background into the IMAGES[backgrounds] asset.
    Returns: In-place.

    """
    # select random background sprites
    randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
    IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()


def populate_hitmasks():
    """
    Loads in hitmasks for the pipe and player objects.
    Returns: In-place.

    """
    # hit mask for pipes
    HIT_MASKS['pipe'] = (
        get_hitmask(IMAGES['pipe'][0]),
        get_hitmask(IMAGES['pipe'][1]),
    )

    # hit mask for player
    HIT_MASKS['player'] = (
        get_hitmask(IMAGES['player'][0]),
        get_hitmask(IMAGES['player'][1]),
        get_hitmask(IMAGES['player'][2]),
    )


def randomize_assets():
    """
    Loads in random assets for the pipe and player into the Images[pipe] and Images[player] assets.
    Returns: In-place.

    """
    select_random_pipe()
    select_random_player()
    select_random_background()


def add_shm_val_to_pos(bird):
    """
    Helper function to increment shm val value of bird to its vertical position.
    Args:
        bird: bird to be passed in.

    Returns: In-place.

    """
    bird.pos_x += bird.shm['val']
