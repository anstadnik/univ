import numpy as np
from time import sleep

def parse():
    data = []
    with open('input.txt', 'r') as f:
        for line in f:
            if not line.startswith('#'):
                data.append(list(map(int, line[:-1].split())))
    train = np.array(data[:-1], dtype=np.float)
    test = np.array(data[-1], dtype=np.float)
    return train, test
    
def Gauss_solve(matrix, p=False):
    s = matrix.shape[0] #  Shape of the input array
    for i in range(s):
        e = matrix[i, i]  # The diagonal element
        matrix[i, :] /= e
        ind = [num for num in range(s) if num != i]
        matrix[ind, :] -= matrix[i, :] * matrix[ind, i][:, None]
        if p:
            print(matrix)
    X = matrix[:, -1]
    return X

def Kramer_solve(matrix):
    s = matrix.shape[0] #  Shape of the input array
    A = matrix[:, :s]
    B = matrix[:, s:]
    d = np.linalg.det(A)
    d_x = []
    for i in range(s):
        d_x.append(np.linalg.det(np.c_[A[:, :i], B, A[:, i+1:]]))
    d_x = np.array(d_x)
    return d_x / d
    
def Inv_solve(matrix):
    s = matrix.shape[0] #  Shape of the input array
    A = matrix[:, :s]
    B = matrix[:, s:]
    print(A.shape, B.shape)
    return (np.linalg.inv(A) @ B).flatten()
    
# DOES NOT CONVERGE
def Jacobi_solve(matrix):
    print(matrix)
    s = matrix.shape[0] #  Shape of the input array
    # A = matrix[:, :s]
    # B = matrix[:, s:]
    # It converges with this matrix
    A = np.array([[10., -1., 2., 0.],
                  [-1., 11., -1., 3.],
                  [2., -1., 10., -1.],
                  [0.0, 3., -1., 8.]])
    # initialize the RHS vector
    B = np.array([6., 25., -11., 15.])
    X = np.random.rand(*B.shape)
    eps = 10 ** -7
    D = A * np.eye(*A.shape)
    R = A - D
    while 42:
        X_prev = X
        X = np.linalg.inv(D) @ (B - R @ X)
        print(X)
        input()
        # sleep(1)
        if np.sum(abs(X - X_prev)) < eps:
            break
    return X
    

def main():
    train, test = parse()

    #  Gauss

    s = train.shape[0] #  Shape of the input array
    A = train[:, :s]
    B = train[:, s:]
    X_gauss = Gauss_solve(train.copy())
    X_kramer = Kramer_solve(train.copy())
    X_inv = Inv_solve(train.copy())
    # DOES NOT CONVERGE WITH A GIVEN MATRIX
    # X_jac = Jacobi_solve(train.copy())
    X_np = np.linalg.solve(A, B).flatten()
    print(train)
    print('Coeffitients, obtained using Gauss method:', X_gauss)
    print('Coeffitients, obtained using Kramer method:', X_kramer)
    # print('Coeffitients, obtained using Jacobi method:', X_kramer)
    print('Coeffitients, obtained using inverse matrix method:', X_inv)
    print('Results, obtained using numpy:', X_np)
    print('Results comparison (has ot be almost 0):', (A.T @ X_gauss[:, None] - B).flatten())
    print('Results for the 6th programmer:', test @ X_gauss)


if __name__ == "__main__":
    main()
