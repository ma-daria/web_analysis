from abc import abstractmethod
from analysis.static.analysis.pythonCode import Include

#  класс для реализации алгоритмов анализа данных
class Analysis(object):
    def __init__(self):
        self.data = Include.pd.DataFrame([]) # результаты реализации алгоритма анализа
        self.buffer = [] #график получены в результате работы алгоритмов
        self.data_flag = 0 #флаг использования алгоритма

    # метод запуска алгоритма и возврата данны работы
    def Analyze(self,  measurement, nameCol = ''):
        if self.data_flag == 0:
            self.data_flag = 1
            self.data = self._toDo(measurement, nameCol)
        return self.data

    # метод реализующий алгоритм анализа
    @abstractmethod
    def _toDo(selfm,  measurement, nameCol):
        pass

    # метод запуска генерации графика
    def getPhoto(self, size = 0, nameCol = '', component1 = 0, component2 = 0 ):
        if self.buffer == []:
            self._draw(size, nameCol, component1, component2)
        return self.buffer

    # метод реализующий генерацию графика
    @abstractmethod
    def _draw(selfm, size, nameCol, component1, component2):
        pass