import pygame as pg
from math import cos, sin

class Planet(pg.sprite.Sprite):
    """The main planet class"""
    def __init__(self, path: str, c_x, c_y, p: list):
        """Initializes a planet"""
        super().__init__()
        self.size = p[1]
        self.image = pg.transform.scale(pg.image.load(path), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.a = p[2]
        self.b = self.a + p[3]
        self.speed = 1 / p[4]
        self.c_x, self.c_y = c_x + self.a * p[5], c_y
        self.t = 0
        self.dt = 1 / max(10e-5, p[6])

    def update(self):
        """Updates the planet's position"""
        self.rect.center = (self.c_x + self.a * cos(self.t), self.c_y + self.b * sin(self.t))
        self.t += self.dt
