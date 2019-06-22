from analysis.static.analysis.pythonCode import Include, Analysis

# класс потомок класса Analysis, для алгоритма метода главных компонент
class GR_PCA(Analysis.Analysis):
    X_pca = [] #результаты работы алгоритма
    c = [] #массив по которому будет происходить окрашивание точек

    #  инициализация
    def __init__(self):
        super().__init__()

    # метод реализующий алгоритм  метод главных компонент
    def _toDo(self, df1, colorField):
        self.data = Include.PCA()
        X = df1.drop(columns=[colorField])
        y = df1[colorField].copy()
        scaler = Include.StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)
        self.X_pca = self.data.fit_transform(X)
        self.c = Include.np.asarray(y)
        return self.data

    # метод реализующий генерацию графика
    def _draw(self, size, nameCol, component1, component2):
        coeff = Include.np.transpose(self.data.components_[[component1 - 1, component2 - 1], :])
        Include.plt.figure(figsize=(16, 16))
        Include.plt.xlim(size[0], size[1])
        Include.plt.ylim(size[2], size[3])
        Include.plt.xlabel("PC{}".format(component1))
        Include.plt.ylabel("PC{}".format(component2))
        Include.plt.grid()
        self._biplot(self.X_pca[:, [component1 - 1, component2 - 1]], coeff, nameCol, self.c)
        self.buffer = Include.io.BytesIO()
        Include.plt.savefig(self.buffer, format='png')

    # вспомогательный метод построения графика
    def _biplot(self, score, coeff, labels=None, colors=None):
        xs = score[:, 0]
        ys = score[:, 1]
        n = coeff.shape[0]
        scalex = 1.0 / (xs.max() - xs.min())
        scaley = 1.0 / (ys.max() - ys.min())
        Include.plt.scatter(xs * scalex, ys * scaley, c=colors)
        Include.plt.colorbar()
        for i in range(n):
            Include.plt.arrow(0, 0, coeff[i, 0], coeff[i, 1], color='r', alpha=0.2)
            if labels is None:
                Include.plt.text(coeff[i, 0] * 1.15, coeff[i, 1] * 1.15, "Var" + str(i + 1), color='g', ha='center', va='center')
            else:
                Include.plt.text(coeff[i, 0] * 1.15, coeff[i, 1] * 1.15, labels[i], color='g', ha='center', va='center')