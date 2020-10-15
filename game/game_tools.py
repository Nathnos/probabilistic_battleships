"""
Helping game functions
"""

import sys
import random


def get_direction(direction):
    if direction == "left":
        return -1, 0
    elif direction == "right":
        return 1, 0
    elif direction == "top":
        return 0, -1
    elif direction == "bottom":
        return 0, 1
    elif direction == "horizontal":
        return get_direction("right")
    elif direction == "vertical":
        return get_direction("bottom")
    else:
        print("Error : Can't resolve direction :", direction, file=sys.stderr)


def get_boat_size(boat):
    if boat == 1:
        return 5
    elif boat == 2:
        return 4
    elif boat == 3:
        return 3
    elif boat == 4:
        return 3
    elif boat == 5:
        return 2
    else:
        print("Error : Can't resolve boat :", boat, file=sys.stderr)


def get_random_direction(to_int=False):
    direction = random.choice(["horizontal", "vertical"])
    if to_int:
        return get_direction(direction)
    return direction


def get_random_player():
    return random.choice([1, 2])


def get_random_position():
    return random.randint(0, 9), random.randint(0, 9)
