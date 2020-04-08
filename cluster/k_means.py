import numpy as np

class kMeans:
    def train(self, m, sents_vec, sentences):
        centroids = []
        for i in range(m):
            centroids.append(sents_vec[i])
        while True:
            clusters, sents_cluster = self.choose_cluster(m, sents_vec, centroids, sentences)
            n_centroids = self.update_centroids(clusters)
            flag = 0
            for i in range(len(centroids)):
                if i < len(n_centroids):
                    if not all(centroids[i] == n_centroids[i]):
                        flag = 1
                else:
                    flag = 1
            if flag:
                centroids = n_centroids
            else:
                break
        return centroids, sents_cluster

    def choose_cluster(self, m, sents_vec, centroids, sentences):
        clusters = {}
        sents_cluster = {}
        for j in range(sents_vec.shape[0]):
            vec = sents_vec[j]
            min_dis = 2
            min_c = -1
            if any(vec) != 0:
                for i in range(len(centroids)):
                    sim = 1-self.cosine_simi(vec, centroids[i])
                    if sim < min_dis:
                        min_dis = sim
                        min_c = i
                if min_c not in clusters:
                    clusters[min_c] = []
                    sents_cluster[min_c] = []
                clusters[min_c].append(vec)
                sents_cluster[min_c].append(sentences[j])
        return clusters, sents_cluster

    def update_centroids(self, clusters):
        centroids = []
        for k, s_vec in clusters.items():
            c = np.zeros(s_vec[0].shape[0])
            for vec in s_vec:
                c = c + vec
            if any(c) != 0:
                c = c / len(s_vec)
                centroids.append(c)
        return centroids

    def cosine_simi(self, vec, cent):
        vec_norm = np.sqrt(np.dot(vec, vec))
        cent_norm = np.sqrt(np.dot(cent, cent))
        return np.dot(vec, cent) / (vec_norm * cent_norm)







