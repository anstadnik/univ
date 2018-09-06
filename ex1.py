import sys
from Display import draw

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: python3.6 ex1.py PATH')
    else:
        try:
            with open(sys.argv[1], 'r') as fd:
                text = [l.strip() for l in fd.readlines()]
        except IOError as e:
            print(e.strerror)
        else:
            try:
                draw(text)
            except RuntimeError as e:
                print(e.strerror)
