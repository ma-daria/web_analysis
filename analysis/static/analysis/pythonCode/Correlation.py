from analysis.static.analysis.pythonCode import Include, Analysis

#  класс потомок класса Analysis, для алгоритма корреляции
class Correlation(Analysis.Analysis):
    # инициализация
    def __init__(self):
        super().__init__()

    # метод реализующий алгоритм корреляции
    def _toDo(selfm,  measurement, nameCol):
        return measurement.corr()

    # метод возврата данных
    def getData(self):
        return self.data

    # метод реализующий алгоритм упорядочения коррелируемых параметров по возрастанию в массиве (correlati)
    def SortingCorrelation(self, correlati):
        correlation_mod = correlati.abs()
        correlation_mod = correlation_mod.sort_values(ascending=False)
        for name in correlation_mod.index:
            correlation_mod[name] = correlati[name]
        return correlation_mod

    # метод реализующий генерацию матрицы корреляции
    def _draw(self, size, nameCol, component1, component2):
        mapPalette = Include.sns.diverging_palette(10, 240, sep=10, as_cmap=True)
        Include.plt.figure(figsize=(size, size), dpi=200)
        Include.sns.heatmap(self.data, cmap=mapPalette, vmin=-1, vmax=1)
        self.buffer = Include.io.BytesIO()
        Include.plt.savefig(self.buffer, format='png')

    # метод реализующий алгоритм получения параметров с высокой корреляцией
    def corMax(self):
        ma = self.data.copy()
        otv = Include.pd.DataFrame(columns=list([0, 1, 2]))
        Include.np.fill_diagonal(ma.values, 0)
        mod = ma.abs()
        i = 0
        while (mod.max()).max() >= 0.7:
            id1 = (mod.max()).idxmax()
            id2 = (mod.idxmax())[(mod.max()).idxmax()]
            otv.loc[i, 0] = id1
            otv.loc[i, 1] = id2
            otv.loc[i, 2] = Include.np.round_(ma.loc[id1, id2], 4)
            i = i + 1
            mod.loc[id1, id2] = 0
            mod.loc[id2, id1] = 0
        return otv