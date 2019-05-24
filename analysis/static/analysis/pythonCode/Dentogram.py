from analysis.static.analysis.pythonCode import Include

class Dentogram(object):
    def __init__(self):
        self.data = []

    def dentogram(self, measurement):
        if len(self.data) == 0:
            self.data = self.toDo(measurement)
        return self.data

    def toDo(self, measurement):
        return []

    def ClusteringMetod(self, measurement, index, col):
        distance_mat = Include.distance.pdist(measurement, 'cosine')
        Z = Include.hierarchy.linkage(distance_mat, 'single')
        Include.plt.figure(figsize=(20, 10))
        dn = Include.hierarchy.dendrogram(Z, labels=col, color_threshold=index)
        return Z

