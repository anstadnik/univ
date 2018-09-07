import sys
from Display import draw

def parse_csv(text: list) -> list:
    """Parses csv
    Parameters:
        text -- list of pure strings
    Return value:
        list[0] -- columns headers
        list[1] -- list of strings. Each string contains one line of csv"""

    print('Loading...')
    ret = []
    if len(text) == 0:
        raise RuntimeError('Wrong file')
    ret.append(text[0].split(','))
    if len(ret[0]) < 2:
        raise RuntimeError('Wrong file')
    lengths = [len(item) for item in ret[0]]
    for line in text[1:]:
        line = line.split(',')
        if len(line) != len(ret[0]):
            raise RuntimeError('Wrong file')
        lengths = [max(l, len(i)) for l, i in zip(lengths, line)]
        ret.append(line)
    for j, l in enumerate(ret):
        arr = ['{:{width}}'.format(item, width = str(length)) for item, length in zip(l, lengths)]
        ret[j] = ' | '.join(arr)
    return ret


def get_text(path: str) -> str:
    try:
        with open(path, 'r') as fd:
            text = [l.strip() for l in fd.readlines()]
    except IOError as e:
        print(e.strerror)
        quit(1)
    try:
        ret = parse_csv(text)
    except RuntimeError as e:
        print(e.strerror)
        quit(1)
    return ret


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print('Usage: python3.6 ex1.py PATH')
        quit(1)
    text = get_text(sys.argv[1])
    try:
        draw(text)
    except RuntimeError as e:
        print(e.strerror)
