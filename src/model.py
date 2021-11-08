import numpy as np

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


def defineModels(n, vector, query_index, *args, **kwargs):
    model_knn = NearestNeighbors(
        metric='cosine', n_neighbors=n, *args, **kwargs)
    model_knn.fit(csr_matrix(vector.astype(np.float)))

    distances, indices = model_knn.kneighbors(
        vector[query_index, :].reshape(1, -1),
        n_neighbors=n)
    return distances, indices
