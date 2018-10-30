import pygame as pg
from enum import Enum

class Car(pg.sprite.Sprite):
    """The car object"""
    def __init__(self, pos: list, direction: list, size: list):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.rect.Rect(pos, size)
        self.direction = direction
        self.states = Enum("States", "moving accelerating braking stopped broke")
        self.state = self.states.accelerating
        self.speed = 0
        self.max_speed = 10

    def update(self):
        """TODO: Docstring for update.
        :returns: TODO

        """
        if self.speed < self.max_speed:
            self.speed += 0.1
        self.rect.move_ip(*[d * self.speed for d in self.direction])

    def draw(self, screen: pg.Surface):
        """TODO: Docstring for draw.

        :f: TODO
        :screen: pg.surface.: TODO
        :returns: TODO

        """
        pg.draw.rect(screen, pg.Color('black'), self.rect)
