# anime-recommendation [BETA]
Anime recommendation using Machine Learning by using Content Based Filtering technique

# Dataset
By default, this repository doesn't contains any dataset, you can download it from these following tutorials:
How to generate data:
  1. Create data directory in parent directory
    --- anime_recommendation
      --- data
      --- ...
  2. Create sub directory binary, dataset and raw
    --- anime_recommendation
      --- data
      --- binary
      --- dataset 
      --- raw
    --- ...
  3. Open kaggle dataset: https://www.kaggle.com/hernan4444/anime-recommendation-database-2020
  4. Download only anime_with_synopsis.csv and anime.csv
  5. Put downloaded dataset in raw directory
    --- anime_recommendation
      --- data
        --- binary
        --- dataset
        --- raw
          --- anime_with_synopsis.csv
          --- anime.csv
      --- ...
  6. Run this script: `python generate_data.py`
