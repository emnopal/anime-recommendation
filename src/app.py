import sys; sys.path.append('..')  # noqa

import pandas as pd

from utils.preprocessing import (
    readDataset,
    readBinary
)

from .model import (
    defineModels
)


class ContentBasedFiltering:

    def __init__(self, dataset, vector1, vector2=None):
        self.dataset = dataset
        if vector2 is None:
            self.vector1 = vector1
        else:
            self.vector1 = vector1
            self.vector2 = vector2

    def _getDataset(self):
        return readDataset(self.dataset)

    def _getVector(self):
        if self.vector2 is None:
            return readBinary(self.vector1)
        else:
            return readBinary(self.vector1), readBinary(self.vector2)

    def animeSearch(self, nameQuery, n=5, sortByScore=True):
        df = self._getDataset().copy()
        nameQuery = nameQuery.lower()

        nameContains = df.loc[df.name_lower.str.contains(
            nameQuery, na=False)].drop(columns=['Features', 'name_lower'])

        if sortByScore:
            nameContains = nameContains.sort_values(
                by="Score", ascending=False)

        if n in ['all', 'All']:
            pd.set_option('display.max_rows', len(nameContains))
        else:
            pd.set_option('display.max_rows', n)
            nameContains = nameContains[:n]
            return nameContains
        return nameContains

    def _getSimilar(self, vector=None, query_index=None, n=50):
        df = self._getDataset().copy()
        distances, indices = defineModels(
            vector=vector, query_index=query_index, n=n)
        result = []
        for i in range(0, len(distances.flatten())):
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
            return self._getSimilar(
                vector=vector, query_index=query_index, n=n)

        else:
            vector1, vector2 = self._getVector()
            self.model1 = self._getSimilar(
                vector=vector1, query_index=query_index, n=n)
            self.model2 = self._getSimilar(
                vector=vector2, query_index=query_index, n=n)
            return self.model1, self.model2

    def mostSimilarByName(self, nameQuery, n=20, show="all"):
        query = self.animeSearch(
            nameQuery=nameQuery, n=1, sortByScore=False)

        query_index = query.index[0]

        if self.vector2 is None:
            vectorModels = self._vectorToModels(query_index=query_index, n=n)
            if show in ["all", "All"]:
                pd.set_option('display.max_rows', len(vectorModels))
                print(
                    f"Generated total dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
                return query, vectorModels.drop_duplicates().drop(columns=['Features', 'name_lower']).sort_values(  # noqa
                    by="Score", ascending=False)
            pd.set_option('display.max_rows', int(show))
            print(
                f"Generated dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
            return query, vectorModels.drop_duplicates().drop(columns=['Features', 'name_lower']).sort_values(  # noqa
                by="Score", ascending=False)

        else:
            vectorModels0, vectorModels1 = self._vectorToModels(
                query_index=query_index, n=n)
            vectorModels = vectorModels1.append(vectorModels0)
            if show in ["all", "All"]:
                pd.set_option('display.max_rows', len(vectorModels))
                print(
                    f"Generated total dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
                return query, vectorModels.drop_duplicates().drop(columns=['Features', 'name_lower']).sort_values(  # noqa
                    by="Score", ascending=False)
            pd.set_option('display.max_rows', int(show))
            print(
                f"Generated dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
            return query, vectorModels.drop_duplicates().drop(columns=['Features', 'name_lower']).sort_values(  # noqa
                by="Score", ascending=False)

    def mostSimilarByIndex(self, query_index, n=20, show="all"):

        if self.vector2 is None:
            vectorModels = self._vectorToModels(query_index=query_index, n=n)
            if show in ["all", "All"]:
                pd.set_option('display.max_rows', len(vectorModels))
                print(
                    f"Generated total dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
                return vectorModels.drop_duplicates().drop(columns=['Features', 'name_lower']).sort_values(  # noqa
                    by="Score", ascending=False)
            pd.set_option('display.max_rows', int(show))
            print(
                f"Generated dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
            return vectorModels.drop_duplicates().drop(columns=['Features', 'name_lower']).sort_values(  # noqa
                by="Score", ascending=False)

        else:
            vectorModels0, vectorModels1 = self._vectorToModels(
                query_index=query_index, n=n)
            vectorModels = vectorModels1.append(vectorModels0)
            if show in ["all", "All"]:
                pd.set_option('display.max_rows', len(vectorModels))
                print(
                    f"Generated total dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
                return vectorModels.drop_duplicates().drop(columns=['Features', 'name_lower']).sort_values(  # noqa
                    by="Score", ascending=False)
            pd.set_option('display.max_rows', int(show))
            print(
                f"Generated dataframe with {vectorModels.shape[0]} rows and {vectorModels.shape[1]} columns")  # noqa
            return vectorModels.drop_duplicates().drop(columns=['Features', 'name_lower']).sort_values(  # noqa
                by="Score", ascending=False)
