import math
debug = False

class Program(object):

    def _input(self):
        self.S = int(input())
        self.N = int(input())
        self.M = int(input())
        self.K = int(input())
        self.L = int(input())
        A1 = []
        A2 = []
        C1 = []
        C2 = []
        for _ in range(self.N):
            A1.append(list(map(int, input().split())))
        for _ in range(self.N):
            A2.append(list(map(int, input().split())))
        for _ in range(self.K):
            C1.append(list(map(int, input().split())))
        for _ in range(self.K):
            C2.append(list(map(int, input().split())))
        A1 = Matrix(self.N, self.M, A1)
        A2 = Matrix(self.N, self.M, A2)
        C1 = Matrix(self.K, self.L, C1)
        C2 = Matrix(self.K, self.L, C2)
        self.A = A2 / A1
        self.C = C2 / C1
        if debug:
            print('A1')
            A1.print()
            print('A2')
            A2.print()
            print('C1')
            C1.print()
            print('C2')
            C2.print()
            print('A')
            self.A.print()
            print('C')
            self.C.print()

    def _S1(self):
        S = self.A + self.C
        if debug:
            print('S')
            S.print()
        det = S.get_determinant()
        print(int(abs(det)))

    def _S2(self):
        s = sum(self.A.tr())
        # IDK what you meant, it seem to works...
        rez = math.e ** s
        if debug:
            assert rez == math.exp(s)
        print(math.floor(rez))

    def _process(self):
        if (self.S == 1 and (self.N != self.K or self.M != self.L)) or (self.S == 2 and self.N != self.M):
            print('ERROR')
            quit()
        elif self.S == 1:
            self._S1()
        else:
            self._S2()

    def run(self):
        self._input()
        self._process()

class Matrix(object):

    def __init__(self, N: int, M: int, arr: list):
        self.N = N
        self.M = M
        self.arr = arr

    def print(self):
        """Prints a Matrix
        :returns: TODO

        """
        for l in self.arr:
            print(l)
        print()

    def __truediv__(self, other):
        """Implements division

        :other: Matrix: TODO
        :returns: TODO

        """
        ret = [[0 for i in range(self.N)] for j in range(self.M)]
        for i in range(self.N):
            for j in range(self.M):
                ret[i][j] = self.arr[i][j] / other.arr[i][j]
        return Matrix(self.N, self.M, ret)

    def __add__(self, other):
        """Implements division

        :other: Matrix: TODO
        :returns: TODO

        """
        ret = [[0 for i in range(self.N)] for j in range(self.M)]
        for i in range(self.N):
            for j in range(self.M):
                ret[i][j] = other.arr[i][j] + self.arr[i][j]
        return Matrix(self.N, self.M, ret)

    def tr(self):
        """Returns main diagonal's elements
        :returns: TODO

        """
        ret = []
        for i in range(self.N):
            ret.append(self.arr[i][i])
        return ret

    def _recurse_det(self, arr: list):
        """Calculates a determinant

        :arr: list: TODO
        :returns: TODO

        """
        # assert len(arr) == len(arr[0])
        if len(arr) == 2:
            return arr[0][0] * arr[1][1] - arr[1][0] * arr[0][1]
        else:
            s = 0
            for i in range(len(arr)):
                tmp = [[arr[j][k] for j in range(1, len(arr))] for k in range(len(arr)) if not k == i]
                s += -1 ** ((arr[0][i] + 1) // 2) * self._recurse_det(tmp)
            return s

    def get_determinant(self):
        """Returns a determinant of a matrix
        :returns: TODO

        """
        return self._recurse_det(self.arr)

if __name__ == "__main__":
    program = Program()
    program.run()
