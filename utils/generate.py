import os, sys; sys.path.append('..')
import time
import re

import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from scipy.sparse import csr_matrix, save_npz
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelBinarizer, MultiLabelBinarizer, MinMaxScaler

from exceptions.exceptions import DirectoryNotFound


def check_path(path):
    if not os.path.exists(path):
        raise DirectoryNotFound(f"{path} not found")
    else:
        print(f"Pass! {path}")

def check_files(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} not found")
    else:
        print(f"Pass! {path}")

def check_directory():
    time.sleep(1)
    check_path("data")
    time.sleep(1)
    check_path("data/binary")
    time.sleep(1)
    check_path("data/dataset")
    time.sleep(1)
    check_path("data/raw")
    time.sleep(1)

def check_files_in_directory():
    time.sleep(1)
    check_files("data/raw/anime_with_synopsis.csv")
    time.sleep(1)
    check_files("data/raw/anime.csv")
    time.sleep(1)

# source: https://www.kaggle.com/indralin/try-content-based-and-collaborative-filtering
# Cleaning text
def text_cleaning(text):
    stopword = set(stopwords.words('english'))
    text = text.lower()
    text = re.sub(r'&quot;', '', text)
    text = re.sub(r'.hack//', '', text)
    text = re.sub(r'&#039;', '', text)
    text = re.sub(r'A&#039;s', '', text)
    text = re.sub(r'I&#039;', 'I\'', text)
    text = re.sub(r'&amp;', 'and', text)
    text = re.sub('[/(){}\[\]\|@,;]', ' ', text)
    text = re.sub('[^0-9a-z #+_]', '', text)
    text = ' '.join(word for word in text.split() if word not in stopword)
    return text

def preprocessing_category(df, column, is_multilabel=False):
        # Binarise labels
        lb = LabelBinarizer()
        if is_multilabel:
            lb = MultiLabelBinarizer()
        expandedLabelData = lb.fit_transform(df[column])
        labelClasses = lb.classes_

        # Create a pandas.DataFrame from our output
        category_df = pd.DataFrame(expandedLabelData, columns=labelClasses)
        del df[column]
        return pd.concat([df, category_df], axis=1)

def create_dataset():
    # Reading anime with synopsis
    animeSynopsis = pd.read_csv("data/raw/anime_with_synopsis.csv").rename(columns={'sypnopsis': 'Synopsis'})

    # Cleaning anime with synopsis
    animeSynopsis['MAL_ID'] = animeSynopsis['MAL_ID'].replace("Unknown", 0).fillna(0).astype('int64')
    animeSynopsis['Score'] = animeSynopsis['Score'].replace("Unknown", 0).fillna(0).astype('float64')
    animeSynopsis = animeSynopsis.fillna("Unknown")

    # Reading anime list
    useCols = ['MAL_ID', 'Type', 'Popularity', 'Favorites', 'Ranked', 'Episodes', 'Rating', 'Premiered', 'Studios', 'Source']

    animeList = pd.read_csv("data/raw/anime.csv", usecols=useCols)

    # Cleaning anime list
    animeList['Ranked'] = animeList['Ranked'].replace("Unknown", 0).fillna(0).astype('float64')
    animeList['MAL_ID'] = animeList['MAL_ID'].replace("Unknown", 0).fillna(0).astype('int64')
    animeList['Episodes'] = animeList['Episodes'].replace("Unknown", 0).fillna(0).astype('int64')
    animeList['Favorites'] = animeList['Favorites'].replace("Unknown", 0).fillna(0).astype('int64')
    animeList['Popularity'] = animeList['Popularity'].replace("Unknown", 0).fillna(0).astype('int64')
    animeList = animeList.fillna("Unknown")

    # Merge animeList dataframe and animeSynopsis dataframe
    anime = pd.merge(animeSynopsis, animeList, on='MAL_ID')

    useCols = ["Genres", "Name", "Type", "Source", "Rating", "Premiered", "Studios"]
    anime["Features"] = anime["Synopsis"].str.cat(anime[useCols], sep=" ")
    anime["Features"] = anime["Features"].apply(text_cleaning)
    anime["name_lower"] = anime["Name"].apply(lambda x: x.lower())

    anime = anime.rename({
                'MAL_ID': 'animeID',
                'Name': 'animeName',
                'Score': 'animeScore',
                'Genres': 'animeGenres',
                'Synopsis': 'animeSynopsis',
                'Type': 'animeType',
                'Episodes': 'animeEpisodes',
                'Premiered' : 'animePremiered',
                'Source': 'animeSource',
                'Rating': 'animeRating',
                'Studios': 'animeStudios',
                'Favorites': 'animeFavorites',
                'Popularity': 'animePopularity',
                'Ranked': 'animeRanked',
                'Features': 'animeFeatures',
                'name_lower': 'animeNameLower'
            }, axis=1)

    anime.to_csv('data/dataset/anime_clean.csv', index=False)
    print(f"Success generate new datasets to data/dataset/anime_clean.csv!")
    return anime

def generate_binary():
    # Using anime metadata to filtering content

    anime_metadata = create_dataset().copy()

    del anime_metadata['animeFeatures']
    del anime_metadata['animeName']
    del anime_metadata['animeGenres']
    del anime_metadata['animeNameLower']
    del anime_metadata['animeSynopsis']
    del anime_metadata['animeID']

    catCols = anime_metadata.select_dtypes(exclude=['int64', 'float64']).columns
    numCols = anime_metadata.select_dtypes(exclude=['object']).columns

    for col in catCols:
        anime_metadata = preprocessing_category(anime_metadata, col)

    anime_metadata[numCols] =  MinMaxScaler().fit_transform(anime_metadata[numCols])
    anime_metadata = anime_metadata.values
    print(anime_metadata.shape)

    np.save("data/binary/anime_metadata.npy", anime_metadata)

    matVet = TfidfVectorizer(stop_words='english',
                            analyzer='word',
                            ngram_range=(1,3),
                            min_df=3,
                            strip_accents='unicode',
                            max_features=None,
                            token_pattern=r'\w{1,}')
                            # currently only support english, and analyze based on word (since this is document dataset)

    animeFeatures = anime['animeFeatures'].copy()
    animeFeaturesTfidf = matVet.fit_transform(animeFeatures)

    save_npz("../data/binary/animeFeaturesTfidf.npz", animeFeaturesTfidf)
    print(f"Success generate new binary to data/dataset/anime_metadata.npy!")
    print(f"Success generate new binary to data/dataset/animeFeaturesTfidf.npz!")

def generate():
    check_directory()
    check_files_in_directory()
    create_dataset()
    generate_binary()
