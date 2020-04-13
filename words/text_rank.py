from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from gensim.models import word2vec
import networkx as nx


class TextRank:
    def __init__(self, word_set):
        self.words = word_set
        self.w2v_model = word2vec.Word2Vec.load('../model/n1_cbow.w2v')

    def sim_mat(self):
        length = len(self.words)
        sim_mat = np.zeros([length, length])
        for i in range(length):
            if self.words[i] in self.w2v_model.wv:
                for j in range(length):
                    if i != j and self.words[j] in self.w2v_model.wv:
                        sim_mat[i][j] = cosine_similarity(self.w2v_model.wv[self.words[i]].reshape(1,100)\
                                                          , self.w2v_model.wv[self.words[j]].reshape(1,100))[0,0]
        return sim_mat

    def rank(self):
        sim_mat = self.sim_mat()
        nx_graph = nx.from_numpy_array(sim_mat)
        scores = nx.pagerank(nx_graph)
        ranked_words = sorted(((scores[i], s) for i, s in enumerate(self.words)), reverse=True)
        return ranked_words


if __name__ == '__main__':
    corpus = []
    with open('../data/n_output.txt') as f:
        for line in f:
            sentence = []
            for word in line.split():
                sentence.append(word)
            if len(sentence) > 1:
                corpus.append(sentence)
    # load stop words
    with open('../data/stop_words.txt') as f:
        stop_words = [word.strip() for word in f]
    # remove stop words
    word_set = []
    for sent in corpus:
        word_set += sent
    word_set = set(word_set)
    word_set = [word for word in word_set if word not in stop_words]
    # train textrank
    tr = TextRank(word_set[:10000])
    ranked_words = tr.rank()
    sn = 10
    for i in range(sn):
        print(ranked_words[i][1])

