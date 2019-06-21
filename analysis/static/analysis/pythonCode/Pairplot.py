from analysis.static.analysis.pythonCode import Include, Analysis

class Pairplot(Analysis.Analysis):
    name = ''

    def __init__(self):
        super().__init__()

    def _toDo(selfm,  measurement, nameCol):
        selfm.name = nameCol
        return measurement

    def _draw(self,  size, nameCol, component1, component2):
        self.buffer = Include.io.BytesIO()
        sns_plot = Include.sns.pairplot(self.data, hue=self.name)
        sns_plot.savefig(self.buffer, format='png')