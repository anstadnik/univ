def find_sub(a, b):
    rez_ = 0
    rez = ''
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i] == b[j]:
                ret = find_sub(a[i+1:], b[j+1:])
                ret_ = ret[0] + 1
                if ret_ > rez_:
                    rez_= ret_
                    rez = a[i] + ret[1]
    return rez_, rez


def main():
    a = input().split()
    b = input().split()
    print(find_sub(a, b))


if __name__ == "__main__":
    main()
