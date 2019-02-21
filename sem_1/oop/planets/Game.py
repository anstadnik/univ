import pygame as pg
from Planet import Planet
from data import planets_data

# TODO Add orbits
# TODO Add more controls
# TODO Add captions
# TODO Add scaling
# TODO Add moon
class Game(object):
    """The main game class"""
    def __init__(self):
        """Initializes things needed"""
        self.FPS = 60
        self.clock = pg.time.Clock()
        pg.init()
        pg.display.set_caption("Solar system")
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN | pg.HWSURFACE | pg.NOFRAME)
        self.init_planets()
    def init_planets(self):
        """Initializes planets"""
        self.planets = pg.sprite.Group()
        c_x, c_y = self.screen.get_size()
        c_x /= 2
        c_y /= 2
        for p in planets_data:
            path = "./images/" + p[0] + "-transparent-300x300.png"
            planet = Planet(path, c_x, c_y, p)
            self.planets.add(planet)

    def loop(self):
        """The main loop"""
        while True:
            self.screen.fill(pg.Color(0, 0, 0))
            self.planets.update()
            self.planets.draw(self.screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    print('hm')
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        print('hmhm')
                        return
            pg.display.flip()
            self.clock.tick(self.FPS)

    def run(self):
        """Combines all the things"""
        self.loop()
