import pygame as pg
from env import Env

class Game():

    """This is a game class"""

    def __init__(self):
        """Initializes pygame stuff """
        self.FPS = 60
        self.clock = pg.time.Clock()
        pg.init()
        pg.display.set_caption("Reflections")
        # self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.HWSURFACE | pg.NOFRAME)
        self.screen = pg.display.set_mode((640, 480))
        self.env = Env(self.screen)

    def loop(self):
        """The main loop"""
        while True:
            self.screen.fill(pg.Color('lightslategray'))
            self.env.update()
            self.env.draw()
            if self.handle_input():
                return
            pg.display.flip()
            self.clock.tick(self.FPS)

    def handle_input(self):
        """Handles input

        :returns: TODO

        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return True
                elif event.key == pg.K_ESCAPE:
                    self.env.esc()
                elif event.key == pg.K_r:
                    self.env.place_ray(pg.mouse.get_pos())
                elif event.key == pg.K_a:
                    self.env.set_angle(pg.mouse.get_pos())
                elif event.key == pg.K_d:
                    import ipdb; ipdb.set_trace()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.env.make_wall(pg.mouse.get_pos(), event.button)
        return False

    def run(self):
        """Combines all the things"""
        self.loop()
