from analysis.static.analysis.pythonCode import Include
from analysis.static.analysis.pythonCode import Dentogram
from django.conf import settings

class Clustering(Dentogram.Dentogram):
    def __init__(self):
        super().__init__()

    def toDo(self, measurement):
        col = measurement.columns
        measurement = measurement.T
        measurementN = Include.preprocessing.normalize(measurement)
        Z = self.ClusteringMetod(measurementN, 0.5, col)
        Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/image/Сlustering.png")
        return Z

