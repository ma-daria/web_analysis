from analysis.static.analysis.pythonCode import Include


class Data(object):
    data = Include.pd.DataFrame([])

    def readFile(self, name):
        measurement = Include.pd.read_csv(name, sep=';', decimal=',', header=1)
        measurement = measurement.rename(columns={'Unnamed: 0': 'Водоем'})
        measurement = measurement.rename(columns={'Unnamed: 1': 'Дата'})
        measurement = measurement.rename(columns={'Unnamed: 2': 'Место измерения'})
        measurement = measurement.rename(columns={'Unnamed: 3': 'Описание точки измерения'})
        measurement = measurement.rename(columns={'Unnamed: 4': 'pH'})
        measurement = measurement.rename(columns={'Unnamed: 5': 'Минерализация'})
        measurement = measurement.rename(columns={'Unnamed: 6': 't'})
        measurement = measurement.rename(columns={'Unnamed: 16': 'биомасса ФП'})

        measurement.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'] = self._ToFloat(
            measurement.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae'])

        new_measurement = measurement
        for number in measurement.columns:
            if measurement[number].dtypes == 'float64':
                if measurement[number].sum() == 0:
                    del new_measurement[number]
        measurement = new_measurement

        for number in measurement.columns:
            measurement = measurement.rename(columns={number: number.strip()})
        self.data = measurement
        return self.data

    def _ToFloat(self, measurement):
        for name in measurement:
            measurement[name] = Include.pd.to_numeric(measurement[name], errors='coerce')
        measurement = measurement.fillna(0)
        return measurement



    def GetData(self):
        return self.data


    def GetDataChemistry(self):
        d = self.GetData()
        return d.loc[:, 'О2':'Са+2']

    def GetDataZooplankton(self):
        d = self.GetData()
        return d.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae']

    def GetDataMix(self, name):
        d = self.GetData()
        return d[name]


    def GetNameChemistry(self):
        d = self.GetDataChemistry()
        return d.columns

    def GetNameZooplankton(self):
        d = self.GetDataZooplankton()
        return d.columns

    def GetNameAll(self):
        d = self.GetData()
        return d.columns

    def GetSizeData(self):
        d = self.GetData()
        return d.index.size

    def GetSizeChemistry(self):
        return self.GetNameChemistry().size

    def GetSizeZooplankton(self):
        return self.GetNameZooplankton().size