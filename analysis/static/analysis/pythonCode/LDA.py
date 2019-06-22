from analysis.static.analysis.pythonCode import Include, Analysis

# класс потомок класса Analysis, для алгоритма латентного размещения Дирихле
class LDA(Analysis.Analysis):
    gro ='' #результат работы алгоритма, который находит первые 10 параметров входящие в выявлены темы с помощью латентного размещения Дирихле

    # инициализация
    def __init__(self):
        super().__init__()

    # метод реализующий алгоритм  латентного размещения Дирихл
    def _toDo(self, measurement, nameCol):
        self.data = Include.LatentDirichletAllocation(n_components=10, max_iter=5, learning_method='online',
                                                      learning_offset=50., random_state=0)
        self.data = self.data.fit(measurement)
        return self.data

    #  метод вызывающий реализацию алгоритма поиска первых 10 параметров темы и возвращающий результат работы
    def group_n(self,  names, no_top_words = 10 ):
        if self.gro == '':
            self.gro = self._group_N(names, no_top_words)
        return self.gro

    # метод реализующий алгоритм, который находит первые 10 параметров входящие в выявлены темы с помощью латентного размещения Дирихле
    def _group_N(self,  names, no_top_words):
        names = names.tolist()
        otvet =[]
        for topic_idx, topic in enumerate(self.data.components_):
            top_ag = topic.argsort()
            st = ''
            st2 = ''
            for i in range(no_top_words):
                if i != 0:
                    st = st + str(names[top_ag[-i]]) + '<br>'
                    st2 = st2 + str(Include.np.round_(topic[top_ag[-i]], 4)) + '<br>'
            otvet.append([st, st2])
        return otvet

    # метод находящий первые N параметров, заданной точности (value), входящие в выявлены темы с помощью латентного размещения Дирихле
    def group(self,  names, value):
        names = names.tolist()
        otvet =[]
        for topic_idx, topic in enumerate(self.data.components_):
            top_ag = topic.argsort()
            st = ''
            st2 = ''
            for i in range(len(top_ag)):
                if i !=0:
                    if topic[top_ag[-i]] >= value:
                        st = st + str(names[top_ag[-i]]) + '<br>'
                        st2 = st2 + str(Include.np.round_(topic[top_ag[-i]], 4)) + '<br>'
                    else:
                        break
            otvet.append([st, st2])
        return otvet

    def _draw(selfm, size, nameCol, component1, component2):
        return Include.io.BytesIO()
