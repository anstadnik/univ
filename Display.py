import curses

class Display(object):
    """Curses handler. It displays the text, help. Processes key pressing
    """

    def __init__(self, scr, text: list):
        """Initializes class.
        Parameters:
            scr -- standart screen, passed from curses.wrapper()
            text -- array of strings"""

        self.scr = scr
        self.header = text[0]
        self.text = text[1:]
        self.maxlen = max([len(l) for l in text]) - 1 # The biggest possible value of num_char
        self.num_line = 0 # Number of line to start from
        self.num_char = 0 # Number of char to start from
        self.helpmsg = "Keys: h, j, k, l, u, d, U, D, g, G, r. Quit - q"
        self.coords = str(self.num_line) + ":" + str(self.num_char)
        curses.curs_set(0)
        self.resize()


    def resize(self):
        self.max_y, self.max_x = self.scr.getmaxyx()
        if self.max_y < 3 or self.max_x < len(self.coords) + 10:
            raise RuntimeError('Window is too small')


    def __draw(self):
        self.scr.clear()
        height = self.max_y - 4
        last_line = len(self.text)\
            if len(self.text) - self.num_line < height\
            else self.num_line + height
        to_draw = self.text[self.num_line : last_line]
        for i, line in enumerate(to_draw):
            end_char = min(len(line), self.max_x + self.num_char)
            self.scr.addstr(i + 2, 0, line[self.num_char : end_char])
        end_char = min(len(self.header), self.max_x + self.num_char)
        self.scr.addstr(0, 0, self.header[self.num_char:end_char])
        if len(self.helpmsg) + len(self.coords) + 3 < self.max_x:
            self.scr.addstr(self.max_y - 1, 0, self.helpmsg)
        else:
            self.scr.addstr(self.max_y - 1, 0, self.helpmsg[:self.max_x - len(self.coords) - 6] + "...")
        self.coords = str(self.num_line) + ":" + str(self.num_char)
        self.scr.addstr(self.max_y - 1, self.max_x - 1 - len(self.coords), self.coords)


    def __move(self, d: str, step: int):
        """Changes the starting point
        Parameters:
            d -- direction
            step -- how much to move the starting point"""

        if d == 'UP':
            if self.num_line - step >= 0:
                self.num_line -= step
            else:
                self.num_line = 0
        if d == 'DOWN':
            if self.num_line + step < len(self.text) - (self.max_y - 2):
                self.num_line += step
            else:
                self.num_line = len(self.text) - (self.max_y - 2)
        if d == 'RIGHT':
            if self.num_char + step < self.maxlen:
                self.num_char += step
            else:
                self.num_char = self.maxlen
        if d == 'LEFT':
            if self.num_char - step > 0:
                self.num_char -= step
            else:
                self.num_char = 0


    def key_hooks(self, c) -> bool:
        """Processes key pressing
        Parameters:
            c -- key that was pressed
        Return value:
            True if redraw is needed else False"""

        if c == curses.KEY_RESIZE:
            self.resize()
        elif c == ord('h'):
            self.__move('LEFT', 1)
        elif c == ord('j'):
            self.__move('DOWN', 1)
        elif c == ord('k'):
            self.__move('UP', 1)
        elif c == ord('l'):
            self.__move('RIGHT', 1)
        elif c == ord('u'):
            self.__move('UP', self.max_y // 2)
        elif c == ord('d'):
            self.__move('DOWN', self.max_y // 2)
        elif c == ord('U'):
            self.__move('UP', self.max_y)
        elif c == ord('D'):
            self.__move('DOWN', self.max_y)
        elif c == ord('g'):
            self.num_line = 0
        elif c == ord('G'):
            self.num_line = len(self.text) - (self.max_y - 2)
        elif c == ord('q'):
            quit()
        elif c == ord('r'):
            self.num_char = 0
            self.num_line = 0
        else:
            return False
        return True


    def run(self):
        """Infinite loop, that does all the action"""

        redraw = True
        while True:
            if redraw:
                self.__draw()
            c = self.scr.getch()
            redraw = self.key_hooks(c)


def wrapper(scr, text: list):
    """This function is needed for using curses.wrapper
    ...and for making things more beautiful
    Parameters:
        scr -- standart screen, passed from curses.wrapper()
        text -- array of strings
    """

    display = Display(scr, text)
    display.run()


def draw(text: list):
    """The draw function. Wrapper for an easy use of this whole file
    Parameters:
        text -- array of strings
    """

    curses.wrapper(wrapper, text)
