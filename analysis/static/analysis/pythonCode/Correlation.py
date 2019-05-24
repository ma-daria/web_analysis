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
