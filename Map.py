"""
This is the map that everything happens on
"""
import numpy as np
from utils import Point
from Food import Food
import random
# from Sprite import Sprite


class Map:
    def __init__(self, width, height, env):
        self.width = width
        self.height = height
        self.env = env
        self.sprites = np.zeros((height, width), dtype=object)
        self.sprites[:, :] = None
        self.foods = []
        self.food_spawn_period_max = 10
        self.env.process(self.run())

    def add_sprite(self, sprite):
        if isinstance(sprite, Food):
            self.foods.append(sprite)
        self.sprites[sprite.position.y][sprite.position.x] = sprite

    def delete_sprite(self, sprite):
        if isinstance(sprite, Food):
            self.foods.remove(sprite)
        self.sprites[sprite.position.y][sprite.position.x] = None

    def run(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            f = Food(self.env, self, Point(x, y, self))
            self.add_sprite(f)
            t = random.randint(0, self.food_spawn_period_max)
            yield self.env.timeout(t)

    def at(self, point):
        return self.sprites[point.y, point.x]

    def move(self, thing, location):
        """
        Moves the `thing` sprite to the given location.
        """
        self.sprites[thing.position.y, thing.position.x] = None
        self.sprites[location.y, location.x] = thing
        thing.position = location
