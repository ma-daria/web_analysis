from analysis.static.analysis.pythonCode import Include, Correlation
from django.conf import settings

class CorrelationChemistry(Correlation.Correlation):
    def __init__(self):
        super().__init__()

    def _toDo(self, measurement):
        mapPalette = Include.sns.diverging_palette(10, 240, sep=10, as_cmap=True)
        Include.plt.figure(figsize=(15, 15), dpi=200)
        correlationChemistry = measurement.corr()
        Include.sns.heatmap(correlationChemistry, cmap=mapPalette, vmin=-1, vmax=1, annot=True)
        Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/image/CorrelationChemistry.png")
        # plt.show()
        # print(measurement.corr())
        return correlationChemistry

