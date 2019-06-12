from analysis.static.analysis.pythonCode import Include, DentogramLSA, DentogramClustering, Correlation, Data
import time

class Data_analysis(object):
    data = Data.Data()
    lsaData = DentogramLSA.DentogramLSA()
    clusteringData = DentogramClustering.DentogramClustering()
    clusteringChemistryData = DentogramClustering.DentogramClustering()
    correlationChemistryData = Correlation.Correlation()
    correlationZooplanktonData = Correlation.Correlation()
    correlationMixData = Correlation.Correlation()
    correlationLSAData = Correlation.Correlation()

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
        return self.correlationChemistryData.correlation(d)

    def CorrelationZooplankton(self):
        d = self.data.GetDataZooplankton()
        return self.correlationZooplanktonData.correlation(d)

    def CorrelationMix(self, name):
        d = self.data.GetDataMix(name)
        self.correlationMixData = Correlation.Correlation()
        return self.correlationMixData.correlation(d)

    def CorrelationLSA(self):
        da = self.lsaData.GetMass()
        db = Include.pd.DataFrame(Include.np.array(da))
        name = self.data.GetNameZooplankton()
        d = db
        i = 0
        for n in name:
            d = d.rename(columns={i: n})
            i = i + 1
        return self.correlationLSAData.correlation(d)

    def clustering(self):
        d = self.data.GetDataZooplankton()
        return self.clusteringData.dentogram(d)

    def lsa(self):
        d = self.data.GetDataZooplankton()
        return self.lsaData.dentogram(d)

    def clusteringChemistry(self):
        d = self.data.GetDataChemistryRes()
        return self.clusteringChemistryData.dentogram(d)





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
            return self.correlationChemistryData.getPhoto(10, "correlationChemistry.png")
        else:
            if fl == 1:
                return self.correlationZooplanktonData.getPhoto(25, 'correlationZooplankton.png')
            else:
                if fl == 2:
                    return self.correlationMixData.getPhoto(15, 'correlationMix.png')
                else:
                    return self.correlationLSAData.getPhoto(20, 'correlationLSA.png')



    def drawDentogram(self, fl):
        if fl == 0:
            return self.clusteringData.getPhoto('clustering.png')
        else:
            if fl == 1:
                return self.lsaData.getPhoto('lsa.png')
            else:
                if fl == 2:
                    return self.clusteringChemistryData.getPhoto('clusteringChemistry.png')

    def drawPairplot(self):
        time.sleep(2)  # вот этот говнокод, но я не знаю как решить. Там они паралельно запускаются похоже и мешают друг другу
        tic = time.time()
        dat = self.data.GetDataMix(self.list)
        dat[ 'Описание точки измерения'] = self.data.GetDataMix(['Описание точки измерения'])
        sns_plot = Include.sns.pairplot(dat, hue='Описание точки измерения')
        buffer = Include.io.BytesIO()
        sns_plot.savefig(buffer, format='png')
        toc = time.time()
        print(toc - tic)
        return buffer

    def drawPairplot2(self):
        time.sleep(7)  # вот этот говнокод, но я не знаю как решить. Там они паралельно запускаются похоже и мешают друг другу
        dat = self.data.GetDataMix(self.list)
        dat[ 'Место измерения'] = self.data.GetDataMix(['Место измерения'])
        sns_plot = Include.sns.pairplot(dat, hue='Место измерения')
        buffer = Include.io.BytesIO()
        sns_plot.savefig(buffer, format='png')
        return buffer

