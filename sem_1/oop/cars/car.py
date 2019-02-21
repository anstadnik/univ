import pygame as pg
from enum import Enum
import random

class Car(pg.sprite.Sprite):
    """The car object"""
    def __init__(self, pos: list, direction: list, size: list):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.rect.Rect(pos, size)
        self.direction = direction
        self.vision_size = 100
        self.vision = pg.rect.Rect(self._get_rect_vis())
        self.states = Enum("States", "accelerating braking stopped broke")
        self.state = self.states.accelerating
        self.speed = 5
        self.max_speed = 10
        self.countdown = random.randint(20, 100)

    def _get_rect_vis(self):
        """Returns parameters for vision rect
        :returns: TODO

        """
        d1, d2 = self.direction[0] > 0, self.direction[1] > 0
        if d1 and d2:
            return (*self.rect.topleft, self.rect.width + self.vision_size, self.rect.height + self.vision_size)
        if not d1 and d2:
            return (self.rect.left - self.vision_size, self.rect.top, self.rect.width + self.vision_size, self.rect.height + self.vision_size)
        if d1 and not d2:
            return (self.rect.left, self.rect.top - self.vision_size, self.rect.width + self.vision_size, self.rect.height + self.vision_size)
        if not d1 and not d2:
            return (self.rect.left - self.vision_size, self.rect.top - self.vision_size, self.rect.width + self.vision_size, self.rect.height + self.vision_size)

    def update(self, cars: pg.sprite.Group):
        """TODO: Docstring for update.
        :returns: TODO

        """
        if not self.state == self.state.broke:
            if len(self.rect.collidelistall(cars.sprites())) > 1:
                self.state = self.states.broke
                self.speed = 0
            elif len(self.vision.collidelistall(cars.sprites())) > 1:
                if self.speed > 0:
                    self.state = self.states.braking
                else:
                    self.state = self.states.stopped
                    self.speed = 0
            else:
                self.state = self.states.accelerating
                self.countdown = random.randint(20, 100)
        if self.speed == 0:
            if self.countdown:
                self.countdown -= 1
            else:
                self.kill()
        if self.state == self.states.accelerating:
            if self.speed < self.max_speed:
                self.speed += 1
        elif self.state == self.states.braking:
            self.speed -= 0.1
        self.rect.move_ip(*[d * self.speed for d in self.direction])
        self.vision.move_ip(*[d * self.speed for d in self.direction])

    def draw(self, screen: pg.Surface):
        """TODO: Docstring for draw.

        :f: TODO
        :screen: pg.surface.: TODO
        :returns: TODO

        """
        # pg.draw.rect(screen, pg.Color('darkviolet'), self.vision)
        if self.state == self.states.accelerating:
            color = pg.Color('chocolate1')
        elif self.state == self.states.braking:
            color = pg.Color('darkgoldenrod')
        elif self.state == self.states.stopped:
            color = pg.Color('darksalmon')
        else:
            color = pg.Color('darkred')
        pg.draw.rect(screen, color, self.rect)
