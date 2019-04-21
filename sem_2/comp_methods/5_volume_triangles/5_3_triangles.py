import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot, iplot
import itertools


def parse():
    # with open('input/triangles_1.txt', 'r') as f:
    data = []
    with open('input/triangles_2.txt', 'r') as f:
        data = [list(map(float, line.split())) for line in f]
    return np.unique(np.array(data), axis=0)

def disp(points, triangles=None):
    X, Y = points[:, 0], points[:, 1]
    data = []
    data.append(go.Scatter(x = X, y = Y, mode='markers'))
    if triangles:
        for i, triangle in enumerate(triangles):
            X = [triangle[j][0] for j in [0, 1, 2, 0]]
            Y = [triangle[j][1] for j in [0, 1, 2, 0]]
            data.append(go.Scatter(x = X, y = Y, mode='lines'))
    plot(data)


def area_of_triangle(p1, p2, p3):
    s = (1/2) * abs(np.linalg.det([[p1[0]-p3[0], p1[1]-p3[1]],
            [p2[0]-p3[0], p2[1]-p3[1]]]))
    return s
    

def main():
    points = parse()
    ps = points

    # The lowest point
    ind = points[:, 1].argsort()[0]
    the_point = points[ind]
    # Remove the_points
    points = np.r_[points[:ind, :], points[ind+1:, :]]
    # Sort from left to right
    points = points[points[:, 0].argsort()]

    triangles = []
    for i in range(2, len(points) + 1):
        triangles.append([the_point, *points[i-2:i]])

    disp(ps, triangles)

    area = 0
    for triangle in triangles:
        p1, p2, p3 = triangle
        area += area_of_triangle(p1, p2, p3)
    print(area)

if __name__ == "__main__":
    main()
