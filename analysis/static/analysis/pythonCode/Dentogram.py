from analysis.static.analysis.pythonCode import Include

class Dentogram(object):
    def __init__(self):
        self.data = []

    def dentogram(self, measurement):
        if len(self.data) == 0:
            self.data = self._toDo(measurement)
        return self.data

    def _toDo(self, measurement):
        return []

    def _ClusteringMetod(self, measurement, index, col):
        distance_mat = Include.distance.pdist(measurement, 'cosine')
        Z = Include.hierarchy.linkage(distance_mat, 'single')
        Include.plt.figure(figsize=(20, 10))
        dn = Include.hierarchy.dendrogram(Z, labels=col, color_threshold=index)
        return Z

    otvet = []

    def _Save(self, clustering, id, size, col):
        if size > id:
            # print(int(id))
            return str(col[int(id)]) + ", "
            # print(col[int(id)])
        else:
            st = self._Save(clustering, clustering.iloc[id - size, 0], size, col)
            st = st + self._Save(clustering, clustering.iloc[id - size, 1], size, col)
            return st

    def GropupClustering(self, Z, id, size, col):
        ZZ = Include.pd.DataFrame(Z)
        ZZ[0] = ZZ[0].astype(Include.np.int64)
        ZZ[1] = ZZ[1].astype(Include.np.int64)
        mas = Include.pd.Series([])
        for i in range(ZZ[0].size):
            mas[i] = i
        ZZ['id'] = mas
        global otvet
        otvet = []
        self._Bypass(ZZ, id, size, col)
        return otvet

    def _Bypass(self, clustering, id, size, col):
        str = clustering[clustering[0] == id]
        if str.size == 0:
            str = clustering[clustering[1] == id]
            if str.size == 0:
                return ""
            id2 = 0
        else:
            id2 = 1
        # print("\nГруппа")
        st = ""
        if size <= id:
            st = self._Save(clustering, clustering.iloc[id - size, 0], size, col)
            st = st + self._Save(clustering, clustering.iloc[id - size, 1], size, col)
        else:
            st = self._Save(clustering, id, size, col)

        st = st + self._Save(clustering, str.iloc[0, id2], size, col)
        otvet.append(st)
        self._Bypass(clustering, int(str['id']) + size, size, col)

