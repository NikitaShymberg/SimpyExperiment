"""
Useful classes/funcitons for the whole program.
A.k.a I didn't know where to put something, so I put it here.
"""
import enum
from Point import Point


def shortest_path(start, finish):
    """
    Returns the next point to go to to reach `finish` from `start`.
    """
    if start.x < finish.x:
        return Point(start.x + 1, start.y, start.map)
    elif start.x > finish.x:
        return Point(start.x - 1, start.y, start.map)
    elif start.y < finish.y:
        return Point(start.x, start.y + 1, start.map)
    elif start.y > finish.y:
        return Point(start.x, start.y - 1, start.map)
    else:
        print('Warning: start and end points are the same!')
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
