import simpy
import numpy as np
import random
from Map import Map
from Peon import Peon
from Food import Food
from utils import Point


env = simpy.Environment()
my_map = Map(600, 400, env)
p1 = Peon(env, my_map, Point(0, 0, my_map))
my_map.add_sprite(p1)

env.run(until=20000)
