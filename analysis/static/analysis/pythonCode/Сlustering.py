from analysis.static.analysis.pythonCode import Include
from django.conf import settings

def Сlustering(measurement):
    col = measurement.columns
    measurement = measurement.T
    measurementN = Include.preprocessing.normalize(measurement)
    Z = СlusteringMetod(measurementN, 0.5, col)
    Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/image/Сlustering.png")
    # Include.plt.savefig("/home/ma-daria/PycharmProjects/web_analysis/analysis/static/analysis/image/Сlustering.png")
    return Z

def СlusteringMetod(measurement, index, col):
    distance_mat = Include.distance.pdist(measurement, 'cosine')
    Z = Include.hierarchy.linkage(distance_mat, 'single')
    Include.plt.figure(figsize=(20, 10))
    dn = Include.hierarchy.dendrogram(Z, labels=col, color_threshold=index)
    return Z
