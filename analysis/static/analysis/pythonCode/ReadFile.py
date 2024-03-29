from analysis.static.analysis.pythonCode import Include
from abc import abstractmethod

# класс работы с чтением и предпроцессингом данных исследования
class ReadFile(object):
    # инициализация
    def __init__(self):
        self.measurement = Include.pd.DataFrame([]) #данные чтения

    # метод с последовательностью выполнения шагов для чтения и предпроцессинга
    def readFile(self, name):
        self._OpenFile(name)
        self.measurement.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'] = self._ToFloat(
            self.measurement.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'])
        self._ClearData()
        return self.measurement

    # метод открытия файла
    @abstractmethod
    def _OpenFile(self, name):
        pass

    #  метод приведения типов данных
    def _ToFloat(self, data):
        for name in data:
            data[name] = Include.pd.to_numeric(data[name], errors='coerce')
        data = data.fillna(0)
        return data

    # метод очистки от факторов, снижающих качество данных
    def _ClearData(self):
        new_measurement = self.measurement
        for number in self.measurement.columns:
            if self.measurement[number].dtypes == 'float64':
                if self.measurement[number].sum() == 0:
                    del new_measurement[number]
        self.measurement = new_measurement

        for number in self.measurement.columns:
            self.measurement = self.measurement.rename(columns={number: number.strip()})

        self.measurement.loc[self.measurement[
                            'Описание точки измерения'] == "заросли тростника, рогоза, погружен раст", 'Описание точки измерения'] = "заросли"