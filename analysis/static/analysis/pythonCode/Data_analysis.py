from analysis.static.analysis.pythonCode import Include, DentogramLSA, DentogramClustering, Correlation, Data, Pairplot

class Data_analysis(object):
    data = Data.Data()
    lsaData = DentogramLSA.DentogramLSA()
    clusteringData = DentogramClustering.DentogramClustering()
    clusteringChemistryData = DentogramClustering.DentogramClustering()
    correlationChemistryData = Correlation.Correlation()
    correlationZooplanktonData = Correlation.Correlation()
    correlationMixData = Correlation.Correlation()
    correlationLSAData = Correlation.Correlation()
    pairplotDescriptionData = Pairplot.Pairplot()
    pairplotPlaceData = Pairplot.Pairplot()

    type = 0
    type_cla = 0
    list = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Data_analysis, cls).__new__(cls)
        return cls.instance

    def newCl(self):
        self.data = Data.Data()
        self.lsaData = DentogramLSA.DentogramLSA()
        self.lsaChemistryData = DentogramLSA.DentogramLSA()
        self.clusteringChemistryData = DentogramClustering.DentogramClustering()
        self.clusteringData = DentogramClustering.DentogramClustering()
        self.correlationChemistryData = Correlation.Correlation()
        self.correlationZooplanktonData = Correlation.Correlation()
        self.correlationMixData = Correlation.Correlation()
        self.correlationLSAData = Correlation.Correlation()
        self.pairplotDescriptionData = Pairplot.Pairplot()
        self.pairplotPlaceData = Pairplot.Pairplot()
        self.type = 0
        self.type_cla = 0
        self.list = []

    def GetType(self):
        return self.type

    def SetType(self, t):
        self.type = t

    def GetType_cla(self):
        return self.type_cla

    def SetType_cla(self, t):
        self.type_cla = t


    def GetDataTable(self):
        meas = []
        measur = self.data.GetData()
        reservoir = measur['Водоем']
        date = measur['Дата']
        plase = measur['Место измерения']
        point = measur['Описание точки измерения']
        mass = measur['биомасса ФП']
        for i in range(len(reservoir)):
            meas.append([reservoir[i], date[i], plase[i], point[i], mass[i]])
        return meas

    def GetSizeData(self):
        return self.data.GetSizeData()

    def GetSizeChemistry(self):
        return self.data.GetSizeChemistry()

    def GetSizeZooplankton(self):
        return self.data.GetSizeZooplankton()

    def GetSizeMix(self):
        return len(self.list)


    def GetList(self):
        return self.list

    def SetList(self, li):
        self.list = li


    def readFile(self, name):
        self.newCl()
        return self.data.readFile(name)

    def GetNameChemistry(self):
        return self.data.GetNameChemistry()

    def GetNameZooplankton(self):
        return self.data.GetNameZooplankton()

    def GetNameAll(self):
        return self.data.GetNameAll()

    def GetNameChemistryRes(self):
        return self.data.GetNameChemistryRes()

    def CorrelationChemistry(self):
        d = self.data.GetDataChemistry()
        otv = self.correlationChemistryData.correlation(d)
        self.drawCorrelation(0)
        return otv

    def CorrelationZooplankton(self):
        d = self.data.GetDataZooplankton()
        otv = self.correlationZooplanktonData.correlation(d)
        self.drawCorrelation(1)
        return otv

    def CorrelationMix(self, name):
        d = self.data.GetDataMix(name)
        self.correlationMixData = Correlation.Correlation()
        otv = self.correlationMixData.correlation(d)
        self.drawCorrelation(2)
        self.drawPairplotDescription()
        self.drawPairplotPlace()
        return otv

    def CorrelationLSA(self):
        da = self.lsaData.GetMass()
        db = Include.pd.DataFrame(Include.np.array(da))
        name = self.data.GetNameZooplankton()
        d = db
        i = 0
        for n in name:
            d = d.rename(columns={i: n})
            i = i + 1
        otv = self.correlationLSAData.correlation(d)
        self.drawCorrelation(3)
        return otv

    def clustering(self):
        d = self.data.GetDataZooplankton()
        otv = self.clusteringData.dentogram(d)
        self.drawDentogram(0)
        return otv

    def lsa(self):
        d = self.data.GetDataZooplankton()
        otv = self.lsaData.dentogram(d)
        self.drawDentogram(1)
        return otv

    def clusteringChemistry(self):
        d = self.data.GetDataChemistryRes()
        otv = self.clusteringChemistryData.dentogram(d)
        self.drawDentogram(2)
        return otv





    def AnalysisCorrelationChemistry(self, name):
        cor = self.CorrelationChemistry()
        ress = self.correlationChemistryData.SortingCorrelation(cor[name])
        ress = Include.np.round_(ress, 4)
        return self._createMas(ress)

    def AnalysisCorrelationZooplankton(self, name):
        cor = self.CorrelationZooplankton()
        ress = self.correlationZooplanktonData.SortingCorrelation(cor[name])
        ress = Include.np.round_(ress, 4)
        return self._createMas(ress)

    def AnalysisCorrelationMix(self, name):
        cor = self.correlationMixData.getData()
        ress = self.correlationMixData.SortingCorrelation(cor[name])
        ress = Include.np.round_(ress, 4)
        return self._createMas(ress)

    def CorrelationMaxChemistry(self):
        ress = self.correlationChemistryData.corMax()
        return self._createMasMax(ress)

    def CorrelationMaxZooplankton(self):
        ress = self.correlationZooplanktonData.corMax()
        return self._createMasMax(ress)

    def CorrelationMaxMix(self):
        ress = self.correlationMixData.corMax()
        return self._createMasMax(ress)

    def AnalysisClustering(self, names):
        cl = self.clustering()
        col = self.data.GetNameZooplankton()
        id = self._Search(names, col)
        return self.clusteringData.GropupClustering(cl, id, col.size, col)

    def AnalysisLSA(self, names):
        cl = self.lsa()
        col = self.data.GetNameZooplankton()
        id = self._Search(names, col)
        return self.lsaData.GropupClustering(cl, id, col.size, col)

    def GroupLSA(self, val):
        cl = self.lsa()
        col = self.data.GetNameZooplankton()
        return self.lsaData.Group(cl, val, col.size, col)

    def GroupClustering(self, val):
        cl = self.clustering()
        col = self.data.GetNameZooplankton()
        return self.clusteringData.Group(cl, val, col.size, col)

    def GroupClusteringChemistry(self, val):
        cl = self.clusteringChemistry()
        col = self.data.GetNameChemistryRes()
        return self.clusteringChemistryData.Group(cl, val, col.size, col)


    def AnalysisClusteringChemistry(self, names):
        cl = self.clusteringChemistry()
        col = self.data.GetNameChemistryRes()
        id = self._Search(names, col)
        return self.clusteringChemistryData.GropupClustering(cl, id, col.size, col)



    def _Search(self, names, col):
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

    def _createMasMax(self, ress):
        res = ress[0].tolist()
        res1 = ress[1].tolist()
        res2 = ress[2].tolist()
        otvet = []
        for i in range(len(res)):
            otvet.append([res[i], res1[i], res2[i]])
        return otvet



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
            if fl == 1:
                return self.lsaData.getPhoto()
            else:
                if fl == 2:
                    return self.clusteringChemistryData.getPhoto()

    def drawPairplotDescription(self):
        dat = self.data.GetDataMix(self.list)
        dat['Описание точки измерения'] = self.data.GetDataMix(['Описание точки измерения'])
        return self.pairplotDescriptionData.pairplot(dat, 'Описание точки измерения')

    def drawPairplotPlace(self):
        dat = self.data.GetDataMix(self.list)
        dat['Место измерения'] = self.data.GetDataMix(['Место измерения'])
        return self.pairplotPlaceData.pairplot(dat, 'Место измерения')

