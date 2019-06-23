from analysis.static.analysis.pythonCode import Include, ReadFileCSV

#  реализует работу с данными измерения
class Data(object):
    data = Include.pd.DataFrame([]) #DataFrame c исследуемыми данными
    list = [] #список параметров указанных вручную

    # метод вызывающий алгоритм чтения данных и предпроцессинг полученных данных
    def readFile(self, name):
        red = ReadFileCSV.ReadFileCSV()
        self.data = red.readFile(name)
        return self.data

    #  метод задания списока параметров указанных вручную
    def SetList(self, li):
        self.list = li

    # метод для получения списка параметров указанных вручную
    def GetList(self):
        return self.list

    #  метод получения всех данных исследования
    def GetData(self):
        return self.data

    #  метод получения данных для ионов
    def GetDataChemistry(self):
        d = self.GetData()
        return d.loc[:, 'pH':'Са+2']

    # метод для получения данных для всех видов зоопланктона
    def GetDataZooplankton(self):
        d = self.GetData()
        return d.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae']

    # метод получения данных для списка заданных параметров (name). Если  name=[], то за список берется list
    def GetDataMix(self, li = []):
        if li == []:
            li = self.list
        d = self.GetData()
        return d[li]

    # метод формирование данных для алгорима кластеризации по измерениям
    def GetDataChemistryRes(self):
        dd = self.GetData()
        d = self.GetDataChemistry()
        d = d.T
        cl = d.columns
        for col in cl:
            name = str(dd.loc[col, 'Водоем']) + '_' + str(dd.loc[col, 'Дата']) + '_' + str(dd.loc[col, 'Место измерения'])+ '_' + str(dd.loc[col, 'Описание точки измерения']) + '_' + str(dd.loc[col, 'pH'])  + '_' + str(Include.np.round_(dd.loc[col, 'Минерализация'], 4))
            d = d.rename(columns={col: name})
        return d

    # метод получения списка всех ионов
    def GetNameChemistry(self):
        d = self.GetDataChemistry()
        return d.columns

    # метод получения списка всех видов зоопланктона
    def GetNameZooplankton(self):
        d = self.GetDataZooplankton()
        return d.columns

    # метод получения списка всех параметров
    def GetNameAll(self):
        d = self.GetData()
        return d.columns

    # метод получения списка параметров для алгорима кластеризации по измерениям
    def GetNameChemistryRes(self):
        d = self.GetDataChemistryRes()
        return d.columns

    #  метод получения количества параметров данных
    def GetSizeData(self):
        d = self.GetData()
        return d.index.size

    # метод получения количества всех ионов
    def GetSizeChemistry(self):
        return self.GetNameChemistry().size

    # метод получения количества всех видов зоопланктона
    def GetSizeZooplankton(self):
        return self.GetNameZooplankton().size

    # метод получения количества параметров из списка list
    def GetSizeMix(self):
        return self.GetDataMix().size