import curses

class Display(object):
    """Curses handler. It displays the text, help. Processes key pressing
    """

    def __init__(self, scr, text: list):
        """Initializes class.
        Parameters:
            scr -- standart screen, passed from curses.wrapper()
            text -- array of strings
        """

        self.scr = scr
        self.max_y, self.max_x = scr.getmaxyx()
        self.text = text
        self.maxlen = max([len(l) for l in text])
        self.num_line = 0 # Number of line to start from
        self.num_char = 0 # Number of char to start from


    def __draw(self):
        self.scr.clear()
        height = self.max_y - 2
        last_line = len(self.text)\
            if len(self.text) - self.num_line < height\
            else self.num_line + height
        to_draw = self.text[self.num_line : last_line]
        for i, line in enumerate(to_draw):
            #TODO test for too big num_line
            end_char = min(len(line) - self.num_char, self.max_x)
            self.scr.addstr(i, 0, line[self.num_char : end_char])
        self.scr.addstr(self.max_y - 1, 0,\
                        "h: left, j: down, k: up, l: right, u: up, d: down")
        coords = str(self.num_line) + " : " + str(self.num_char)
        self.scr.addstr(self.max_y - 1, self.max_x - 2 - len(coords), coords)


    def __move(self, d: str, step: int):
        """Changes top line's position
        """

        if d == 'UP':
            if self.num_line - step >= 0:
                self.num_line -= step
            else:
                self.num_line = 0
        if d == 'DOWN':
            if self.num_line + step < len(self.text):
                #TODO check if I should leave < there or I should use <=
                self.num_line += step
            else:
                self.num_line = len(self.text) - (self.max_y - 2)
        if d == 'RIGHT':
            if self.num_char + step < self.maxlen:
                #TODO check if I should leave < there or I should use <=
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
            True if redraw is needed else False
        """

        if c == curses.KEY_RESIZE:
            self.max_y, self.max_x = self.scr.getmaxyx()
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
        elif c == ord('q'):
            quit()
        else:
            return False
        return True


    def run(self):
        """Infinite loop, that does all the action
        """

        redraw = True
        while True:
            if redraw:
                self.__draw()
            c = self.scr.getch()
            redraw = self.key_hooks(c)
        #TODO Handle screen resize (KEY_RESIZE)

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
    """The draw function. Sets things up and if all is good calls the draw function
    Parameters:
        text -- array of strings
    """

    curses.wrapper(wrapper, text)
