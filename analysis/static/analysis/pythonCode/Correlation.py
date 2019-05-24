from analysis.static.analysis.pythonCode import Include

class Correlation(object):
    def __init__(self):
        self.data = []

    def correlation(self, measurement):
        if len(self.data) == 0:
            self.data = self.toDo(measurement)
        return self.data

    def toDo(self, measurement):
        return []

    def SortingCorrelation(self, correlati):
        correlation_mod = correlati.abs()
        correlation_mod = correlation_mod.sort_values(ascending=False)
        for name in correlation_mod.index:
            correlation_mod[name] = correlati[name]
        return correlation_mod