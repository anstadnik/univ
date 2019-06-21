import pygame as pg

class Wall():

    """Class for walls and glasses"""

    def __init__(self, t, beg, end):
        """TODO: to be defined1. """
        self.type = t
        self.beg = beg
        self.end = end

    def draw(self, screen: pg.Surface):
        """TODO: Docstring for draw.

        :f: TODO
        :screen: pg.surface.: TODO
        :returns: TODO

        """
        if self.type == 'new':
            color = pg.Color('green')
        if self.type == 'glass':
            color = pg.Color('cyan')
        else:
            color = pg.Color('darkred')
        pg.draw.line(screen, color, self.beg, self.end)
