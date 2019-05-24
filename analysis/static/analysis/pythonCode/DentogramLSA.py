from analysis.static.analysis.pythonCode import Include
from analysis.static.analysis.pythonCode import Dentogram
from django.conf import settings

class DentogramLSA(Dentogram.Dentogram):
    def __init__(self):
        super().__init__()

    def _toDo(self, measurement):
        col = measurement.columns
        measurement = measurement.T
        measurement = Include.preprocessing.normalize(measurement)
        U, S, Vt = Include.np.linalg.svd(measurement)
        k = int((col.size * 10)/100)
        U = U[:,0:k]
        S = S[0:k]
        Vt = Vt[0:k, :]
        U_S = Include.np.multiply(S, U)
        A_ = Include.np.dot(U_S, Vt)
        cl = self._ClusteringMetod(A_, 0.2, col)
        Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/image/LSA.png")
        return cl