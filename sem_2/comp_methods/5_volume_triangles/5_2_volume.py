import numpy as np

def parse():
    with open('input/volume.txt', 'r') as f:
        points = []
        point = []
        for line in f:
            point.append(float(line[:-1]))
            if len(point) == 3:
                points.append(np.array(point))
                point = []
    return points


def main():
    points = parse()
    mat = []
    for i in range(1, 4):
        mat.append((points[0] - points[i]))
    print(np.array(mat).T)
    # weight = dencity * volume
    V = abs(np.linalg.det(mat))  # In micrones
    #  1 micron == 10 000 cm
    p = 2.711 # gr / sm ** 3
    M = V * p
    print("Volume = ", V, ", mass = ", M)


if __name__ == "__main__":
    main()
