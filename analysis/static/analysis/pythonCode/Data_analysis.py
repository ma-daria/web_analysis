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
    # list = []

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
        # self.list = []


    def SetType_cla(self, t):
        self.type_cla = t

    def SetList(self, li):
        # self.list = li
        self.data.SetList(li)


    def GetType(self):
        return self.type

    def SetType(self, t):
        self.type = t

    def GetType_cla(self):
        return self.type_cla

    def GetData(self):
        return self.data

    # def GetList(self):
    #     return self.list

    def ReadFile(self, name):
        self._newCl()
        return self.data.readFile(name)

    def Correlation(self):

        if self.type == 0:
            d = self.data.GetDataChemistry()
            otv = self.correlationChemistryData.Analyze(d)
            # otv = self.correlationChemistryData.correlation(d)
        else:
            if self.type == 1:
                d = self.data.GetDataZooplankton()
                otv = self.correlationZooplanktonData.Analyze(d)
                # otv = self.correlationZooplanktonData.correlation(d)
            else:
                if self.type == 2:
                    d = self.data.GetDataMix()
                    self.correlationMixData = Correlation.Correlation()
                    otv = self.correlationMixData.Analyze(d)
                    # otv = self.correlationMixData.correlation(d)
                    self.drawPairplot(Include.PA_DESCRIPTION)
                    self.drawPairplot(Include.PA_PLACE)
                else:
                    da = self.lsaData.GetMass()
                    db = Include.pd.DataFrame(Include.np.array(da))
                    name = self.data.GetNameZooplankton()
                    d = db
                    i = 0
                    for n in name:
                        d = d.rename(columns={i: n})
                        i = i + 1
                    otv = self.correlationLSAData.Analyze(d)
                    # otv = self.correlationLSAData.correlation(d)
        self.drawCorrelation()
        return otv

    def Clustering(self):
        otv = []
        if self.type_cla == 0:
            d = self.data.GetDataZooplankton()
            otv = self.clusteringData.Analyze(d)
            # otv = self.clusteringData.dentogram(d)
        else:
            if self.type_cla == 1:
                d = self.data.GetDataZooplankton()
                otv = self.lsaData.Analyze(d)
                # otv = self.lsaData.dentogram(d)
            else:
                if self.type_cla == 2:
                    d = self.data.GetDataChemistryRes()
                    otv = self.clusteringChemistryData.Analyze(d)
                    # otv = self.clusteringChemistryData.dentogram(d)
        self.drawDentogram()
        self.PCA()
        return otv



    def PCA(self):
        if self.type_cla == 0:
            d = self.data.GetDataZooplankton()
            d['pH'] = self.data.GetDataMix(['pH'])
            self.pcaData.Analyze(d, 'pH')
            # self.pcaData.gr_pca(d, 'pH')
        else:
            if self.type_cla == 1:
                d = self.data.GetDataZooplankton()
                d['pH'] = self.data.GetDataMix(['pH'])
                self.pcaLsaData.Analyze(d, 'pH')
                # self.pcaLsaData.gr_pca(d, 'pH')
            else:
                if self.type_cla == 2:
                    d = self.data.GetDataChemistryRes()
                    # d['pH'] = self.data.GetDataMix(['pH'])
                    d['pH'] = Include.pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 1])
                    self.pcaChemistryData.Analyze(d, 'pH')
                    # self.pcaChemistryData.gr_pca(d, 'pH')
        self.drawPCA()


    def AnalysisCorrelation(self, name):
        ress = []
        if self.type == 0:
            cor = self.Correlation()
            ress = self.correlationChemistryData.SortingCorrelation(cor[name])
        else:
            if self.type == 1:
                cor = self.Correlation()
                ress = self.correlationZooplanktonData.SortingCorrelation(cor[name])
            else:
                if self.type == 2:
                    cor = self.correlationMixData.getData()
                    ress = self.correlationMixData.SortingCorrelation(cor[name])
        ress = Include.np.round_(ress, 4)
        return self._createMas(ress)

    def CorrelationMax(self):
        ress = []
        if self.type == 0:
            ress = self.correlationChemistryData.corMax()
        else:
            if self.type == 1:
                ress = self.correlationZooplanktonData.corMax()
            else:
                if self.type == 2:
                    ress = self.correlationMixData.corMax()
        return self._createMasMax(ress)


    def AnalysisClustering(self, names):
        cl = self.Clustering()
        if self.type_cla == 0:
            col = self.data.GetNameZooplankton()
            id = self._Search(names, col)
            return self.clusteringData.GropupClustering(cl, id, col.size, col)
        else:
            if self.type_cla == 1:
                col = self.data.GetNameZooplankton()
                id = self._Search(names, col)
                return self.lsaData.GropupClustering(cl, id, col.size, col)
            else:
                if self.type_cla == 2:
                    col = self.data.GetNameChemistryRes()
                    id = self._Search(names, col)
                    return self.clusteringChemistryData.GropupClustering(cl, id, col.size, col)

    def GroupClustering(self, val):
        cl = self.Clustering()
        if self.type_cla == 0:
            col = self.data.GetNameZooplankton()
            return self.clusteringData.Group(cl, val, col.size, col)
        else:
            if self.type_cla == 1:
                col = self.data.GetNameZooplankton()
                return self.lsaData.Group(cl, val, col.size, col)
            else:
                if self.type_cla == 2:
                    col = self.data.GetNameChemistryRes()
                    return self.clusteringChemistryData.Group(cl, val, col.size, col)



    def LDA(self):
        d = self.data.GetDataZooplankton()
        self.ldaData.Analyze(d)
        # self.ldaData.lda(d)

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


    def drawCorrelation(self):
        if self.type == 0:
            return self.correlationChemistryData.getPhoto(size=10)
        else:
            if self.type == 1:
                return self.correlationZooplanktonData.getPhoto(size=25)
            else:
                if self.type == 2:
                    return self.correlationMixData.getPhoto(size=15)
                else:
                    return self.correlationLSAData.getPhoto(size=20)

    def drawDentogram(self):
        if self.type_cla == 0:
            return self.clusteringData.getPhoto(size=0.5)
        else:
            if self.type_cla == 1:
                return self.lsaData.getPhoto(size=0.2)
            else:
                if self.type_cla == 2:
                    return self.clusteringChemistryData.getPhoto(size=0.021)

    def drawPairplot(self, fl):
        dat = self.data.GetDataMix()
        if fl == 0:
            dat['Описание точки измерения'] = self.data.GetDataMix(['Описание точки измерения'])
            self.pairplotDescriptionData.Analyze(dat, 'Описание точки измерения')
            return self.pairplotDescriptionData.getPhoto()
            # return self.pairplotDescriptionData.getPhoto(dat, 'Описание точки измерения')
        else:
            if fl == 1:
                dat['Место измерения'] = self.data.GetDataMix(['Место измерения'])
                self.pairplotPlaceData.Analyze(dat, 'Место измерения')
                return self.pairplotPlaceData.getPhoto()
                # return self.pairplotPlaceData.getPhoto(dat, 'Место измерения')



    def drawPCA(self):
        if self.type_cla == 0:
            name = self.data.GetNameZooplankton()
            return self.pcaData.getPhoto([-0.5, 0.5, -0.04, 0.35], name, 0, 1)
        else:
            if self.type_cla == 1:
                name = self.data.GetNameZooplankton()
                return self.pcaLsaData.getPhoto([-0.5, 0.5, -0.04, 0.35], name, 0, 1)
            else:
                name = self.data.GetNameChemistryRes()
                return self.pcaChemistryData.getPhoto([-0.6, 0.6, 0.02, 0.115], name, 0, 1)


