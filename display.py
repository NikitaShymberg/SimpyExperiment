import re
import numpy as np
import cv2
from utils import Point, Actions


class Event():
    """
    A class that represents a single line in the log.
    This is an event at a single timestamp, for a single sprite, at a single place.
    """
    def __init__(self, log_string):
        """
        Black magic string parsing method to create an Event from a log entry.
        """
        match_string = r'\[([0-9]+) \| ([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}) \| \((\s*[0-9]+,\s*[0-9]+)\)\] ([\S\s]*)'  # noqa: E501
        groups = re.search(match_string, log_string).groups()
        self.time = int(groups[0])  # Event timestamp
        self.id = groups[1]  # ID of the sprite that the event affects
        x, y = int(groups[2].split()[0][:-1]), int(groups[2].split()[1])
        self.point = Point(x, y)  # The location of the event
        for action in Actions:
            if groups[3].strip() == action.name:
                self.action = action  # The type of event
                break
        else:
            # Spawn because it is followed by what spawned
            self.action = Actions.Spawned
            self.sprite = groups[3][7:].strip()  # The type of sprite that was spawned

    def __repr__(self):
        return f'[{int(self.time)} | {self.id} | {self.point}] {self.action.name}'


class Display():
    """
    This is the class that visualises the simulation.
    Collects and processes all events. At every timestep displays the current map setup.
    If `save` is true, saves the visualization as an avi.
    """
    def __init__(self, width, height, fps=120, save=False):
        self.width = width
        self.height = height
        self.current_time = 0
        self.img = np.zeros((height, width, 3), dtype=np.uint8)
        self.fps = fps
        self.sprites = {}  # Keeps track of the sprite IDs, locations, and types
        self.sprite_colors = {
            'Peon': (255, 255, 255),
            'Food': (0, 0, 255),
            'Background': (0, 0, 0)
        }
        if save:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # HFYU works for lossless, TODO figure out HEVC
            self.video = cv2.VideoWriter('simulation.avi', fourcc, self.fps, (self.width, self.height))
        else:
            self.video = None

    def __del__(self):
        """
        Clean up the video creation on exit.
        """
        if self.video:
            self.video.release()

    def read_log(self, path):
        """
        A generator that reads the log at `path` and yields one row at a time.
        """
        for row in open(path):
            yield row

    def show(self):
        """
        Displays the current `self.img` state at the framerate specified by `self.fps`.
        """
        if self.video:
            self.video.write(self.img)
        cv2.imshow('Simpy', self.img)
        cv2.waitKey(1000 // self.fps)

    def simulate(self, path):
        """
        This is the "main" function to run.
        Iterates over the log at `path` and displays the simulation.
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

    def process_died_event(self, event):
        """
        Processes a "died", "expired" or "eaten" event.
        """
        old_point = self.sprites[event.id][0]
        self.img[old_point.y, old_point.x] = self.sprite_colors["Background"]
        del self.sprites[event.id]

    def process_event(self, event):
        """
        Processes a given event by calling one of the helper functions.
        This updates the state of `self` to reflect the changes of the current `event`.
        """
        options = {
            Actions.Spawned: self.process_spawned_event,
            Actions.Walked: self.process_walked_event,
            Actions.Ate: None,
            Actions.Eaten: self.process_died_event,
            Actions.Mitosed: None,
            Actions.Died: self.process_died_event,
            Actions.Expired: self.process_died_event,
            Actions.NoAction: None,
        }
        if options[event.action] is not None:
            print(event)
            print('-'*32)
            options[event.action](event)


d = Display(600, 400, save=True)
d.simulate('log.log')
