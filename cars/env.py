import pygame as pg

class Env(object):

    """The environment class, which handles all the stuff"""

    def __init__(self):
        self.cars = pg.sprite.Group()
        self.max_cars = 20

    def update(self):
        """Updates stuff

        :f: TODO
        :returns: TODO

        """
        if len(self.cars) < self.max_cars:
            self._add_car()
        # calculate intersections for cars
        # update cars

    def _add_car(self):
        """Adds a car
        :returns: TODO

        """
        pass


    def draw(self):
        """Draws cars
        :returns: TODO

        """
        # draw cars
        pass
