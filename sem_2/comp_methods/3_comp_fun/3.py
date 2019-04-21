import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot, iplot

def f1(x):
    return (x-2) * (x-0) * (x-31) * (x-6)

def f2(x):
    return x ** 4 - 39 * x ** 3 + 260 * x ** 2 - 372 * x + 0


def main():
    X = [np.arange(0, 10, i) for i in [0.001, 0.01, 0.1, 1]]
    f1_v = np.vectorize(f1)
    f2_v = np.vectorize(f2)
    data = []
    data_abs = []
    for x in X:
        data.append(go.Scatter(x = x, y = f1_v(x) - f2_v(x), mode='lines+markers', name=str(x[1]-x[0])))
        data_abs.append(go.Scatter(x = x, y = abs(f1_v(x) - f2_v(x)), mode='lines+markers', name=str(x[1]-x[0])))
    # layout = go.Layout(
    #         xaxis=dict(
    #             type='log',
    #             autorange=True
    #             )
    #         )
    # plot(go.Figure(data=data, layout=layout))
    plot(data)
    

if __name__ == "__main__":
    main()
