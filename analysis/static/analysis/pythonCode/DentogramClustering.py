from analysis.static.analysis.pythonCode import Include, Dentogram


class DentogramClustering(Dentogram.Dentogram):
    def __init__(self):
        super().__init__()

    def _toDo(self, measurement):
        self.col = measurement.columns
        measurement = measurement.T
        measurementN = Include.preprocessing.normalize(measurement)
        Z = self._ClusteringMetod(measurementN)
        return Z

