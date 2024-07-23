import numpy as np

from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from utils.profiling import timeit
from .preprocessing import (
    dataset,
    preprocessing_category
)

@timeit
def generate_binary(save_clean_dataset: bool = False):
    """ Generate binary features and save to binary directory

    Args:
        save_clean_dataset (bool, optional): Whether to save clean dataset to dataset directory. Defaults to False.
    """
    # Using anime metadata to filtering content
    anime = dataset(save_clean_dataset)

    # delete unused columns
    del anime['animeNameLower']
    del anime['animeID']

    # will be used for binary features
    anime_features = anime['animeFeatures']

    # Convert metadata to binary features
    del anime['animeFeatures']

    # TODO:
    del anime['animeName']
    del anime['animeGenres']
    del anime['animeSynopsis']
    del anime['animeType']
    del anime["animeProducers"]
    del anime["animeLicensors"]
    del anime["animeStudios"]
    del anime["animeSource"]

    catCols = anime.select_dtypes(exclude=['int64', 'float64']).columns
    numCols = anime.select_dtypes(exclude=['object']).columns

    # TODO:
    for col in catCols:
        anime = preprocessing_category(anime, col)

    anime[numCols] = MinMaxScaler().fit_transform(anime[numCols])
    anime = anime.values 
    print(anime.shape)

    np.save("data/binary/animeMetadata.npy", anime)
    print("Success generate new binary to data/dataset/animeMetadata.npy!")
    del anime

    # currently only support english, and analyze based on word (since this is document dataset)
    matVet = TfidfVectorizer(
        stop_words='english', analyzer='word',
        ngram_range=(1,3), min_df=3, 
        strip_accents='unicode', max_features=None,
        token_pattern=r'\w{1,}'
    )

    animeFeatures = matVet.fit_transform(anime_features)

    save_npz("data/binary/animeFeatures.npz", animeFeatures)
    print("Success generate new binary to data/dataset/animeFeatures.npz!")
