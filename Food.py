"""
A Sprite that can be eaten
"""
from utils import Point, Actions
from Sprite import Sprite
import simpy


class Food(Sprite):
    def __init__(self, env, my_map, position=Point(0, 0), expiration=500):
        super().__init__(env, my_map, position)
        self.filling = 100  # The amount of hunger this food restores
        self.expiration = expiration
        self.existance = self.env.process(self.run())

    def run(self):
        try:
            yield self.env.timeout(self.expiration)
            self.print(Actions.Expired.name)
        except simpy.Interrupt:
            self.print(Actions.Eaten.name)
        self.map.delete_sprite(self)
