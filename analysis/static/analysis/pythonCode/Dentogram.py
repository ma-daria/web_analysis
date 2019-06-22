from analysis.static.analysis.pythonCode import Include, Analysis
from abc import abstractmethod

# класс потомок класса Analysis, который объединяет алгоритмы, для которых необходимо построить дендрограмму
class Dentogram(Analysis.Analysis):
    col = Include.np.asarray([]) #список параметров
    otvet = [] #результат алгоритмов вывод заданых групп
    us_couples = Include.np.asarray([]) #массив использования параметров
    us_options = Include.np.asarray([]) # массив использования кластеров

    #  инициализация
    def __init__(self):
        super().__init__()

    # метод разбиения на кластеры
    @abstractmethod
    def _toDo(self,  measurement, nameCol):
        pass

    # вспомогательный метод разбиения на кластеры
    def _ClusteringMetod(self, measurement):
        distance_mat = Include.distance.pdist(measurement, 'cosine')
        Z = Include.hierarchy.linkage(distance_mat, 'single', metric='cosine')
        return Z

    # формирование результата работы алгоритма получения списка всех групп в которые входит параметр (name), выявленных в процессе кластеризации
    def _Save(self, clustering, id, size, col):
        if size > id:
            return str(col[int(id)]) + "<br>"
        else:
            st = self._Save(clustering, clustering.iloc[id - size, 0], size, col)
            st = st + self._Save(clustering, clustering.iloc[id - size, 1], size, col)
            return st

    # метод подготовки данных и вызывающий метод реализующий алгоритм получения списка всех групп в которые входит параметр (col), выявленных в процессе кластеризации
    def GropupClustering(self, Z, id, size, col):
        ZZ = self._createMas(Z)
        self.otvet = []
        self._Bypass(ZZ, id, size, col)
        return self.otvet

    # метод реализующий алгоритм получения списка всех групп в которые входит параметр (col), выявленных в процессе кластеризации
    def _Bypass(self, clustering, id, size, col):
        str = clustering[clustering[0] == id]
        if str.size == 0:
            str = clustering[clustering[1] == id]
            if str.size == 0:
                return ""
            id2 = 0
        else:
            id2 = 1
        st = ""
        if size <= id:
            st = self._Save(clustering, clustering.iloc[id - size, 0], size, col)
            st = st + self._Save(clustering, clustering.iloc[id - size, 1], size, col)
        else:
            st = self._Save(clustering, id, size, col)

        st = st + self._Save(clustering, str.iloc[0, id2], size, col)
        self.otvet.append(st)
        self._Bypass(clustering, int(str['id']) + size, size, col)

    # метод предобработки данных
    def _createMas(self, Z):
        ZZ = Include.pd.DataFrame(Z)
        ZZ[0] = ZZ[0].astype(Include.np.int64)
        ZZ[1] = ZZ[1].astype(Include.np.int64)
        mas = Include.pd.Series([])
        for i in range(ZZ[0].size):
            mas[i] = i
        ZZ['id'] = mas
        return ZZ

    # метод реализующий алгоритм получения списка всех групп, выявленных в процессе кластеризации, заданной точности
    def Group(self, Z, r, size, col):
        ZZ = self._createMas(Z)
        ZZ = ZZ[ZZ[2] <= r]
        self.us_couples = Include.pd.DataFrame(ZZ['id'])
        self.us_couples['fl'] = "False"
        self.us_couples['id'] = self.us_couples['id'] + size
        lis = []
        for i in range(size):
            lis.append(i)
        self.us_options = Include.pd.DataFrame({'id': lis})
        self.us_options['fl'] = "False"
        self.otvet = []
        for i in range(ZZ['id'].size):
            ind = 0
            if i == 0:
                ind = 1
            else:
                if self.us_couples.iloc[-i, 1] == "True":
                    ind = 1
                if ZZ.iloc[-i, 0] >= size:
                    if self.us_couples.loc[ZZ.iloc[-i, 0] - size, 'fl'] == "True":
                        ind = 1
                else:
                    if self.us_options.loc[ZZ.iloc[-i, 0], 'fl'] == "True":
                        ind = 1
                if ZZ.iloc[-i, 1] >= size:
                    if self.us_couples.loc[ZZ.iloc[-i, 1] - size, 'fl'] == "True":
                        ind = 1
                else:
                    if self.us_options.loc[ZZ.iloc[-i, 1], 'fl'] == "True":
                        ind = 1
            if ind == 0:
                self.us_couples.iloc[-i, 1] = "True"
                st = self._serGr(-i, ZZ, size, col)
                self.otvet.append(st)
        self._options(col)
        return self.otvet

    # метод проверки параметров, которые были не использвоаны во время работы алгоритма получения списка всех групп, выявленных в процессе кластеризации, заданной точности
    def _options(self, col):
        st = ''
        for i in self.us_options['id']:
            if self.us_options.loc[i, 'fl'] == "False":
                st=col[self.us_options.loc[i,'id']]
                self.otvet.append(st)

    # метод объединения результата работы алгоритма получения списка всех групп, выявленных в процессе кластеризации, заданной точности
    def _serGr(self, i, ZZ, size, col):
        if ZZ.iloc[i, 0] >= size:
            self.us_couples.loc[ZZ.iloc[i, 0] - size, 'fl'] = "True"
            st1 = self._serGr(ZZ.iloc[i, 0] - size, ZZ, size, col)
        else:
            self.us_options.loc[ZZ.iloc[i, 0], 'fl'] = "True"
            st1 = self._saveGr(ZZ.iloc[i, 0], col)

        if ZZ.iloc[i, 1] >= size:
            self.us_couples.loc[ZZ.iloc[i, 1] - size, 'fl'] = "True"
            st2 = self._serGr(ZZ.iloc[i, 1] - size, ZZ, size, col)
        else:
            self.us_options.loc[ZZ.iloc[i, 1], 'fl'] = "True"
            st2 = self._saveGr(ZZ.iloc[i, 1], col)
        return st1+st2

    # метод формирование результата работы алгоритма получения списка всех групп, выявленных в процессе кластеризации, заданной точности
    def _saveGr(self, id, col):
        return str(col[id])+"<br>"

    # метод построения дендрограммы
    def _draw(self, size, nameCol, component1, component2):
        Include.plt.figure(figsize=(20, 15), dpi=200)
        dn = Include.hierarchy.dendrogram(self.data, labels=self.col, color_threshold=size)
        self.buffer = Include.io.BytesIO()
        Include.plt.savefig(self.buffer, format='png')