from analysis.static.analysis.pythonCode import Include, Analysis

class Pairplot(Analysis.Analysis):
    name = ''

    def __init__(self):
        super().__init__()
        # self.buffer= []
        # self.flag = 0

    # def getPhoto(self, dat, name):
    #     if self.flag == 0:
    #         self.flag = 1
    #         self._draw(dat, name)
    #     return self.buffer
    def _toDo(selfm,  measurement, nameCol):
        selfm.name = nameCol
        return measurement

    def _draw(self,  size, nameCol, component1, component2):
        self.buffer = Include.io.BytesIO()
        sns_plot = Include.sns.pairplot(self.data, hue=self.name)
        sns_plot.savefig(self.buffer, format='png')