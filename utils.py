"""
Useful classes/funcitons for the whole program.
A.k.a I didn't know where to put something, so I put it here.
"""
import enum
import random
from Point import Point


def shortest_path(start, finish):
    """
    Returns the next point to go to to reach `finish` from `start`.
    """
    d_x = finish.x - start.x
    d_y = finish.y - start.y

    d_x = min(max(d_x, -1), 1)  # -1, 0, or 1
    d_y = min(max(d_y, -1), 1)

    if d_x == 0 and d_y != 0:  # Move in y direction
        return Point(start.x, start.y + d_y, start.map)
    elif d_x != 0 and d_y == 0:  # Move in x direction
        return Point(start.x + d_x, start.y, start.map)
    elif d_x != 0 and d_y != 0:  # Move in a random direction
        coin_flip = random.randint(0, 1)
        if coin_flip == 0:
            d_x = 0
        else:
            d_y = 0
        return Point(start.x + d_x, start.y + d_y, start.map)
    else:
        # print('Warning: start and end points are the same!')
        return start


def distance_between(p1, p2):
    """
    Returns the distance between two given points
    """
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


class Actions(enum.Enum):
    """
    All the available actions that can be taken by Sprites.
    """
    Spawned = 0
    Walked = 1
    Ate = 2
    Eaten = 3
    Mitosed = 4
    Died = 5
    Expired = 6
    NoAction = -1
