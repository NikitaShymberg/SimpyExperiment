"""
A basic "worker"
"""
from utils import Point, shortest_path, distance_between
from Sprite import Sprite
from Food import Food
import numpy as np
# TODO: something something pdb?


class Peon(Sprite):
    def __init__(self, env, my_map, position=Point(0, 0)):
        super().__init__(env, my_map, position)
        self.stats = {
            'mitosis_progress': 0,
            'mitosis_efficiency': 0.5,
            'mitosis_threshold': 300,
            'speed': 1,
        }
        self.hunger = 100  # TODO: decrement this at some rate maybe have a separate "process" for this actually
        self.destination = None
        self.action = self.env.process(self.run())

    def find_food(self):
        """
        Returns the nearest food or None if none found.
        TODO: test?
        """
        if self.map.foods == []:
            return None

        distances = [distance_between(self.position, food.position)
                     for food in self.map.foods]

        return self.map.foods[np.argmin(distances)]

    def determine_action(self):
        if self.destination is None or self.position != self.destination:
            food = self.find_food()
            if food is not None:
                self.destination = food.position
            else:
                self.destination = None
            return self.walk
        if self.position == self.destination:
            return self.eat

        return self.walk

    def walk(self):
        if self.destination is not None:
            next_point = shortest_path(self.position, self.destination)
            self.map.move(self, next_point)
            self.print('Walked')
        else:
            self.print('No destination, stood still')
        return self.env.timeout(self.stats['speed'])  # FIXME: this is backwards, at the moment the higher your speed, the longer you wait to walk

    def mitose(self):
        """
        Makes a slightly altered copy of the Peon
        """
        ...  # TODO: implement

    def eat(self):
        my_food = self.find_food()
        self.hunger += my_food.filling
        self.stats['mitosis_threshold'] += my_food.filling * self.stats['mitosis_efficiency']
        if self.stats['mitosis_progress'] >= self.stats['mitosis_threshold']:
            self.mitose()
        self.destination = None
        self.print('Ate')
        my_food.existance.interrupt()
        return self.env.timeout(self.stats['speed'])  # FIXME: this is backwards, at the moment the higher your speed, the longer you wait to walk

    def run(self):
        # TODO: rename this probably
        while True:
            action = self.determine_action()
            yield action()
