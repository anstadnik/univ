import sys
from Display import draw

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Please give some parameters')
    else:
        try:
            with open(sys.argv[1], 'r') as fd:
                text = fd.readlines()
            draw(text)
        except FileNotFoundError:
            print('File not found')
