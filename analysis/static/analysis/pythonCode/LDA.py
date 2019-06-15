from analysis.static.analysis.pythonCode import Include

class LDA(object):

    def __init__(self):
        self.lda_data = Include.LatentDirichletAllocation()
        self.fla = 0
        self.gro = ''

    def lda(self, toTopics, no_topics = 5):
        if self.fla ==0:
            self.fla = 1
            self.toDo(toTopics, no_topics)

    def toDo(self, toTopics, no_topics):
        self.lda_data = Include.LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online',
                                                          learning_offset=50., random_state=0)
        self.lda_data = self.lda_data.fit(toTopics)


    def group_n(self,  names, no_top_words = 5 ):
        if self.gro == '':
            self.gro = self._group_N(names, no_top_words)
        return self.gro

    def _group_N(self,  names, no_top_words):
        names = names.tolist()
        otvet =[]
        for topic_idx, topic in enumerate(self.lda_data.components_):
            top_ag = topic.argsort()
            st = ''
            for i in range(no_top_words):
                if i != 0:
                    st =st + str(names[top_ag[-i]]) + ' [' + str(topic[top_ag[-i]]) + '] ||'
            otvet.append(st)
        return otvet


    def group(self,  names, value):
        names = names.tolist()
        otvet =[]
        for topic_idx, topic in enumerate(self.lda_data.components_):
            top_ag = topic.argsort()
            st = ''
            for i in range(len(top_ag)):
                if i !=0:
                    if topic[top_ag[-i]] >= value:
                        st =st + str(names[top_ag[-i]]) + ' [' + str(topic[top_ag[-i]]) + '] ||'
                    else:
                        break
            otvet.append(st)
        return otvet