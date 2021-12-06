# anime-recommendation
Anime recommendation using Machine Learning by using Content Based Filtering technique

Due to GitHub maximum file size limit, so i don't include the dataset and binaries in the repository.

# Dataset
By default, this repository doesn't contains any dataset, you can download and generate it from these following tutorials:<br>

  1. Create data directory in parent directory<br>

    |--- anime_recommendation
        |--- data
        |--- ...

  2. Create sub directory binary, dataset and raw<br>

    |--- anime_recommendation
        |--- data
        |--- binary
        |--- dataset
        |--- raw
    |--- ...

  3. Open kaggle dataset: [Here](https://www.kaggle.com/hernan4444/anime-recommendation-database-2020)<br>
  4. Download only `anime_with_synopsis.csv` and `anime.csv`<br>
  5. Put downloaded dataset in raw directory<br>

    |--- anime_recommendation
        |--- data
            |--- binary
            |--- dataset
            |--- raw
                |--- anime_with_synopsis.csv
                |--- anime.csv
        |--- ...

  6. Run this script: `python generate_data.py`<br>


# Generate to SQL
By default, this app is using MySQL as databases to store the datasets, if you don't want to use MySQL you can edit some of codes to works with csv data.

But if you want to use MySQL you can run some codes:
  1. `python grant_sql.py` to create new user and grants the user privilege
  2. `python generate_sql.py` to convert CSV to SQL

# Models
This app generates binary data using NLP (Natural Language Processing) with TfidfVectorizer and LabelBinarizer technique, all of technique can be generated from `python generate_data.py` after it, all of binaries appends to K Nearest Neighbors to created Machine Learning models.

# API
By default, this app is using FastAPI to create an API. To run the API, run this file: <br>
  `python main.py`

then, type in the browser `http://127.0.0.1/api` or `http://127.0.0.1/docs` to see documentation.
