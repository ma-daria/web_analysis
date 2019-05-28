from analysis.static.analysis.pythonCode import Include, Correlation
from django.conf import settings

class CorrelationZooplankton(Correlation.Correlation):
    def __init__(self):
        super().__init__()

    def _toDo(self, measurement):
        mapPalette = Include.sns.diverging_palette(10, 240, sep=10, as_cmap=True)
        Include.plt.figure(figsize=(20, 20), dpi=200)
        correlationZooplankton = measurement.corr()
        Include.sns.heatmap(correlationZooplankton, cmap=mapPalette, vmin=-1, vmax=1)
        Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/image/CorrelationZooplankton.png")
        # plt.show()
        # print(measurement.corr())
        return correlationZooplankton