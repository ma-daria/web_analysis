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






otvet = []

def Save(clustering, id, size, col):
    if size > id:
        # print(int(id))
        return str(col[int(id)])+", "
        # print(col[int(id)])
    else:
        st = Save(clustering, clustering.iloc[id - size, 0], size, col)
        st = st + Save(clustering, clustering.iloc[id - size, 1], size, col)
        return st

def GropupClustering(Z, id, size, col):
    ZZ = Include.pd.DataFrame(Z)
    ZZ[0] = ZZ[0].astype(Include.np.int64)
    ZZ[1] = ZZ[1].astype(Include.np.int64)
    mas = Include.pd.Series([])
    for i in range(ZZ[0].size):
        mas[i] = i
    ZZ['id'] = mas
    global otvet
    otvet = []
    Bypass(ZZ, id, size, col)
    return otvet

def Bypass(clustering, id, size, col):
    str = clustering[clustering[0] == id]
    if str.size == 0:
        str = clustering[clustering[1] == id]
        if str.size == 0:
            return ""
        id2 = 0
    else:
        id2 = 1
    # print("\nГруппа")
    st = ""
    if size <= id:
        st = Save(clustering, clustering.iloc[id - size, 0], size, col)
        st= st + Save(clustering, clustering.iloc[id - size, 1], size, col)
    else:
        st = Save(clustering,id, size, col)

    st = st + Save(clustering, str.iloc[0, id2], size, col)
    otvet.append(st)
    Bypass(clustering, int(str['id'])+size, size, col)
