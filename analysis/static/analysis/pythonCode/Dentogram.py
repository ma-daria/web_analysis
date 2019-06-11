from analysis.static.analysis.pythonCode import Include
from django.conf import settings

class Dentogram(object):
    def __init__(self):
        self.data = Include.np.asarray([])
        self.buffer = []
        self.index = 0
        self.col = Include.np.asarray([])

    def dentogram(self, measurement):
        if len(self.data) == 0:
        # if self.data.size == 0:
            self.data = self._toDo(measurement)
        return self.data

    def _toDo(self, measurement):
        return []

    def _ClusteringMetod(self, measurement, index, col):
        distance_mat = Include.distance.pdist(measurement, 'cosine')
        Z = Include.hierarchy.linkage(distance_mat, 'single', metric='cosine')
        # Include.plt.figure(figsize=(15, 15), dpi=200)
        # dn = Include.hierarchy.dendrogram(Z, labels=col, color_threshold=index)
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
        print(self.Group(Z, 0.9, size, col))
        ZZ = self._createMas(Z)
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

    def _createMas(self, Z):
        ZZ = Include.pd.DataFrame(Z)
        ZZ[0] = ZZ[0].astype(Include.np.int64)
        ZZ[1] = ZZ[1].astype(Include.np.int64)
        mas = Include.pd.Series([])
        for i in range(ZZ[0].size):
            mas[i] = i
        ZZ['id'] = mas
        return ZZ

    def Group(self, Z, r, size, col):



        ZZ = self._createMas(Z)
        ZZ = ZZ[ZZ[2] <= r]
        global us_couples
        us_couples = Include.pd.DataFrame(ZZ['id'])
        us_couples['fl'] = "False"
        us_couples['id'] = us_couples['id'] + size

        global us_options
        lis = []
        for i in range(size):
            lis.append(i)
        us_options = Include.pd.DataFrame({'id': lis})
        us_options['fl'] = "False"

        global otvet
        otvet = []

        for i in range(ZZ['id'].size):
            if ZZ.iloc[~i, 0] >= size:
                # if us_couples.loc[us_couples['id'] == ZZ.iloc[~i, 0], 'fl'] == "True":
                if us_couples.loc[ZZ.iloc[~i, 0] - size, 'fl'] == "True":
                    break
            else:
                # if us_options.loc[us_options['id'] == ZZ.iloc[~i, 0], 'fl'] == "True":
                if us_options.loc[ZZ.iloc[~i, 0], 'fl'] == "True":
                    break
            if ZZ.iloc[~i, 1] >= size:
                # if us_couples.loc[us_couples['id'] == ZZ.iloc[~i, 1], 'fl'] == "True":
                if us_couples.loc[ZZ.iloc[~i, 1] - size, 'fl'] == "True":
                    break
            else:
                # if us_options.loc[us_options['id'] == ZZ.iloc[~i, 0], 'fl'] == "True":
                if us_options.loc[ZZ.iloc[~i, 0], 'fl'] == "True":
                    break
            st = self._serGr(-i, ZZ, size, col)
            st = st + self._options(col)
            otvet.append(st)

        return otvet


    def _options(self, col):
        st = ''
        global us_options
        for i in us_options['id']:
            if us_options.loc[i, 'fl'] == "False":
                st=st + col[us_options.loc[i,'id']] +" | "
        return st


    def _serGr(self, i, ZZ, size, col):
        global us_couples
        global us_options
        if ZZ.iloc[i, 0] >= size:
            us_couples.loc[ZZ.iloc[i, 0] - size, 'fl'] = "True"
            # us_couples.loc[us_couples['id'] == ZZ.iloc[~i, 0], 'fl'] = "True"
            st1 = self._serGr(ZZ.iloc[i, 0] - size, ZZ, size, col)
        else:
            us_options.loc[ZZ.iloc[i, 0], 'fl'] = "True"
            # us_options.loc[us_options['id'] == ZZ.iloc[~i, 0], 'fl'] = "True"
            st1 = self._saveGr(ZZ.iloc[i, 0], col)

        if ZZ.iloc[i, 1] >= size:
            us_couples.loc[ZZ.iloc[i, 1] - size, 'fl'] = "True"
            # us_couples.loc[us_couples['id'] == ZZ.iloc[~i, 1], 'fl'] = "True"
            st2 = self._serGr(ZZ.iloc[i, 1] - size, ZZ, size, col)
        else:
            us_options.loc[ZZ.iloc[i, 0], 'fl'] = "True"
            # us_options.loc[us_options['id'] == ZZ.iloc[~i, 0], 'fl'] = "True"
            st2 = self._saveGr(ZZ.iloc[i, 1], col)

        return st1+st2

    def _saveGr(self, id, col):
        return str(col[id])+" | "



    def getPhoto(self, name):
        if self.buffer == []:
            self.draw(name)
        return self.buffer

    def draw(self, name):
        Include.plt.figure(figsize=(20, 15), dpi=200)
        dn = Include.hierarchy.dendrogram(self.data, labels=self.col, color_threshold=self.index)
        self.buffer = Include.io.BytesIO()
        Include.plt.savefig(self.buffer, format='png')
        Include.plt.savefig(str(settings.STATIC_ROOT_A) + "/analysis/img/"+name)

