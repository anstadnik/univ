import pygame as pg
from enum import Enum

class Car(pg.sprite.Sprite):

    """The car object"""

    def __init__(self, pos: list, direction: list, size: list):
        pg.sprite.Sprite.__init__()
        self.rect = pg.rect.Rect(pos, size)
        self.direction = direction
        self.states = Enum("moving", "accelerating", "braking", "stopped", "broke")
        self.state = self.states.accelerating
        self.max_speed = 10

    def update(self):
        """TODO: Docstring for update.
        :returns: TODO

        """
        pass
