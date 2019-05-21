import Include

def Сlustering(measurement):
    col = measurement.columns
    measurement = measurement.T
    measurementN = Include.preprocessing.normalize(measurement)
    Z = СlusteringMetod(measurementN, 0.5, col)
    Include.plt.savefig("Result/Сlustering.png")
    return Z

def СlusteringMetod(measurement, index, col):
    distance_mat = Include.distance.pdist(measurement, 'cosine')
    Z = Include.hierarchy.linkage(distance_mat, 'single')
    Include.plt.figure(figsize=(20, 10))
    dn = Include.hierarchy.dendrogram(Z, labels=col, color_threshold=index)
    return Z
