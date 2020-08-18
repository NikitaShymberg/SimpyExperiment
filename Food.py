"""
A Sprite that can be eaten
"""
from Point import Point
from utils import Actions
from Sprite import Sprite
import simpy


class Food(Sprite):
    """
    A food thing that can be eaten by a Peon.
    """
    def __init__(self, env, my_map, position=Point(0, 0), expiration=500):
        super().__init__(env, my_map, position)
        self.filling = 100  # The amount of hunger this food restores
        self.expiration = expiration  # The time before the food expires and disappears
        self.existance = self.env.process(self.simulate())

    def simulate(self):
        """
        The main simulation method.
        Waits until this food expires, then deletes itself.
        If the process is interrupted the food is "eaten" and also deletes itself.
        """
        try:
            yield self.env.timeout(self.expiration)
            self.print(Actions.Expired.name)
        except simpy.Interrupt:  # Someone ate me
            self.print(Actions.Eaten.name)
        self.map.delete_sprite(self)
