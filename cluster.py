# -*- coding: utf-8 -*-

"""The Class of Cluster

the module describe the different method and afford methods to clustering the data
"""

from numpy import unique
from numpy import where
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AffinityPropagation
from sklearn_extra.cluster import KMedoids
from sklearn_extra.cluster import CLARA
from kmodes.kprototypes import KPrototypes


class CLUSTER:
    """CLUSTER CLASS

    """

    def __init__(self, X, cluster_type, K=None):
        """

        :param X:o
        :param Kmeans_num:
        """

        self.X = X  # cluster data
        self.K = K  # the kmeans cluster number

    def kmeans(self):
        """

        :return: cluster labels and cluster center
        """
        K = KMeans(n_clusters=self.K,
                   max_iter=500,
                   n_init=10,
                   init= 'k-means++'
                   )
        K.fit(self.X)
        labels = K.labels_
        center = K.cluster_centers_

        return ('Kmeans',
                labels,
                center,
                )

    def kmedoids(self):
        """

        :return:
        """
        K = KMedoids(n_clusters=self.K,
                     metric='euclidean',
                     method='pam',
                     init='k-medoids++',
                     max_iter=500,
                     random_state=None)
        K.fit(self.X)
        label = K.labels_
        center = K.cluster_centers_

        return ('KMedoids',
                label,
                center,
                )

    def dbscan(self):
        """

        :return:
        """
        db = DBSCAN(eps=0.3,
                    min_samples=10
                    )
        db.fit(self.X)
        labels = db.labels_

        n_cluster_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_special_ = list(labels).count(-1)

        return ('DBSCAN',
                labels,
                n_cluster_,
                n_special_,
                )

    def affinity_propagation(self):
        """

        :return:
        """
        af = AffinityPropagation(preference=-50,
                                 random_state=0,
                                 )
        af.fit(self.X)
        labels = af.labels_
        n_clusters_ = len(af.cluster_centers_indices_)

        return ('Affinity_Propagation',
                labels,
                n_clusters_
                )

    def clara(self):
        """

        :return:
        """
        cl = CLARA(n_clusters=self.K,
                   metric='euclidean',
                   max_iter=500,
                   )
        cl.fit(self.X)
        labels = cl.labels_
        center = cl.cluster_centers_

        return ('CLARA',
                labels,
                center,
                )

    def kprototypes(self):
        """

        :return:
        """
        kpro = KPrototypes(n_clusters=self.K)