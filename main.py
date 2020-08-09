import simpy
import numpy as np
from Map import Map
from Peon import Peon
from Food import Food
from utils import Point


my_map = Map(600, 400)
env = simpy.Environment()
p1 = Peon(env, my_map, Point(0, 0, my_map))
p2 = Peon(env, my_map, Point(20, 20, my_map))
p3 = Peon(env, my_map, Point(40, 40, my_map))
f1 = Food(env, my_map, Point(5, 5, my_map))
my_map.add_sprite(p1)
my_map.add_sprite(p2)
my_map.add_sprite(p3)
my_map.add_sprite(f1)
env.run(until=15)
