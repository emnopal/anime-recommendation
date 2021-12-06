"""
Due to GitHub maximum file size limit,
so i don't include the dataset in the repository.
If you want to download or use dataset, please go to the following link:
https://www.kaggle.com/hernan4444/anime-recommendation-database-2020

Binary file is not included in the repository too.
But you can generate by yourself in this_repository/notebook file
to create *.npz. and *.npy files.
"""


import sys; sys.path.append('..')  # noqa

import pandas as pd

from utils.preprocessing import (
    readDataset,
    readBinary
)

from .model import (
    defineModels
)

ALLOWED_DB_ARGS = ['db', 'sql', 'useDB', 'useSQL', 'usedb', 'use db', 'use DB', 'use SQL']

class ContentBasedFiltering:

    def __init__(self, vector1, vector2=None, conn=None, dataset='use SQL', index_col="animeIndex"):
        if vector2 is None:
            self.vector1 = vector1
        else:
            self.vector1 = vector1
            self.vector2 = vector2
        self.conn = conn
        self.index_col = index_col
        self.dataset = dataset


    def _getDataset(self):
        if isinstance(self.dataset, str):
            if self.dataset in ALLOWED_DB_ARGS:
                pass
            return readDataset(self.dataset, self.conn, self.index_col)
        if isinstance(self.dataset, pd.DataFrame):
            return self.dataset
        else:
            raise TypeError("dataset type not understand")


    def _getVector(self):
        if self.vector2 is None:
            return readBinary(self.vector1)
        else:
            return readBinary(self.vector1), readBinary(self.vector2)


    def animeSearch(self, nameQuery, n=5):
        if self.dataset in ALLOWED_DB_ARGS:
            query = f'SELECT * from animedb.anime WHERE animeName LIKE "%{nameQuery}%" ORDER BY animeScore DESC LIMIT {n};'
            nameContains = pd.read_sql(sql=query, con=self.conn, index_col=self.index_col)
            nameContains.index = nameContains.index - 1
        else:
            df = self._getDataset().copy()
            nameQuery = nameQuery.lower()
            nameContains = df.loc[df.animeNameLower.str.contains(nameQuery, na=False)]
            nameContains = nameContains.sort_values(by="animeScore", ascending=False)
        pd.set_option('display.max_rows', len(nameContains))
        return nameContains


    def animeSearchById(self, id):
        if self.dataset in ALLOWED_DB_ARGS:
            query = f'SELECT * from animedb.anime WHERE animeID = {id};'
            idQuery = pd.read_sql(sql=query, con=self.conn, index_col=self.index_col)
            idQuery.index = idQuery.index - 1
        else:
            df = self._getDataset().copy()
            idQuery = df[df.animeID == id]
        return idQuery


    def _getSimilar(self, vector=None, query_index=None, n=50):
        distances, indices = defineModels(vector=vector, query_index=query_index, n=n)
        if self.dataset in ALLOWED_DB_ARGS:
            result = []
            for i in range(len(distances.flatten())):
                index = indices.flatten()[i]
                if index == query_index:
                    continue
                result.append(index)
            result = tuple(map(lambda x: x+1, result))
            query = f"select * from animedb.anime where animeIndex in {result};"
            results_df = pd.read_sql(sql=query, con=self.conn, index_col=self.index_col)
        else:
            df = self._getDataset().copy()
            result = []
            for i in range(len(distances.flatten())):
                index = indices.flatten()[i]
                if index == query_index:
                    continue
                result.append(df.iloc[index])
            results_df = pd.DataFrame(result)
        pd.set_option('display.max_rows', len(results_df))
        return results_df


    def _vectorToModels(self, query_index=None, n=50):
        if self.vector2 is None:
            vector = self._getVector()
            return self._getSimilar(vector=vector, query_index=query_index, n=n)
        else:
            vector1, vector2 = self._getVector()
            self.model1 = self._getSimilar(vector=vector1, query_index=query_index, n=n)
            self.model2 = self._getSimilar(vector=vector2, query_index=query_index, n=n)
            return self.model1, self.model2


    def mostSimilarByName(self, nameQuery, n=20):
        query = self.animeSearch(nameQuery=nameQuery, n=1)
        query_index = query.index[0]
        if self.vector2 is None:
            vectorModels = self._vectorToModels(query_index=query_index, n=n)
        else:
            vectorModels0, vectorModels1 = self._vectorToModels(query_index=query_index, n=n)
            vectorModels = vectorModels1.append(vectorModels0)
        pd.set_option('display.max_rows', len(vectorModels))
        print(f"Generated dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
        return query, vectorModels.drop_duplicates().sort_values(by="animeScore", ascending=False)


    def mostSimilarByIndex(self, mal_id, n=20):
        query = self.animeSearchById(mal_id)
        query_index = query.index
        if self.vector2 is None:
            vectorModels = self._vectorToModels(query_index=query_index, n=n)
        else:
            vectorModels0, vectorModels1 = self._vectorToModels(query_index=query_index, n=n)
            vectorModels = vectorModels1.append(vectorModels0)
        pd.set_option('display.max_rows', len(vectorModels))
        print(f"Generated dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
        return query, vectorModels.drop_duplicates().sort_values(by="animeScore", ascending=False)


