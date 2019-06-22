from analysis.static.analysis.pythonCode import Include, Analysis

# класс потомок класса Analysis, для алгоритма построения попарных диаграмм рассеяния
class Pairplot(Analysis.Analysis):
    name = '' #название данных, по которым будет происходить покраска точек

    # инициализация
    def __init__(self):
        super().__init__()

    # метод подготовки данных
    def _toDo(selfm,  measurement, nameCol):
        selfm.name = nameCol
        return measurement

    # метод построение попарных диаграмм рассеяния
    def _draw(self,  size, nameCol, component1, component2):
        self.buffer = Include.io.BytesIO()
        sns_plot = Include.sns.pairplot(self.data, hue=self.name)
        sns_plot.savefig(self.buffer, format='png')