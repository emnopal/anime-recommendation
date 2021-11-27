# anime-recommendation [BETA]
Anime recommendation using Machine Learning by using Content Based Filtering technique

# Dataset
By default, this repository doesn't contains any dataset, you can download it from these following tutorials:
How to generate data:
  1. Create data directory in parent directory<br>
    `
    |--- anime_recommendation<br>
        |--- data<br>
        |--- ...<br>
    `
  2. Create sub directory binary, dataset and raw<br>
    `
    |--- anime_recommendation<br>
        |--- data<br>
        |--- binary<br>
        |--- dataset<br>
        |--- raw<br>
    |--- ...<br>
    `
  3. Open kaggle dataset: https://www.kaggle.com/hernan4444/anime-recommendation-database-2020<br>
  4. Download only anime_with_synopsis.csv and anime.csv<br>
  5. Put downloaded dataset in raw directory<br>
    `
    |--- anime_recommendation<br>
        |--- data<br>
            |--- binary<br>
            |--- dataset<br>
            |--- raw<br>
                |--- anime_with_synopsis.csv<br>
                |--- anime.csv<br>
        |--- ...<br>
      `
  6. Run this script: `python generate_data.py`<br>
