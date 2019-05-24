from analysis.static.analysis.pythonCode import Include
from django.conf import settings

def CreatePairplotChemistry(measurement):
    sns_plot = Include.sns.pairplot(measurement, hue='Место измерения')
    Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/image/pairplotPlace.png")

    sns_plot = Include.sns.pairplot(measurement, hue='Описание точки измерения')
    Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/image/pairplotPoint.png")

def CreateRegplotZooplankton(correlation):
    Include.np.fill_diagonal(correlation.values, -2)
    while (correlation.max()).max() > 0.8:
        id1 = (correlation.max()).idxmax()
        id2 = (correlation.idxmax())[(correlation.max()).idxmax()]
        print(id1, ' - ', id2, ' - ', (correlation.max()).max())
        correlation.loc[id1, id2] = -2
        correlation.loc[id2, id1] = -2



