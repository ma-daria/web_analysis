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
        return AnalysisResult.SortingCorrelation(cor[name])

    def AnalysisCorrelationZooplankton(self, name):
        cor = self.CorrelationZooplankton()
        return AnalysisResult.SortingCorrelation(cor[name])

    def AnalysisClustering(self, id):
        cl = self.clustering()
        col = self.GetNameZooplankton()
        return AnalysisResult.GropupClustering(cl, id, col.size, col)

    def AnalysisLSA(self, id):
        cl = self.lsa()
        col = self.GetNameZooplankton()
        return AnalysisResult.GropupClustering(cl, id, col.size, col)



