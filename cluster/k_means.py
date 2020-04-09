import numpy as np
from collections import defaultdict
import random
from helper.max_stack import MaxStack


class KMeans:
    def train(self, m, sents_vec):
        """
        train kmeans model until centriods converge
        :param m:
        :param sents_vec:
        :return:
        """
        # 在数据中随机抽取m个中心点
        self.centroids = []
        R = random.randint(0, sents_vec.shape[0]-1)
        self.centroids.append(sents_vec[R])
        stack = MaxStack(m-1)
        for i in range(sents_vec.shape[0]):
            sim = self.cosine_simi(sents_vec[i], self.centroids[0])
            stack.push(sim, sents_vec[i])
        data = stack.get_data_list()
        for i in data:
            self.centroids.append(i)
        while True:
            clusters = self.choose_cluster(m, sents_vec, self.centroids)
            n_centroids = self.update_centroids(clusters)
            flag = 0
            for i in range(len(self.centroids)):
                if i < len(n_centroids):
                    if not all(self.centroids[i] == n_centroids[i]):
                        flag = 1
                else:
                    flag = 1
            if flag:
                self.centroids = n_centroids
            else:
                break

    def choose_cluster(self, m, sents_vec, centroids):
        """
        put data to the closest centroid based on cosine similarity
        :param m:
        :param sents_vec:
        :param centroids:
        :return:
        """
        clusters = defaultdict(list)
        for j in range(sents_vec.shape[0]):
            vec = sents_vec[j]
            min_dis = 2
            min_c = -1
            if any(vec) != 0:
                for i in range(len(centroids)):
                    sim = self.cosine_simi(vec, centroids[i])
                    if sim <= min_dis:
                        min_dis = sim
                        min_c = i
                clusters[min_c].append(vec)
        return clusters

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
        if vec.shape[0] > 1:
            vec_norm = np.sqrt(np.dot(vec, vec))
            cent_norm = np.sqrt(np.dot(cent, cent))
            return 1 - np.dot(vec, cent) / (vec_norm * cent_norm)
        return np.abs(vec - cent)

    def predict(self, sents_vec):
        result = []
        for j in range(sents_vec.shape[0]):
            vec = sents_vec[j]
            min_dis = 2
            min_c = -1
            if any(vec) != 0:
                for i in range(len(self.centroids)):
                    sim = self.cosine_simi(vec, self.centroids[i])
                    if sim <= min_dis:
                        min_dis = sim
                        min_c = i
                result.append(min_c)
        return result


if __name__ == '__main__':
    from sklearn.datasets import load_iris
    from sklearn.preprocessing import MinMaxScaler
    iris = load_iris()
    iris_data = iris['data']
    iris_target = iris['target']
    data_zs = (iris_data - iris_data.mean()) / iris_data.std()
    ## 也可以自定义函数minmax标准化、或者现成的函数
    scale = MinMaxScaler().fit(iris_data)
    iris_datascale = scale.transform(iris_data)
    km = KMeans()
    km.train(3, iris_datascale)
    result1 = km.predict(iris_datascale)
    print(result1)


