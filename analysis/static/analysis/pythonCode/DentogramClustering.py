from analysis.static.analysis.pythonCode import Include, Dentogram

# класс потомок класса Dentogram, который реализует алгоритм кластеризации
class DentogramClustering(Dentogram.Dentogram):
    def __init__(self):
        super().__init__()

    # метод реализации алгоритма кластеризации
    def _toDo(self,  measurement, nameCol):
        self.col = measurement.columns
        measurement = measurement.T
        measurementN = Include.preprocessing.normalize(measurement)
        Z = self._ClusteringMetod(measurementN)
        return Z