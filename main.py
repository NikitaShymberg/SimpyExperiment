import simpy
from Map import Map
from Peon import Peon
from Point import Point
import random

NUM_PEONS = 5  # The number of Peons at the start of the simulation
WIDTH = 600  # The number of columns in the map
HEIGHT = 400  # The number of rows in the map

if __name__ == '__main__':
    env = simpy.Environment()
    my_map = Map(600, 400, env)
    for i in range(NUM_PEONS):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        peon = Peon(env, my_map, Point(x, y, my_map))
        my_map.add_sprite(peon)
    env.run(until=5000)
    # TODO: print out some stats here or something
