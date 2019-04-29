import argparse

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--variable", required=True, default=None, help="Target variable")
    parser.add_argument("fp", nargs=1, default=None, help="Input file")
    return parser.parse_args()

def main():
    args = parse()
    if len(args.variable) != 1:
        print("Target variable has to be a single char")
        quit(1)
    inp = []
    with open(args.fp[0], 'r') as f:
        for l in f:
            s = list(map(set, l[:-1].split('->')))
            if len(s) == 2:
                inp.append(s)
    for s in inp:
        print(s)
    dep = {args.variable}
    i = 0
    while 42:
        print(i, ":", args.variable, "->", ''.join(list(dep)))
        prev_dep = dep.copy()
        for d in inp:
            if d[0].issubset(prev_dep):
                dep |= d[1]
        i += 1
        if prev_dep == dep:
            break
    print(args.variable, "->", ''.join(list(dep)))

if __name__ == "__main__":
    main()
