import pygame as pg
from enum import Enum
from wall import Wall
import numpy as np

class Env(object):
    """The environment class, which handles all the stuff"""

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.walls = []
        self.glasses = []
        self.refls = []
        self.current = None
        self.fr = None
        self.to = None
        self.angle = None
        self.states = Enum('states', 'idle mk_wall mk_glass set_angle')
        self.state = self.states.idle

    def comp_int(self, beg1, end1, beg2, end2):
        x1, y1 = beg1
        x2, y2 = end1
        x3, y3 = beg2
        x4, y4 = end2
        if abs((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)) < 10e-7:
            return None, None
        Px = (((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) /
              ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)))
        Py = (((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) /
              ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)))
        return Px, Py

    def update(self):
        """Updates stuff
        :returns: TODO
        """
        fr = self.fr
        to = self.to
        if fr and to:
            self.refls = [fr]
            while True:
                inters = []
                for wall in self.walls:
                    px, py = self.comp_int(fr, to, wall.beg, wall.end)
                    if px is None:
                        return
                    if ((fr[0] - to[0]) * (fr[0] - px) > 0 and
                            (fr[1] - to[1]) * (fr[1] - py) > 0 and
                            min(wall.beg[0], wall.end[0]) < px < max(wall.beg[0], wall.end[0]) and
                            min(wall.beg[1], wall.end[1]) < py < max(wall.beg[1], wall.end[1])):
                        inters.append((px, py, True, wall))
                for glass in self.glasses:
                    px, py = self.comp_int(fr, to, glass.beg, glass.end)
                    if px is None:
                        return
                    if ((fr[0] - to[0]) * (fr[0] - px) > 0 and
                            (fr[1] - to[1]) * (fr[1] - py) > 0 and
                            min(glass.beg[0], glass.end[0]) < px < max(glass.beg[0], glass.end[0]) and
                            min(glass.beg[1], glass.end[1]) < py < max(glass.beg[1], glass.end[1])):
                        inters.append((px, py, False, glass))
                rez = None
                br = True
                wall = None
                if inters:
                    for inter in inters:
                        dist = (fr[0] - inter[0]) ** 2 + (fr[1] - inter[1]) ** 2
                        if not rez or dist < rez[2]:
                            rez = inter[0], inter[1], dist
                            br = inter[2]
                            wall = inter[3]
                else:
                    rez = fr[0] + (to[0] - fr[0]) * 100, fr[1] + (to[1] - fr[1]) * 100
                    br = True
                self.refls.append(rez[:2])
                if br:
                    break

                a = np.array(inter[:2]) - np.array(fr)
                b = np.array(wall.beg) - np.array(wall.end)
                if (a @ b) < 0:
                    b = -b
                cosa = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
                l = np.linalg.norm(a) * cosa
                tmp = fr
                fr = to
                to = tmp + b / np.linalg.norm(b) * (2 * l)

    def esc(self):
        self.state = self.states.idle
        self.current = None

    def make_wall(self, pos, button):
        """Makes a new wall

        Args:
            pos (TODO): TODO

        Returns: TODO

        """
        if self.state is self.states.idle:
            self.current = Wall('new', pos, pos)
            self.state = self.states.mk_wall
        elif self.state is self.states.mk_wall:
            if button == 1:
                self.walls.append(Wall('wall', self.current.beg, pos))
                self.current = None
            else:
                self.glasses.append(Wall('glass', self.current.beg, pos))
                self.current = None
            self.state = self.states.idle

    def set_angle(self, pos):
        """Sets the angle

        Args:
            pos (TODO): TODO

        Returns: TODO

        """
        if self.fr:
            self.to = pos

    def place_ray(self, pos):
        """Places the ray beginning

        Args:
            pos (TODO): TODO

        Returns: TODO

        """
        self.fr = pos

    def draw(self):
        """Draws stuff
        :returns: TODO

        """
        for wall in self.walls:
            wall.draw(self.screen)
        for glass in self.glasses:
            glass.draw(self.screen)
        if self.current:
            self.current.end = pg.mouse.get_pos()
            self.current.draw(self.screen)
        color = pg.Color('yellow')
        # print(len(self.refls))
        if self.refls:
            for i in range(len(self.refls) - 1):
                pg.draw.line(self.screen, color, self.refls[i], self.refls[i + 1])
        if self.fr:
            pg.draw.circle(self.screen, color, self.fr, 3, 0)
