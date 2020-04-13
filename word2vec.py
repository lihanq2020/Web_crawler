from collections import defaultdict
import numpy as np
from tqdm import tqdm
class word2vec():
    def __init__(self, settings):
        self.n = settings['n']
        self.lr = settings['learning_rate']
        self.epochs = settings['epochs']
        self.window = settings['window_size']

    def generate_training_data(self, corpus):
        print('start generating training_data')
        word_counts = defaultdict(int)
        for row in corpus:
            for word in row:
                word_counts[word] += 1
        self.v_count = len(word_counts.keys())
        self.word_list = list(word_counts.keys())
        self.word_index = {word: i for i, word in enumerate(self.word_list)}
        self.index_word = {i: word for i, word in enumerate(self.word_list)}

        pbar = tqdm(total=len(corpus))
        training_data = []
        for sentence in corpus:
            pbar.update(1)
            sent_len = len(sentence)
            for i, word in enumerate(sentence):
                w_target = self.word2onehot(word)
                w_context = []
                for j in range(i-self.window, i+self.window+1):
                    if j>=0  and j != i and j < sent_len:
                        w_context.append(self.word2onehot(sentence[j]))
                training_data.append([w_target, w_context])
        return np.array(training_data)

    def word2onehot(self, word):
        word_vec = [0 for i in range(0, self.v_count)]
        word_vec[self.word_index[word]] = 1
        return word_vec

    def train(self, training_data):
        self.w1 = np.random.uniform(-1, 1, (self.v_count, self.n))
        self.w2 = np.random.uniform(-1, 1, (self.n, self.v_count))
        for i in range(self.epochs):
            self.loss = 0
            for w_t, w_c in training_data:
                y_pred, h, u = self.forward_pass(w_t)
                EI = np.sum([np.subtract(y_pred, word) for word in w_c], axis=0)
                self.backprop(EI, h, w_t)
                self.loss += -np.sum([u[word.index(1)] for word in w_c]) + len(w_c) * np.log(np.sum(np.exp(u)))
            print('Epoch:', i, "Loss", self.loss)



    def forward_pass(self, x):
        h = np.dot(self.w1.T, x) #shape(n, 1)
        u = np.dot(self.w2.T, h) #shape(v_count, 1)
        y_c = self.softmax(u)
        return y_c, h, u

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def backprop(self, e, h, x):
        d1_dw2 = np.outer(h, e) #shape(n, v_count)
        d1_dw1 = np.outer(x, np.dot(self.w2, e.T)) #(v_count, n)
        self.w1 = self.w1 - (self.lr * d1_dw1)
        self.w2 = self.w2 - (self.lr * d1_dw2)

    def word_vec(self, word):
        w_index = self.word_index[word]
        v_w = self.w1[w_index]
        return v_w

    def vec_sim(self, word, top_n):
        v_w1 = self.word_vec(word)
        word_sim = {}
        for i in range(self.v_count):
            v_w2 = self.w1[i]
            theta_sum = np.dot(v_w1, v_w2)
            theta_den = np.linalg.norm(v_w1) * np.linalg.norm(v_w2)
            theta = theta_sum / theta_den
            word = self.index_word[i]
            word_sim[word] = theta
        words_sorted = sorted(word_sim.items(), key=lambda kv: kv[1], reverse=True)
        for word, sim in words_sorted[:top_n]:
            print(word, sim)


if __name__ == '__main__':
    corpus = []
    with open('data/output.txt') as f:
        for line in f:
            sentence = []
            for word in line.split():
                sentence.append(word)
            if len(sentence) > 1:
                corpus.append(sentence)

    # settings = {
    #     'window_size': 2,
    #     'n': 100,
    #     'epochs': 50,
    #     'learning_rate': 0.01
    # }
    # w2v = word2vec(settings)
    # training_data = w2v.generate_training_data(corpus[:10000])
    # w2v.train(training_data)
    from gensim.models import word2vec
    print(word2vec.FAST_VERSION)
    import multiprocessing
    model = word2vec.Word2Vec(corpus, size=100, window=3, workers=multiprocessing.cpu_count(), iter=50)
    model.save("model/wangzhademadai.w2v")
