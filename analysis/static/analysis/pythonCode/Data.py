from analysis.static.analysis.pythonCode import Include
from analysis.static.analysis.pythonCode import ReadFile
from analysis.static.analysis.pythonCode import LSA
from analysis.static.analysis.pythonCode import Clustering
from analysis.static.analysis.pythonCode import AnalysisResult
from analysis.static.analysis.pythonCode import CorrelationChemistry
from analysis.static.analysis.pythonCode import CorrelationZooplankton

class Data(object):
    data = Include.pd.DataFrame([])
    lsaData = LSA.LSA()
    clusteringData = Clustering.Clustering()
    correlationChemistryData = CorrelationChemistry.CorrelationChemistry()
    correlationZooplanktonData = CorrelationZooplankton.CorrelationZooplankton()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Data, cls).__new__(cls)
        return cls.instance

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
        self.data = ReadFile.ReadFile(name)
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
        ress = AnalysisResult.SortingCorrelation(cor[name])
        return self._createMas(ress)

    def AnalysisCorrelationZooplankton(self, name):
        cor = self.CorrelationZooplankton()
        ress = AnalysisResult.SortingCorrelation(cor[name])
        return self._createMas(ress)


    def AnalysisClustering(self, names):
        id = self._Search(names)
        cl = self.clustering()
        col = self.GetNameZooplankton()
        return AnalysisResult.GropupClustering(cl, id, col.size, col)

    def AnalysisLSA(self, names):
        id = self._Search(names)
        cl = self.lsa()
        col = self.GetNameZooplankton()
        return AnalysisResult.GropupClustering(cl, id, col.size, col)




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
