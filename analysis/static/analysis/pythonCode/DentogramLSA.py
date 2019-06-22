from analysis.static.analysis.pythonCode import Include, Dentogram

class DentogramLSA(Dentogram.Dentogram):
    mass = [] #матрица основной структуры различных зависимостей исходных данных

    def __init__(self):
        super().__init__()

    # метод реализация алгоритма латентно-семантического анализа
    def _toDo(self,  measurement, nameCol):
        self.col = measurement.columns
        measurement = measurement.T
        measurement = Include.preprocessing.normalize(measurement)
        U, S, Vt = Include.np.linalg.svd(measurement)
        k = int((len(S) * 10)/100)
        if k == 0:
            k = 1
        U = U[:,0:k]
        S = S[0:k]
        Vt = Vt[0:k, :]
        U_S = Include.np.multiply(S, U)
        A_ = Include.np.dot(U_S, Vt)
        self.mass = A_
        cl = self._ClusteringMetod(A_)
        return cl

    # метод возврата матрицы основной структуры различных зависимостей исходных данных
    def GetMass(self):
        return self.mass