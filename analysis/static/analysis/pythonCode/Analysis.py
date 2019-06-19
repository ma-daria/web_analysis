from abc import abstractmethod
from analysis.static.analysis.pythonCode import Include

class Analysis(object):
    def __init__(self):
        self.data = Include.np.asarray([])
        self.buffer = []
        self.data_flag = 0


    def Analyze(self,  measurement, nameCol = ''):
        if self.data_flag == 0:
            self.data_flag = 1
            self.data = self._toDo(measurement, nameCol)
        return self.data

    @abstractmethod
    def _toDo(selfm,  measurement, nameCol):
        pass

    def getPhoto(self, size = 0, nameCol = '', component1 = 0, component2 = 0 ):
        if self.buffer == []:
            self._draw(size, nameCol, component1, component2)
        return self.buffer

    @abstractmethod
    def _draw(selfm, size, nameCol, component1, component2):
        pass