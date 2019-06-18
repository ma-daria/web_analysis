from analysis.static.analysis.pythonCode import Include, DentogramLSA, DentogramClustering, Correlation, Data, Pairplot, GR_PCA, LDA

class Data_analysis(object):
    data = Data.Data()
    lsaData = DentogramLSA.DentogramLSA()
    clusteringData = DentogramClustering.DentogramClustering()
    clusteringChemistryData = DentogramClustering.DentogramClustering()
    pcaData = GR_PCA.GR_PCA()
    pcaLsaData = GR_PCA.GR_PCA()
    pcaChemistryData = GR_PCA.GR_PCA()
    correlationChemistryData = Correlation.Correlation()
    correlationZooplanktonData = Correlation.Correlation()
    correlationMixData = Correlation.Correlation()
    correlationLSAData = Correlation.Correlation()
    pairplotDescriptionData = Pairplot.Pairplot()
    pairplotPlaceData = Pairplot.Pairplot()
    ldaData= LDA.LDA()

    type = 0
    type_cla = 0
    list = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Data_analysis, cls).__new__(cls)
        return cls.instance

    def _newCl(self):
        self.data = Data.Data()
        self.lsaData = DentogramLSA.DentogramLSA()
        self.clusteringChemistryData = DentogramClustering.DentogramClustering()
        self.clusteringData = DentogramClustering.DentogramClustering()
        self.pcaData = GR_PCA.GR_PCA()
        self.pcaLsaData = GR_PCA.GR_PCA()
        self.pcaChemistryData = GR_PCA.GR_PCA()
        self.correlationChemistryData = Correlation.Correlation()
        self.correlationZooplanktonData = Correlation.Correlation()
        self.correlationMixData = Correlation.Correlation()
        self.correlationLSAData = Correlation.Correlation()
        self.pairplotDescriptionData = Pairplot.Pairplot()
        self.pairplotPlaceData = Pairplot.Pairplot()
        self.type = 0
        self.type_cla = 0
        self.list = []


    def SetType_cla(self, t):
        self.type_cla = t

    def SetList(self, li):
        self.list = li


    def GetType(self):
        return self.type

    def SetType(self, t):
        self.type = t

    def GetType_cla(self):
        return self.type_cla

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

    def GetNameChemistry(self):
        return self.data.GetNameChemistry()

    def GetNameZooplankton(self):
        return self.data.GetNameZooplankton()

    def GetNameAll(self):
        return self.data.GetNameAll()

    def GetNameChemistryRes(self):
        return self.data.GetNameChemistryRes()


    def readFile(self, name):
        self._newCl()
        return self.data.readFile(name)

    def Correlation(self, fl):

        if fl == 0:
            d = self.data.GetDataChemistry()
            otv = self.correlationChemistryData.correlation(d)
        else:
            if fl == 1:
                d = self.data.GetDataChemistry()
                otv = self.correlationZooplanktonData.correlation(d)
            else:
                if fl == 2:
                    d = self.data.GetDataChemistry()
                    self.correlationMixData = Correlation.Correlation()
                    otv = self.correlationMixData.correlation(d)
                    self.drawPairplotDescription()
                    self.drawPairplotPlace()
                else:
                    da = self.lsaData.GetMass()
                    db = Include.pd.DataFrame(Include.np.array(da))
                    name = self.data.GetNameZooplankton()
                    d = db
                    i = 0
                    for n in name:
                        d = d.rename(columns={i: n})
                        i = i + 1
                    otv = self.correlationLSAData.correlation(d)
        self.drawCorrelation(fl)
        return otv

    def Clustering(self, fl):
        otv = []
        if fl == 0:
            d = self.data.GetDataZooplankton()
            otv = self.clusteringData.dentogram(d)
        else:
            if fl == 1:
                d = self.data.GetDataZooplankton()
                otv = self.lsaData.dentogram(d)
            else:
                if fl == 2:
                    d = self.data.GetDataChemistryRes()
                    otv = self.clusteringChemistryData.dentogram(d)
        self.drawDentogram(fl)
        self.pca(fl)
        return otv



    def pca(self, fl):
        if fl == 0:
            d = self.data.GetDataZooplankton()
            d['pH'] = self.data.GetDataMix(['pH'])
            self.pcaData.gr_pca(d, 'pH')
        else:
            if fl == 1:
                d = self.data.GetDataZooplankton()
                d['pH'] = self.data.GetDataMix(['pH'])
                self.pcaLsaData.gr_pca(d, 'pH')
            else:
                if fl == 2:
                    d = self.data.GetDataChemistryRes()
                    # d['pH'] = self.data.GetDataMix(['pH'])
                    d['pH'] = Include.pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 1])
                    self.pcaChemistryData.gr_pca(d, 'pH')
        self.drawPCA(fl)



    def AnalysisCorrelationChemistry(self, name):
        cor = self.Correlation(0)
        ress = self.correlationChemistryData.SortingCorrelation(cor[name])
        ress = Include.np.round_(ress, 4)
        return self._createMas(ress)

    def AnalysisCorrelationZooplankton(self, name):
        cor = self.Correlation(1)
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
        cl = self.Clustering(0)
        col = self.data.GetNameZooplankton()
        id = self._Search(names, col)
        return self.clusteringData.GropupClustering(cl, id, col.size, col)

    def AnalysisLSA(self, names):
        cl = self.Clustering(1)
        col = self.data.GetNameZooplankton()
        id = self._Search(names, col)
        return self.lsaData.GropupClustering(cl, id, col.size, col)

    def AnalysisClusteringChemistry(self, names):
        cl = self.Clustering(2)
        col = self.data.GetNameChemistryRes()
        id = self._Search(names, col)
        return self.clusteringChemistryData.GropupClustering(cl, id, col.size, col)

    def GroupLSA(self, val):
        cl = self.Clustering(1)
        col = self.data.GetNameZooplankton()
        return self.lsaData.Group(cl, val, col.size, col)

    def GroupClustering(self, val):
        cl = self.Clustering(0)
        col = self.data.GetNameZooplankton()
        return self.clusteringData.Group(cl, val, col.size, col)

    def GroupClusteringChemistry(self, val):
        cl = self.Clustering(2)
        col = self.data.GetNameChemistryRes()
        return self.clusteringChemistryData.Group(cl, val, col.size, col)

    def LDA(self):
        d = self.data.GetDataZooplankton()
        self.ldaData.lda(d)

    def NAnalysisLDA(self):
        col = self.data.GetNameZooplankton()
        return self.ldaData.group_n(col)

    def AnalysisLDA(self, val):
        col = self.data.GetNameZooplankton()
        return self.ldaData.group(col, val)



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
            return self.clusteringData.getPhoto(0.5)
        else:
            if fl == 1:
                return self.lsaData.getPhoto(0.2)
            else:
                if fl == 2:
                    return self.clusteringChemistryData.getPhoto(0.021)

    def drawPairplotDescription(self):
        dat = self.data.GetDataMix(self.list)
        dat['Описание точки измерения'] = self.data.GetDataMix(['Описание точки измерения'])
        return self.pairplotDescriptionData.getPhoto(dat, 'Описание точки измерения')

    def drawPairplotPlace(self):
        dat = self.data.GetDataMix(self.list)
        dat['Место измерения'] = self.data.GetDataMix(['Место измерения'])
        return self.pairplotPlaceData.getPhoto(dat, 'Место измерения')

    def drawPCA(self, fl):
        if fl == 0:
            name = self.data.GetNameZooplankton()
            return self.pcaData.getPhoto(name, 0, 1, [-0.5, 0.5, -0.04, 0.35])
        else:
            if fl == 1:
                name = self.data.GetNameZooplankton()
                return self.pcaLsaData.getPhoto(name, 0, 1, [-0.5, 0.5, -0.04, 0.35])
            else:
                name = self.data.GetNameChemistryRes()
                return self.pcaChemistryData.getPhoto(name, 0, 1, [-0.6, 0.6, 0.02, 0.115])


