import simpy
import numpy as np
import random
from Map import Map
from Peon import Peon
from Food import Food
from utils import Point


my_map = Map(600, 400)
env = simpy.Environment()
p1 = Peon(env, my_map, Point(0, 0, my_map))
my_map.add_sprite(p1)
for i in range(200):
    x = random.randint(0, 599)
    y = random.randint(0, 399)
    f = Food(env, my_map, Point(x, y, my_map))
    my_map.add_sprite(f)

env.run(until=2000)
