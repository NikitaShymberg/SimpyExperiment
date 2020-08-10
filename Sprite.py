"""
This represents the super class of all the things that can be on the map.
"""
from utils import Point
import uuid


class Sprite:
    def __init__(self, env, my_map, position=Point(0, 0)):
        self.env = env
        self.map = my_map
        self.position = position
        self.id = uuid.uuid4()
        self.print('Spawned', type(self).__name__)

    def print(self, *args) -> None:
        string = f'[{int(self.env.now)} | {self.id} | {self.position}]'  # TODO: not sure if the int here is correct
        print(string, *args)

    def __eq__(self, other):
        return self.id == other.id
