from analysis.static.analysis.pythonCode import Include, Analysis

class LDA(Analysis.Analysis):
    gro =''

    def __init__(self):
        super().__init__()
        # self.data = Include.LatentDirichletAllocation()
        # self.fla = 0
        # self.gro = ''

    # def lda(self, toTopics, no_topics = 10):
    #     if self.fla ==0:
    #         self.fla = 1
    #         self._toDo(toTopics, no_topics)

    def _toDo(self, measurement, nameCol):
        self.data = Include.LatentDirichletAllocation(n_components=10, max_iter=5, learning_method='online',
                                                      learning_offset=50., random_state=0)
        self.data = self.data.fit(measurement)
        return self.data

    def group_n(self,  names, no_top_words = 10 ):
        if self.gro == '':
            self.gro = self._group_N(names, no_top_words)
        return self.gro

    def _group_N(self,  names, no_top_words):
        names = names.tolist()
        otvet =[]
        for topic_idx, topic in enumerate(self.data.components_):
            top_ag = topic.argsort()
            st = ''
            st2 = ''
            for i in range(no_top_words):
                if i != 0:
                    # st =st + str(names[top_ag[-i]]) + ' [' + str(Include.np.round_(topic[top_ag[-i]], 4)) + '] <br>'
                    st = st + str(names[top_ag[-i]]) + '<br>'
                    st2 = st2 + str(Include.np.round_(topic[top_ag[-i]], 4)) + '<br>'
            # otvet.append(st)
            otvet.append([st, st2])
        return otvet


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
                        # st =st + str(names[top_ag[-i]]) + ' [' + str(Include.np.round_(topic[top_ag[-i]], 4)) + '] <br>'
                        st = st + str(names[top_ag[-i]]) + '<br>'
                        st2 = st2 + str(Include.np.round_(topic[top_ag[-i]], 4)) + '<br>'
                    else:
                        break
            # otvet.append(st)
            otvet.append([st, st2])
        return otvet

    def _draw(selfm, size, nameCol, component1, component2):
        return Include.io.BytesIO()
