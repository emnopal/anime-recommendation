from generate import run_binary

if __name__ == "__main__":
    """
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
            6. Run this script: python generate_data.py
    """
    run_binary()
