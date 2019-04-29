import argparse
from itertools import combinations

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("fp", nargs=1, default=None, help="Input file")
    return parser.parse_args()

def closure(X, deps, p=False):
    if p:
        print("X:", X, "deps:", deps)
    dep = set(X)
    i = 0
    while 42:
        # print(i, ":", X, "->", ''.join(list(dep)))
        prev_dep = dep.copy()
        for d in deps:
            if d[0].issubset(prev_dep):
                dep |= d[1]
        i += 1
        if prev_dep == dep:
            break
    if p:
        print(X, "->", ''.join(list(dep)))
        print()
    return dep

def main():
    args = parse()
    schema = None
    deps = []
    with open(args.fp[0], 'r') as f:
        for l in f:
            if schema is None:  # First line is schema
                schema = set(l[:-1])
            else:
                s = list(map(set, l[:-1].split('->')))
                deps.append(s)
    # print(schema)
    # for s in deps:
    #     print(s)
    n = 1
    unused = schema.copy()
    keys = []
    while n <= len(schema):
        # print(list(combinations(schema, n)))
        for key in combinations(unused, n):
            k = set(key)
            if closure(key, deps) - k == schema - k:
                keys.append(list(key))
                unused -= set(key)
        n += 1
    for key in sorted(keys):
        print(''.join(sorted(key)))

if __name__ == "__main__":
    main()
