from analysis.static.analysis.pythonCode import Include
from django.conf import settings
class GR_PCA(object):

    def __init__(self):
        self.pca = Include.PCA()
        self.X_pca = []
        self.c = []
        self.flag = 0
        self.buffer = []

    def gr_pca(self, df1, colorField):
        if self.flag == 0:
            self._toDo(df1, colorField)

    def _toDo(self, df1, colorField):
        X = df1.drop(columns=[colorField])
        y = df1[colorField].copy()
        scaler = Include.StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)
        self.X_pca = self.pca.fit_transform(X)
        self.c = Include.np.asarray(y)

    def getPhoto(self, col, component1, component2):
        if self.buffer == []:
            self._draw(col, component1, component2)
        return self.buffer

    def _draw(self, col, component1, component2):
        coeff = Include.np.transpose(self.pca.components_[[component1 - 1, component2 - 1], :])
        Include.plt.figure(figsize=(16, 16))
        Include.plt.xlim(-0.75, 0.75)
        Include.plt.ylim(-0.75, 0.75)
        Include.plt.xlabel("PC{}".format(component1))
        Include.plt.ylabel("PC{}".format(component2))
        Include.plt.grid()

        self._biplot(self.X_pca[:, [component1 - 1, component2 - 1]], coeff, col, self.c)

        self.buffer = Include.io.BytesIO()
        Include.plt.savefig(self.buffer, format='png')
        Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/img/test.png")

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