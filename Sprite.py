"""
This represents the super class of all the things that can be on the map.
"""
from Point import Point
from utils import Actions
import uuid


class Sprite:
    """
    An object that can be placed on a map. On its own a Sprite is nothing.
    Extend this class to create things to put on the map.
    """
    def __init__(self, env, my_map, position=Point(0, 0)):
        self.env = env  # The environment to simulate in
        self.map = my_map  # The map that the sprite is on
        self.position = position  # The current location of the Sprite
        self.id = uuid.uuid4()  # The Sprite's unique ID
        self.print(Actions.Spawned.name, type(self).__name__)

    def print(self, *args) -> None:
        """
        Prints out an event.
        This is used to create logs to display the simulation.
        """
        string = f'[{int(self.env.now)} | {self.id} | {self.position}]'  # TODO: not sure if the int here is correct
        print(string, *args)

    def __eq__(self, other):
        """
        A sprite is equal to another if their ids are the same.
        """
        return self.id == other.id
