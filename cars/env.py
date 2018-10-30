import pygame as pg
from car import Car
import random
from text import text_to_screen

class Env(object):
    """The environment class, which handles all the stuff"""
    def __init__(self, screen: pg.Surface):
        self.cars = pg.sprite.Group()
        self.tmp = len(self.cars)
        self.size_car = (10, 20)
        self.max_cars = 20
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.start = 0
        self.starts = [pg.sprite.Sprite() for _ in range(4)]
        self.starts[0].rect = pg.rect.Rect((10, 10), (10, 10))
        self.starts[1].rect = pg.rect.Rect((self.width - 30, 10), (10, 10))
        self.starts[2].rect = pg.rect.Rect((10, self.height - 30), (10, 10))
        self.starts[3].rect = pg.rect.Rect((self.width - 30, self.height - 30), (10, 10))

    def get_dir(self, start: int):
        """Returns dir for specific position

        :start: int: TODO
        :returns: TODO"""
        r1, r2 = random.random() + 1e-7, random.random() + 1e-7
        if start == 0:
            return (r1, r2)
        elif start == 1:
            return (-r1, r2)
        elif start == 2:
            return (r1, -r2)
        return (-r1, -r2)

    def _manage_cars(self):
        """Adds a car

        :returns: TODO"""
        dead_list = self.screen.get_rect().collidelistall(self.cars.sprites())
        to_delete = []
        for n, c in enumerate(self.cars):
            if not n in dead_list:
                to_delete.append(c)
        self.cars.remove(to_delete)
        if len(self.cars) < self.max_cars:
            tmp = None
            i = 0
            while pg.sprite.spritecollideany(self.starts[self.start], self.cars):
                if tmp:
                    if tmp == self.start:
                        return
                else:
                    tmp = self.start
                i += 1
                self.start = (self.start + 1) % 4
            start = self.starts[self.start]
            self.cars.add(Car(start.rect.topleft, self.get_dir(self.start), self.size_car))

    def update(self):
        """Updates stuff
        :f: TODO
        :returns: TODO
        """
        self._manage_cars()
        self.cars.update()
        text_to_screen(self.screen, len(self.cars), 10, 10)
        # calculate intersections for cars
        # update cars

    def draw(self):
        """Draws cars
        :returns: TODO

        """
        for car in self.cars:
            car.draw(self.screen)
