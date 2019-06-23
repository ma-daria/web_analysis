from analysis.static.analysis.pythonCode import Include, DentogramLSA, DentogramClustering, Correlation, Data, Pairplot, GR_PCA, LDA

# реализует паттерн “фасад”. Используется для доступа к реализованным функциям
class Data_analysis(object):
    data = Data.Data() #экземпляр класса Data для хранения данных
    lsaData = DentogramLSA.DentogramLSA() #экземпляр класса DentogramLSA для хранения рузультатом лса
    clusteringData = DentogramClustering.DentogramClustering() #экземпляр класса DentogramClustering
    clusteringChemistryData = DentogramClustering.DentogramClustering() #экземпляр класса DentogramClustering для хранения и обработки результатов кластеризации видов зоопланктона
    pcaData = GR_PCA.GR_PCA() #экземпляр класса DentogramClustering для хранения и обработки результатов кластеризации химического состава
    pcaLsaData = GR_PCA.GR_PCA() #экземпляр класса GR_PCA для хранения и обработки результатов PCA для  видов зоопланктона после лса
    pcaChemistryData = GR_PCA.GR_PCA() #экземпляр класса GR_PCA для хранения и обработки результатов PCA для  химического состава
    correlationChemistryData = Correlation.Correlation() #экземпляр класса Correlation для хранения и обработки результатов корреляции между химическим составом
    correlationZooplanktonData = Correlation.Correlation() #экземпляр класса Correlation для хранения и обработки результатов корреляции между видами зоопланктона
    correlationMixData = Correlation.Correlation() #экземпляр класса Correlation для хранения и обработки результатов корреляции между указанными параметрами
    correlationLSAData = Correlation.Correlation() #экземпляр класса Correlation для хранения и обработки результатов корреляции между видами зоопланктона после лса
    pairplotDescriptionData = Pairplot.Pairplot() #экземпляр класса Pairplot для хранения попарных диаграмм рассеяния [Описание точки измерения]
    pairplotPlaceData = Pairplot.Pairplot() #экземпляр класса Pairplot для хранения попарных диаграмм рассеяния [Место измерения]
    ldaData= LDA.LDA() #экземпляр класса LDA для хранения и обработки результатов латентного размещения Дирихле
    type = 0 #тип данных для корреляции
    type_cla = 0 #тип данных для кластеризации

    #  конструктор
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Data_analysis, cls).__new__(cls)
        return cls.instance

    #  метод для обнуления данных
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

    # метод для задания типа данных для кластеризации
    def SetType_cla(self, t):
        self.type_cla = t

    # метод для задания списка параметров указанных вручную
    def SetList(self, li):
        self.data.SetList(li)

    # метод для задания типа данных для корреляции
    def GetType(self):
        return self.type

    #  метод для получения типа данных для корреляции
    def SetType(self, t):
        self.type = t

    # метод для получения типа данных для кластеризации
    def GetType_cla(self):
        return self.type_cla

    #  метод для получения экземпляра класса Data
    def GetData(self):
        return self.data

    # метод вызывающий алгоритм чтения данных и предпроцессинг полученных данных
    def ReadFile(self, name):
        self._newCl()
        return self.data.readFile(name)

    #  метод вызывающий алгоритм корреляционного анализа
    def Correlation(self):
        if self.type == 0:
            d = self.data.GetDataChemistry()
            otv = self.correlationChemistryData.Analyze(d)
        else:
            if self.type == 1:
                d = self.data.GetDataZooplankton()
                otv = self.correlationZooplanktonData.Analyze(d)
            else:
                if self.type == 2:
                    d = self.data.GetDataMix()
                    self.correlationMixData = Correlation.Correlation()
                    otv = self.correlationMixData.Analyze(d)
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
        self.drawCorrelation()
        return otv

    # метод вызывающий алгоритм кластерного анализа
    def Clustering(self):
        otv = []
        if self.type_cla == 0:
            d = self.data.GetDataZooplankton()
            otv = self.clusteringData.Analyze(d)
        else:
            if self.type_cla == 1:
                d = self.data.GetDataZooplankton()
                otv = self.lsaData.Analyze(d)
            else:
                if self.type_cla == 2:
                    d = self.data.GetDataChemistryRes()
                    otv = self.clusteringChemistryData.Analyze(d)
        self.drawDentogram()
        self.PCA()
        return otv

    # метод вызывающий алгоритм метода главных компонент
    def PCA(self):
        if self.type_cla == 0:
            d = self.data.GetDataZooplankton()
            d['pH'] = self.data.GetDataMix(['pH'])
            self.pcaData.Analyze(d, 'pH')
        else:
            if self.type_cla == 1:
                d = self.data.GetDataZooplankton()
                d['pH'] = self.data.GetDataMix(['pH'])
                self.pcaLsaData.Analyze(d, 'pH')
            else:
                if self.type_cla == 2:
                    d = self.data.GetDataChemistryRes()
                    d['pH'] = Include.pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 1])
                    self.pcaChemistryData.Analyze(d, 'pH')
        self.drawPCA()

    # метод вызывающий алгоритм упорядочения коррелируемых параметров по возрастанию с заданным параметром (name)
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

    # метод вызывающий алгоритм получения параметров с высокой корреляцией
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

    # метод вызывающий алгоритм получения списка всех групп в которые входит параметр (name), выявленных в процессе кластеризации
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

    # метод вызывающий алгоритм получения списка всех групп, выявленных в процессе кластеризации, заданной точности (val)
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

    # метод вызывающий алгоритм латентного размещения Дирихле
    def LDA(self):
        d = self.data.GetDataZooplankton()
        self.ldaData.Analyze(d)

    # метод вызывающий алгоритм находящий первые 10 параметров входящие в выявлены темы с помощью латентного размещения Дирихле
    def NAnalysisLDA(self):
        col = self.data.GetNameZooplankton()
        return self.ldaData.group_n(col)

    # метод вызывающий алгоритм находящий первые N параметров, заданной точности (val), входящие в выявлены темы с помощью латентного размещения Дирихле
    def AnalysisLDA(self, val):
        col = self.data.GetNameZooplankton()
        return self.ldaData.group(col, val)

    # метод поиска индекса заданного значения (names) в массиве (col)
    def _Search(self, names, col):
        i = 0
        for i in range(col.size):
            if col[i] == names:
                return i

    # метод преобразования результатов работы алгоритма вызываемого в AnalysisCorrelation в удобном для пользователя виде
    def _createMas(self, ress):
        ind = ress.index.tolist()
        res = ress.tolist()
        otvet = []
        for i in range(len(res)):
            otvet.append([ind[i], res[i]])
        return otvet

    # метод преобразования результатов работы алгоритма вызываемого в CorrelationMax в удобном для пользователя виде
    def _createMasMax(self, ress):
        res = ress[0].tolist()
        res1 = ress[1].tolist()
        res2 = ress[2].tolist()
        otvet = []
        for i in range(len(res)):
            otvet.append([res[i], res1[i], res2[i]])
        return otvet

    # метод вызывающий алгоритм построения матрица корреляции
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

    # метод вызывающий алгоритм построения дендрограммы
    def drawDentogram(self):
        if self.type_cla == 0:
            return self.clusteringData.getPhoto(size=0.5)
        else:
            if self.type_cla == 1:
                return self.lsaData.getPhoto(size=0.2)
            else:
                if self.type_cla == 2:
                    return self.clusteringChemistryData.getPhoto(size=0.021)

    # метод вызывающий алгоритм построения попарных диаграмм рассеяния
    def drawPairplot(self, fl):
        dat = self.data.GetDataMix()
        if fl == 0:
            self.pairplotDescriptionData = Pairplot.Pairplot()
            dat['Описание точки измерения'] = self.data.GetDataMix(['Описание точки измерения'])
            self.pairplotDescriptionData.Analyze(dat, 'Описание точки измерения')
            return self.pairplotDescriptionData.getPhoto()
        else:
            if fl == 1:
                self.pairplotPlaceData = Pairplot.Pairplot()
                dat['Место измерения'] = self.data.GetDataMix(['Место измерения'])
                self.pairplotPlaceData.Analyze(dat, 'Место измерения')
                return self.pairplotPlaceData.getPhoto()

    # метод вызывающий алгоритм визуализации результатов  метода главных компонент
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