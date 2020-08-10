import simpy
import numpy as np
from Map import Map
from Peon import Peon
from Food import Food
from utils import Point


my_map = Map(600, 400)
env = simpy.Environment()
p1 = Peon(env, my_map, Point(0, 0, my_map))
f1 = Food(env, my_map, Point(5, 5, my_map))
f2 = Food(env, my_map, Point(5, 6, my_map))
f3 = Food(env, my_map, Point(5, 7, my_map))
f4 = Food(env, my_map, Point(6, 5, my_map))
my_map.add_sprite(p1)
my_map.add_sprite(f1)
my_map.add_sprite(f2)
my_map.add_sprite(f3)
my_map.add_sprite(f4)
env.run(until=25)
