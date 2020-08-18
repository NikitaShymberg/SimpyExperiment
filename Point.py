class Point:
    """
    A single point on the map.
    """
    def __init__(self, x, y, my_map=None):
        self.x = x  # The column of this point's location
        self.y = y  # The row of this point's location
        self.map = my_map  # The map where this point is

    def get_adjacent(self):
        """
        Returns a list of the adjacent points to this point
        """
        if self.map is None:
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
        """
        Returns the point's coordinates as a (x, y) tuple.
        """
        return (self.x, self.y)

    def __repr__(self):
        return f"({self.x:3}, {self.y:3})"

    def __eq__(self, other):
        """
        Two points are equal if they have the same coordinates.
        """
        return self.x == other.x and self.y == other.y
