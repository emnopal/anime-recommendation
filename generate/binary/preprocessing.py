import re
import gc

import pandas as pd
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelBinarizer, MultiLabelBinarizer


def text_cleaning(text: str) -> str:
    """
    Cleaning text from stopwords
    source: https://www.kaggle.com/indralin/try-content-based-and-collaborative-filtering

    Args:
        text (str): Text to clean

    Returns:
        str: Cleaned text
    """
    # read english stopwords
    stopword = set(stopwords.words("english"))

    # cleaning text by regex
    text = text.lower()
    text = re.sub(r"&quot;", "", text)
    text = re.sub(r".hack//", "", text)
    text = re.sub(r"&#039;", "", text)
    text = re.sub(r"A&#039;s", "", text)
    text = re.sub(r"I&#039;", "I\"", text)
    text = re.sub(r"&amp;", "and", text)
    text = re.sub("[/(){}\[\]\|@,;]", " ", text)
    text = re.sub("[^0-9a-z #+_]", "", text)

    # cleaning text from stopwords
    text = " ".join(word for word in text.split() if word not in stopword)
    return text


def preprocessing_category(df: pd.DataFrame, column: str, is_multilabel: bool = False) -> pd.DataFrame:
    """
    Binarise labels

    Args:
        df (pd.DataFrame): Dataframe to binarise
        column (str): Column to binarise
        is_multilabel (bool, optional): Whether the column is multilabel or not. Defaults to False.

    Returns:
        pd.DataFrame: Dataframe with binarised column
    """

    lb = MultiLabelBinarizer() if is_multilabel else LabelBinarizer()

    expanded_label_data = lb.fit_transform(df[column])
    label_classes = lb.classes_

    # Create a pandas.DataFrame from our output
    category_df = pd.DataFrame(expanded_label_data, columns=label_classes)
    del df[column]
    df = pd.concat([df, category_df], axis=1)

    # Explicitly call garbage collection
    gc.collect()
    return df


def dataset(dump: bool = False) -> pd.DataFrame:
    """
    Reading anime list dataset and anime synopsis dataset, merging and cleaning them

    Args:
        dump (bool, optional): Whether to dump the dataset to csv. Defaults to False.

    Returns:
        pd.DataFrame: Clean and merged dataset
    """
    # Reading anime with synopsis
    animeSynopsis = pd.read_csv("data/raw/anime_with_synopsis.csv").rename(columns={"sypnopsis": "Synopsis"})

    # Cleaning anime with synopsis
    animeSynopsis["MAL_ID"] = animeSynopsis["MAL_ID"].replace("Unknown", 0).fillna(0).astype("int64")
    animeSynopsis["Score"] = animeSynopsis["Score"].replace("Unknown", 0).fillna(0).astype("float64")
    animeSynopsis = animeSynopsis.fillna("Unknown")

    # Reading anime list
    # Name, Score and Genres already in animeSynopsis, so no need to read again
    # MAL_ID is for merging ID
    useCols = ["MAL_ID", "Type", "Premiered", "Episodes", "Producers", "Licensors", "Studios", "Source", "Duration", "Rating", "Aired", "Popularity", "Favorites", "Ranked"]

    animeList = pd.read_csv("data/raw/anime.csv", usecols=useCols)

    # Cleaning anime list
    animeList["Ranked"] = animeList["Ranked"].replace("Unknown", 0).fillna(0).astype("float64")
    animeList["MAL_ID"] = animeList["MAL_ID"].replace("Unknown", 0).fillna(0).astype("int64")
    animeList["Episodes"] = animeList["Episodes"].replace("Unknown", 0).fillna(0).astype("int64")
    animeList["Favorites"] = animeList["Favorites"].replace("Unknown", 0).fillna(0).astype("int64")
    animeList["Popularity"] = animeList["Popularity"].replace("Unknown", 0).fillna(0).astype("int64")
    animeList = animeList.fillna("Unknown")

    # Merge animeList dataframe and animeSynopsis dataframe
    anime = pd.merge(animeSynopsis, animeList, on="MAL_ID")

    useCols = ["Name", "Genres", "Type", "Premiered", "Episodes", "Producers", "Licensors", "Studios", "Source", "Duration", "Rating", "Aired"]

    anime["Features"] = anime["Synopsis"].str.cat(anime[useCols].astype(str), sep=" ")
    anime["Features"] = anime["Features"].apply(text_cleaning)
    anime["name_lower"] = anime["Name"].apply(lambda x: x.lower())

    anime = anime.rename({
        "MAL_ID": "animeID", # has number
        "Name": "animeName",
        "Score": "animeScore", # has number
        "Genres": "animeGenres",
        "Synopsis": "animeSynopsis",
        "Type": "animeType",
        "Premiered": "animePremiered", # has number
        "Episodes": "animeEpisodes", # has number
        "Producers": "animeProducers",
        "Licensors": "animeLicensors",
        "Studios": "animeStudios",
        "Source": "animeSource",
        "Duration": "animeDuration", # has number
        "Rating": "animeRating", # has number
        "Aired": "animeAired", # has number
        "Popularity": "animePopularity", # has number
        "Favorites": "animeFavorites", # has number
        "Ranked": "animeRanked", # has number
        "Features": "animeFeatures",
        "name_lower": "animeNameLower"
    }, axis=1)

    if dump:
        anime_clean = anime.copy().drop(["animeNameLower", "animeFeatures"], axis=1)
        anime_clean.to_csv("data/dataset/anime_clean.csv", index=False)
        print("Success save new datasets to data/dataset/anime_clean.csv!")
        del anime_clean

    return anime
