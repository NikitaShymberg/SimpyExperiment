import re
import numpy as np
import cv2
from utils import Point, Actions


class Event():
    def __init__(self, log_string):
        """
        Black magic string parsing method to create an Event from a log entry.
        """
        match_string = r'\[([0-9]+) \| ([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}) \| \((\s*[0-9]+,\s*[0-9]+)\)\] ([\S\s]*)'
        groups = re.search(match_string, log_string).groups()
        self.time = int(groups[0])
        self.id = groups[1]
        x, y = int(groups[2].split()[0][:-1]), int(groups[2].split()[1])
        self.point = Point(x, y)
        for action in Actions:
            if groups[3].strip() == action.name:
                self.action = action
                break
        else:
            # Spawn because it is followed by what spawned
            self.action = Actions.Spawned
            self.sprite = groups[3][7:].strip()  # The type of sprite that was spawned

    def __repr__(self):
        return f'[{int(self.time)} | {self.id} | {self.point}] {self.action.name}'


class Display():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_time = 0
        self.img = np.zeros((height, width, 3))
        self.sprites = {}  # Keeps track of the sprite IDs, locations, and types
        self.sprite_colors = {
            'Peon': (255, 255, 255),
            'Food': (0, 0, 255),
            'Background': (0, 0, 0)
        }

    def read_log(self, path: str):
        for row in open(path):
            yield row

    def show(self):
        cv2.imshow('Simpy', self.img)
        cv2.waitKey(100)

    def run(self, path: str):
        """
        "main" function to run
        """
        prev_time = 0
        for entry in self.read_log(path):
            event = Event(entry)
            if event.time != prev_time:  # Show frame at time i
                self.show()
                prev_time = event.time
            self.process_event(event)

    def process_spawned_event(self, event):
        """
        Processes a "spawned" event.
        """
        self.sprites[event.id] = [event.point, event.sprite]
        self.img[event.point.y, event.point.x] = self.sprite_colors[event.sprite]

    def process_walked_event(self, event):
        """
        Processes a "walked" event.
        """
        sprite = self.sprites[event.id][1]
        old_point = self.sprites[event.id][0]
        self.sprites[event.id][0] = event.point
        self.img[event.point.y, event.point.x] = self.sprite_colors[sprite]
        self.img[old_point.y, old_point.x] = self.sprite_colors["Background"]

    def process_ate_event(self, event):
        """
        Processes an "ate" event.
        """
        pass

    def process_eaten_event(self, event):
        """
        Processes an "eaten" event.
        """
        old_point = self.sprites[event.id][0]
        self.img[old_point.y, old_point.x] = self.sprite_colors["Background"]
        del self.sprites[event.id]

    def process_event(self, event):
        options = {
            Actions.Spawned: self.process_spawned_event,
            Actions.Walked: self.process_walked_event,
            Actions.Ate: self.process_ate_event,
            Actions.Eaten: self.process_eaten_event,
            Actions.Mitosed: None,
            Actions.Died: None,
            Actions.Expired: None,
            Actions.NoAction: None,
        }
        if options[event.action] is not None:
            print(event)
            print('-'*32)
            options[event.action](event)


d = Display(600, 400)
d.run('log.log')
# d.run('testlog.log')
