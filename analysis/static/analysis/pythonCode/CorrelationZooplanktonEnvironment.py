from analysis.static.analysis.pythonCode import Include, Correlation
from django.conf import settings

class CreateCorrelationZooplankton(Correlation.Correlation):
    def __init__(self):
        super().__init__()

    def toDoI(self, measurement, environment):
        mapPalette = Include.sns.diverging_palette(10, 240, sep=10, as_cmap=True)
        Include.plt.figure(figsize=(10, 20), dpi=200)
        test = measurement.corrwith(environment['О2'])
        teste = Include.pd.DataFrame(test)
        teste = teste.rename(columns={0: 'О2'})

        test = measurement.corrwith(environment['БПК5'])
        teste['БПК5'] = test

        test = measurement.corrwith(environment['НСО3–'])
        teste['НСО3–'] = test
        # teste = teste.fillna(0)
        Include.sns.heatmap(teste, cmap=mapPalette, vmin=-1, vmax=1)
        Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/image/СorrelationZooplanktonEnvironment.png")