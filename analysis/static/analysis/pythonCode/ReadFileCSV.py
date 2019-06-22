from analysis.static.analysis.pythonCode import Include, ReadFile

# класс потомок класса ReadFile для чтения CSV файлов
class ReadFileCSV(ReadFile.ReadFile):
    def __init__(self):
        super().__init__()

    # метод открытия файла csv
    def _OpenFile(self, name):
        self.measurement = Include.pd.read_csv(name, sep=';', decimal=',', header=1)
        self.measurement = self.measurement.rename(columns={'Unnamed: 0': 'Водоем'})
        self.measurement = self.measurement.rename(columns={'Unnamed: 1': 'Дата'})
        self.measurement = self.measurement.rename(columns={'Unnamed: 2': 'Место измерения'})
        self.measurement = self.measurement.rename(columns={'Unnamed: 3': 'Описание точки измерения'})
        self.measurement = self.measurement.rename(columns={'Unnamed: 4': 'pH'})
        self.measurement = self.measurement.rename(columns={'Unnamed: 5': 'Минерализация'})
        self.measurement = self.measurement.rename(columns={'Unnamed: 6': 't'})
        self.measurement = self.measurement.rename(columns={'Unnamed: 16': 'биомасса ФП'})