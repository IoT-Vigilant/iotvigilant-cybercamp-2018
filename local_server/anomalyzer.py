# -*- coding: utf-8 -*-
"""
===================================
DBSCAN processing algorithm
===================================

--> Connects to Elastic Search Database and Extract selected features
--> Processes extracted features and labels data as clusters/noise
--> Returns labeled points to elasticsearch, in order to issue alerts

"""
print(__doc__)

import numpy as np
import time

from sklearn.cluster import DBSCAN
from sklearn import metrics



##############################################################################
# Example Data generation
# This phase must be replaced with features extracted from Elasticsearch
##############################################################################
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.4,
                            random_state=0)


## Data scaling to normalize to Epsilon scale
X = StandardScaler().fit_transform(X)

# #############################################################################
# Compute DBSCAN with time elapsed
###############################################################################

t = time.time()


db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Processing time calculation
elapsed = time.time() - t

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)


print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)
print('Time dedicated to DBSCAN execution %.5f seconds' % elapsed)


# #############################################################################
# Plot result
# ONLY FOR DEBUGGING AND DEVELOPING PURPOSES
###############################################################################
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
