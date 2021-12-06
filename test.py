from src.app import ContentBasedFiltering
from utils.exporting import (
    convert_to_html,
    convert_to_json,
    convert_to_json_api
)
from src.fetch_from_sql import connect


if __name__ == "__main__":
    conn = connect()
    set_index = 'animeIndex'
    #db_name = 'animedb'
    #query = f'select * from {db_name}.anime'
    #dataset = readDataset(dataset=query, con=conn, index_col=set_index)
    #dataset = "data/dataset/anime_clean.csv"
    vector = "data/binary/anime_metadata.npy"
    vector1 = "data/binary/animeFeaturesTfidf.npz"
    content = ContentBasedFiltering(vector1=vector, vector2=vector1, dataset='use SQL', index_col=set_index, conn=conn)
    OriginalsDf, similarDf = content.mostSimilarByName("Jojo")
    convert_to_html(OriginalsDf, similarDf)
    convert_to_json(OriginalsDf, similarDf)
