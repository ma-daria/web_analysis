from analysis.static.analysis.pythonCode import Include, ReadFileCSV

class Data(object):
    data = Include.pd.DataFrame([])
    list = []

    def readFile(self, name):
        red = ReadFileCSV.ReadFileCSV()
        self.data = red.readFile(name)
        return self.data

    def _ToFloat(self, measurement):
        for name in measurement:
            measurement[name] = Include.pd.to_numeric(measurement[name], errors='coerce')
        measurement = measurement.fillna(0)
        return measurement

    def SetList(self, li):
        self.list = li

    def GetList(self):
        return self.list

    def GetData(self):
        return self.data

    def GetDataChemistry(self):
        d = self.GetData()
        return d.loc[:, 'О2':'Са+2']

    def GetDataZooplankton(self):
        d = self.GetData()
        return d.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae']

    def GetDataMix(self, li = []):
        if li == []:
            li = self.list
        d = self.GetData()
        return d[li]

    def GetDataChemistryRes(self):
        dd = self.GetData()
        d = self.GetDataChemistry()
        d = d.T
        cl = d.columns
        for col in cl:
            name = str(dd.loc[col, 'Водоем']) + '_' + str(dd.loc[col, 'Дата']) + '_' + str(dd.loc[col, 'Место измерения'])+ '_' + str(dd.loc[col, 'Описание точки измерения'])
            d = d.rename(columns={col: name})
        return d

    def GetNameChemistry(self):
        d = self.GetDataChemistry()
        return d.columns

    def GetNameZooplankton(self):
        d = self.GetDataZooplankton()
        return d.columns

    def GetNameAll(self):
        d = self.GetData()
        return d.columns

    def GetNameChemistryRes(self):
        d = self.GetDataChemistryRes()
        return d.columns

    def GetSizeData(self):
        d = self.GetData()
        return d.index.size

    def GetSizeChemistry(self):
        return self.GetNameChemistry().size

    def GetSizeZooplankton(self):
        return self.GetNameZooplankton().size

    def GetSizeMix(self):
        return self.GetDataMix().size