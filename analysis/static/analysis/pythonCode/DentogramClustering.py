from analysis.static.analysis.pythonCode import Include
from analysis.static.analysis.pythonCode import Dentogram
from django.conf import settings

class DentogramClustering(Dentogram.Dentogram):
    def __init__(self):
        super().__init__()

    def _toDo(self, measurement):
        col = measurement.columns
        measurement = measurement.T
        measurementN = Include.preprocessing.normalize(measurement)
        Z = self._ClusteringMetod(measurementN, 0.5, col)
        Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/image/Сlustering.png")
        return Z

