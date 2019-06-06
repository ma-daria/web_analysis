from analysis.static.analysis.pythonCode import Include
import time

class Correlation(object):
    def __init__(self):
        self.data = []
        self.buffer = []

    def correlation(self, measurement):
        if len(self.data) == 0:
            self.data = measurement.corr()
        return self.data
    def getData(self):
        return self.data

    def SortingCorrelation(self, correlati):
        correlation_mod = correlati.abs()
        correlation_mod = correlation_mod.sort_values(ascending=False)
        for name in correlation_mod.index:
            correlation_mod[name] = correlati[name]
        return correlation_mod

    def getPhoto(self, size):
        if self.buffer == []:
            self.drаw(size)
        return self.buffer

    def drаw(self, size):
        if (size == 20):
            time.sleep(5)  # вот этот говнокод, но я не знаю как решить. Там они паралельно запускаются похоже и мешают друг другу
        mapPalette = Include.sns.diverging_palette(10, 240, sep=10, as_cmap=True)
        Include.plt.figure(figsize=(size, size), dpi=200)
        Include.sns.heatmap(self.data, cmap=mapPalette, vmin=-1, vmax=1)
        self.buffer = Include.io.BytesIO()
        Include.plt.savefig(self.buffer, format='png')
