import simpy
from Map import Map
from Peon import Peon
from Point import Point

if __name__ == '__main__':
    env = simpy.Environment()
    my_map = Map(600, 400, env)
    p1 = Peon(env, my_map, Point(0, 0, my_map))
    my_map.add_sprite(p1)
    env.run(until=20000)
