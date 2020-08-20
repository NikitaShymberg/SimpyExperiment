"""
A character that walks around and eats food
"""
from Point import Point
from utils import shortest_path, distance_between, Actions
from Sprite import Sprite
import numpy as np
import random


class Peon(Sprite):
    """
    The main character of the simulation.
    Walks to the nearest food and tries to eat before it dies.
    If the Peon eats enough, it will mitose and spawn another Peon next to itself.
    """
    def __init__(self, env, my_map, position=Point(0, 0)):
        super().__init__(env, my_map, position)
        self.stats = {
            'mitosis_progress': 0,  # The current mitosis juice level
            'mitosis_efficiency': 0.5,  # The efficiency with which filling is converted to mitosis juice
            'mitosis_threshold': 500,  # The amount of mitosis juice required to mitose
            'speed': 1,  # The number of tiles it moves per time
            'max_child_difference': 0.05,  # The maximum percentage a child's stats may differ by
        }  # The characteristics of this Peon
        self.hunger = 250  # The initial hunger value, if this reaches 0 the Peon dies
        self.destination = None  # The current place that the Peon walks to
        self.is_alive = True
        self.action = [self.env.process(self.simulate_events()), self.env.process(self.simulate_hunger())]

    def find_food(self):
        """
        Returns the nearest food or None if none found.
        """
        if self.map.foods == []:
            return None

        distances = [distance_between(self.position, food.position)
                     for food in self.map.foods]

        return self.map.foods[np.argmin(distances)]

    def determine_action(self):
        """
        Determines the next action to take at this timestep.
        Returns a method to run.
        """
        if self.hunger <= 0:
            return self.die
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
        """
        Moves towards `self.destination` at the rate specified by `self.stats['speed']`
        """
        have_stepped = False
        # Walk
        for step in range(round(self.stats['speed'])):
            if self.destination is not None:
                next_point = shortest_path(self.position, self.destination)
                self.map.move(self, next_point)
                have_stepped = True

        # Log things
        if have_stepped:
            self.print(Actions.Walked.name)
        else:
            self.print(Actions.NoAction.name)
        return self.env.timeout(1)

    def mitose(self):
        """
        Makes a slightly altered copy of the Peon.
        Spawns the child Peon on a random adjacent point.
        If all adjacent points are full, the child is killed.
        """
        child_stats = {}
        for stat in self.stats:
            coin_flip = 1 if random.random() < 0.5 else - 1
            percent_change = 1 + coin_flip * (random.random() * self.stats['max_child_difference'])
            child_stats[stat] = self.stats[stat] * percent_change

        available_spawns = self.position.get_adjacent()
        if available_spawns is not None:
            spawn = random.choice(available_spawns)
        else:
            spawn = None  # The child must die

        self.print(Actions.Mitosed.name)
        child = Peon(self.env, self.map, spawn)
        child.stats = child_stats

        if child.position is None:  # No valid spawns for the child
            child.die()

    def die(self):
        """
        Removes the Peon from the map.
        """
        self.is_alive = False
        self.print(Actions.Died.name)
        self.map.delete_sprite(self)
        return self.env.timeout(0)

    def eat(self):
        """
        Eats a food.
        If enough food has been eaten, spawns a child Peon nearby.
        """
        my_food = self.find_food()
        if my_food is not None:
            self.hunger += my_food.filling
            self.print(Actions.Ate.name)
            self.stats['mitosis_progress'] += my_food.filling * self.stats['mitosis_efficiency']
            if self.stats['mitosis_progress'] >= self.stats['mitosis_threshold']:
                self.mitose()
            my_food.existance.interrupt()
        self.destination = None
        return self.env.timeout(1)

    def simulate_hunger(self):
        """
        A simulation method that decrements `self`'s hunger value.
        BUG: Sometimes when a Peon starves to death it doesn't call self.die
        """
        while self.is_alive:
            self.hunger -= 1
            yield self.env.timeout(1)

    def simulate_events(self):
        """
        The main simulation method.
        Chooses an action and does it.
        """
        while self.is_alive:
            action = self.determine_action()
            yield action()
