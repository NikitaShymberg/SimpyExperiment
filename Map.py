"""
This is the map that everything happens on
"""
import numpy as np
from Point import Point
from Food import Food
import random


class Map:
    """
    A map holds all the locations of all the simulated sprites.
    Spawns food sprites at a random interval.
    """
    def __init__(self, width, height, env):
        self.width = width  # The number of points in the x axis
        self.height = height  # The number of points in the y axis
        self.env = env  # The environment to use to run simulations
        self.sprites = np.zeros((height, width), dtype=object)
        self.sprites[:, :] = None  # A grid that holds the sprites on the map
        self.foods = []  # A list of all the existing food sprites
        self.food_spawn_period_max = 10  # The maximum amount of time to wait before spawning a new food
        self.env.process(self.simulate())

    def add_sprite(self, sprite):
        """
        Adds the given `sprite` to the map.
        """
        if isinstance(sprite, Food):
            self.foods.append(sprite)
        self.sprites[sprite.position.y][sprite.position.x] = sprite

    def delete_sprite(self, sprite):
        """
        Removes the given `sprite` from the map.
        """
        if isinstance(sprite, Food):
            self.foods.remove(sprite)
        self.sprites[sprite.position.y][sprite.position.x] = None

    def simulate(self):
        """
        The main simulation method.
        Waits a random period of time before spawning a food at a random location.
        The longest waiting time is specified by self.food_spawn_period_max.
        """
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            f = Food(self.env, self, Point(x, y, self))
            self.add_sprite(f)
            t = random.randint(0, self.food_spawn_period_max)
            yield self.env.timeout(t)

    def at(self, point):
        """
        Returns the sprite at the given `point`.
        """
        return self.sprites[point.y, point.x]

    def move(self, sprite, location):
        """
        Moves the `sprite` to the given `location`.
        """
        self.sprites[sprite.position.y, sprite.position.x] = None
        self.sprites[location.y, location.x] = sprite
        sprite.position = location
