"""
This is the map that everything happens on
"""
import numpy as np
from utils import Point
from Food import Food
# from Sprite import Sprite


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sprites = np.zeros((height, width), dtype=object)
        self.sprites[:, :] = None
        self.foods = []

    def add_sprite(self, sprite):
        if isinstance(sprite, Food):
            self.foods.append(sprite)
        self.sprites[sprite.position.y][sprite.position.x] = sprite

    def delete_sprite(self, sprite):
        if isinstance(sprite, Food):
            self.foods.remove(sprite)
        self.sprites[sprite.position.y][sprite.position.x] = None

    def at(self, point):
        return self.sprites[point.y, point.x]

    def move(self, thing, location):
        """
        Moves the `thing` sprite to the given location.
        """
        self.sprites[thing.position.y, thing.position.x] = None
        self.sprites[location.y, location.x] = thing
        thing.position = location
