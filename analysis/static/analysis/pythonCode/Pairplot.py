from analysis.static.analysis.pythonCode import Include

class Pairplot(object):
    def __init__(self):
        self.buffer= Include.io.BytesIO()
        self.flag = 0

    def getPhoto(self, dat, name):
        if self.flag == 0:
            self.flag = 1
            self._drаw(dat, name)
        return self.buffer

    def _drаw(self, dat, name):
        print(name)
        sns_plot = Include.sns.pairplot(dat, hue=name)
        sns_plot.savefig(self.buffer, format='png')