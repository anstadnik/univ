import pygame as pg
from env import Env

class Game(object):
    """The main game class"""
    def __init__(self):
        """Initializes things needed"""
        self.FPS = 60
        self.clock = pg.time.Clock()
        pg.init()
        pg.display.set_caption("Cars")
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.HWSURFACE | pg.NOFRAME)
        self.env = Env(self.screen)

    def loop(self):
        """The main loop"""
        while True:
            self.screen.fill(pg.Color('darkturquoise'))
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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return True
        return False

    def run(self):
        """Combines all the things"""
        self.loop()

if __name__ == "__main__":
    game = Game()
    game.run()
