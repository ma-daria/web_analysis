from analysis.static.analysis.pythonCode import Include, DentogramLSA, DentogramClustering, Correlation

class Data(object):
    data = Include.pd.DataFrame([])
    lsaData = DentogramLSA.DentogramLSA()
    clusteringData = DentogramClustering.DentogramClustering()
    correlationChemistryData = Correlation.Correlation()
    correlationZooplanktonData = Correlation.Correlation()
    type = 0

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Data, cls).__new__(cls)
        return cls.instance

    def newCl(self):
        self.data = Include.pd.DataFrame([])
        self.lsaData = DentogramLSA.DentogramLSA()
        self.clusteringData = DentogramClustering.DentogramClustering()
        self.correlationChemistryData = Correlation.Correlation()
        self.correlationZooplanktonData = Correlation.Correlation()
        type = 0

    def GetType(self):
        return self.type

    def SetType(self, t):
        self.type = t

    def GetData(self):
        return self.data

    def GetDataTable(self):
        meas = []
        measur = self.GetData()
        reservoir = measur['Водоем']
        date = measur['Дата']
        plase = measur['Место измерения']
        point = measur['Описание точки измерения']
        mass = measur['биомасса ФП']
        for i in range(len(reservoir)):
            meas.append([reservoir[i], date[i], plase[i], point[i], mass[i]])
        return meas

    def GetDataChemistry(self):
        d = self.GetData()
        return d.loc[:, 'О2':'Са+2']

    def GetDataZooplankton(self):
        d = self.GetData()
        return d.loc[:, 'Acroperus harpae (Baird)':'copepoditae Diaptomidae']

    def GetNameChemistry(self):
        d = self.GetDataChemistry()
        return d.columns

    def GetNameZooplankton(self):
        d = self.GetDataZooplankton()
        return d.columns

    def readFile(self, name):
        self.newCl()

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

    def CorrelationChemistry(self):
        d = self.GetDataChemistry()
        return self.correlationChemistryData.correlation(d)

    def CorrelationZooplankton(self):
        d = self.GetDataZooplankton()
        return self.correlationZooplanktonData.correlation(d)

    def clustering(self):
        d = self.GetDataZooplankton()
        return self.clusteringData.dentogram(d)

    def lsa(self):
        d = self.GetDataZooplankton()
        return self.lsaData.dentogram(d)

    def AnalysisCorrelationChemistry(self, name):
        cor = self.CorrelationChemistry()
        ress = self.correlationChemistryData.SortingCorrelation(cor[name])
        return self._createMas(ress)

    def AnalysisCorrelationZooplankton(self, name):
        cor = self.CorrelationZooplankton()
        ress = self.correlationZooplanktonData.SortingCorrelation(cor[name])
        return self._createMas(ress)


    def AnalysisClustering(self, names):
        id = self._Search(names)
        cl = self.clustering()
        col = self.GetNameZooplankton()
        return self.clusteringData.GropupClustering(cl, id, col.size, col)

    def AnalysisLSA(self, names):
        id = self._Search(names)
        cl = self.lsa()
        col = self.GetNameZooplankton()
        return self.lsaData.GropupClustering(cl, id, col.size, col)




    def _Search(self, names):
        col = self.GetNameZooplankton()
        i = 0
        for i in range(col.size):
            if col[i] == names:
                return i

    def _createMas(self, ress):
        ind = ress.index.tolist()
        res = ress.tolist()
        otvet = []
        for i in range(len(res)):
            otvet.append([ind[i], res[i]])
        return otvet

    def _ToFloat(self, measurement):
        for name in measurement:
            measurement[name] = Include.pd.to_numeric(measurement[name], errors='coerce')
        measurement = measurement.fillna(0)
        return measurement


    def drawCorrelation(self, fl):
        if fl == 0:
            return self.correlationChemistryData.getPhoto(10)
        else:
            return self.correlationZooplanktonData.getPhoto(25)

    def drawDentogram(self, fl):
        if fl == 0:
            return self.clusteringData.getPhoto()
        else:
            return self.lsaData.getPhoto()

