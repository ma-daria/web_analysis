from analysis.static.analysis.pythonCode import Include, DentogramLSA, DentogramClustering, Correlation

class Data(object):
    data = Include.pd.DataFrame([])
    lsaData = DentogramLSA.DentogramLSA()
    clusteringData = DentogramClustering.DentogramClustering()
    correlationChemistryData = Correlation.Correlation()
    correlationZooplanktonData = Correlation.Correlation()
    correlationMixData = Correlation.Correlation()
    correlationLSAData = Correlation.Correlation()
    type = 0
    list = []

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
        self.correlationMixData = Correlation.Correlation()
        self.correlationLSAData = Correlation.Correlation()
        self.type = 0
        self.list = []

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

    def GetDataMix(self, name):
        d = self.GetData()
        return d[name]

    def GetNameChemistry(self):
        d = self.GetDataChemistry()
        return d.columns

    def GetNameZooplankton(self):
        d = self.GetDataZooplankton()
        return d.columns

    def GetList(self):
        return self.list

    def SetList(self, li):
        self.list = li


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

    def CorrelationMix(self, name):
        d = self.GetDataMix(name)
        self.correlationMixData = Correlation.Correlation()
        return self.correlationMixData.correlation(d)

    def CorrelationLSA(self):
        da = self.lsaData.GetMass()
        db = Include.pd.DataFrame(Include.np.array(da))
        name = self.GetNameZooplankton()
        d = db
        i = 0
        for n in name:
            d = d.rename(columns={i: n})
            i = i + 1
        return self.correlationLSAData.correlation(d)

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

    def AnalysisCorrelationMix(self, name):
        cor = self.correlationMixData.getData()
        ress = self.correlationMixData.SortingCorrelation(cor[name])
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
            if fl == 1:
                return self.correlationZooplanktonData.getPhoto(25)
            else:
                if fl == 2:
                    return self.correlationMixData.getPhoto(15)
                else:
                    return self.correlationLSAData.getPhoto(20)



    def drawDentogram(self, fl):
        if fl == 0:
            return self.clusteringData.getPhoto()
        else:
            return self.lsaData.getPhoto()

    def drawPairplot(self):
        dat = self.data[ self.list]
        dat[ 'Описание точки измерения'] = self.data['Описание точки измерения']
        sns_plot = Include.sns.pairplot(dat, hue='Описание точки измерения')
        buffer = Include.io.BytesIO()
        sns_plot.savefig(buffer, format='png')
        return buffer

    def drawPairplot2(self):
        dat = self.data[ self.list]
        dat[ 'Место измерения'] = self.data['Место измерения']
        sns_plot = Include.sns.pairplot(dat, hue='Место измерения')
        buffer = Include.io.BytesIO()
        sns_plot.savefig(buffer, format='png')
        return buffer

