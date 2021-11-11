from src.app import ContentBasedFiltering
from utils.exporting import (
    convert_to_html,
    convert_to_json,
    convert_to_json_api
)


if __name__ == "__main__":
    dataset = "data/dataset/anime_clean.csv"
    vector = "data/binary/anime_metadata.npy"
    vector1 = "data/binary/animeFeaturesTfidf.npz"
    content = ContentBasedFiltering(dataset=dataset, vector1=vector, vector2=vector1)  # noqa
    OriginalsDf, similarDf = content.mostSimilarByName("Jojo")
    convert_to_html(OriginalsDf, similarDf)
    convert_to_json(OriginalsDf, similarDf)
