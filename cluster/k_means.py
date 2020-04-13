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
        [stack.push(self.cosine_simi(vec, self.centroids[0]), vec) for vec in sents_vec]
        self.centroids += stack.get_data_list()
        while True:
            clusters = self.choose_cluster(sents_vec, self.centroids)[0]
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

    def choose_cluster(self, sents_vec, centroids):
        """
        put data to the closest centroid based on cosine similarity
        :param m:
        :param sents_vec:
        :param centroids:
        :return:
        """
        clusters = defaultdict(list)
        result = []
        for vec in sents_vec:
            min_dis = {i: self.cosine_simi(vec, centroids[i]) for i in range(len(centroids))}
            min_c = min(min_dis.keys(), key=(lambda k: min_dis[k]))
            clusters[min_c].append(vec)
            result.append(min_c)
        return clusters, result

    def update_centroids(self, clusters):
        centroids = [sum(s_vec)/len(s_vec) for k, s_vec in clusters.items() if len(s_vec) != 0 and any(sum(s_vec)) != 0]
        return centroids

    def cosine_simi(self, vec, cent):
        if vec.shape[0] > 1:
            vec_norm = np.sqrt(np.dot(vec, vec))
            cent_norm = np.sqrt(np.dot(cent, cent))
            if vec_norm == 0 or cent_norm == 0:
                return 2
            return 1 - np.dot(vec, cent) / (vec_norm * cent_norm)
        return np.abs(vec - cent)

    def predict(self, sents_vec):
        return self.choose_cluster(sents_vec, self.centroids)[1]


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


