"""
Useful funcitons/classes for the whole program
"""


class Point:
    def __init__(self, x, y, my_map=None):
        self.x = x
        self.y = y
        self.map = my_map

    def get_adjacent(self):
        """
        Returns the adjacent points to this point
        """
        if self.map is None:
            # TODO: handle this
            print('ERROR: point not attached to a map')
            return None

        adjacent = []
        max_w = self.map.width
        max_h = self.map.height
        if self.x != 0:
            adjacent.append(Point(self.x - 1, self.y, self.map))
        if self.x != max_w - 1:
            adjacent.append(Point(self.x + 1, self.y, self.map))
        if self.y != 0:
            adjacent.append(Point(self.x, self.y - 1, self.map))
        if self.y != max_h - 1:
            adjacent.append(Point(self.x, self.y + 1, self.map))

        return adjacent

    def as_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"({self.x:3}, {self.y:3})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def shortest_path(start: Point, finish: Point) -> Point:
    """
    Returns the next point to go to.
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


def distance_between(p1: Point, p2: Point):
    """
    Returns the distance between two given points
    """
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)
