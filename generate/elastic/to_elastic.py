import os
import pandas as pd
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from utils.profiling import timeit

load_dotenv()

INDEX = "animedb.anime"
ES_HOST = os.environ['ELASTIC_HOST']
ES_USER = os.environ['ELASTIC_USER']
ES_PASSWORD = os.environ['ELASTIC_PASSWORD']

@timeit
def generate_elastic(csv_files):
    es = Elasticsearch('http://localhost:9200', basic_auth=(ES_USER, ES_PASSWORD), verify_certs=False)
    df = pd.read_csv(csv_files)

    try:
        mapping_body = {
            "mappings": {
                "properties": {
                    "animeIndex": {"type": "integer"},
                    "animeID": {"type": "integer"},
                    "animeName": {"type": "text"},
                    "animeScore": {"type": "float"},
                    "animeGenres": {"type": "text"},
                    "animeSynopsis": {"type": "text"},
                    "animeType": {"type": "text"},
                    "animeEpisodes": {"type": "integer"},
                    "animeAired": {"type": "text"},
                    "animePremiered": {"type": "text"},
                    "animeProducers": {"type": "text"},
                    "animeLicensors": {"type": "text"},
                    "animeStudios": {"type": "text"},
                    "animeSource": {"type": "text"},
                    "animeDuration": {"type": "text"},
                    "animeRating": {"type": "text"},
                    "animeRanked": {"type": "integer"},
                    "animePopularity": {"type": "integer"},
                    "animeFavorites": {"type": "integer"}
                }
            }
        }

        if not es.indices.exists(index=INDEX):
            es.indices.create(index=INDEX, body=mapping_body)
        
        for i, row in df.iterrows():
            body = {
                "animeIndex": i+1,
                "animeID": row[0],
                "animeName": row[1],
                "animeScore": row[2],
                "animeGenres": row[3],
                "animeSynopsis": row[4],
                "animeType": row[5],
                "animeEpisodes": row[6],
                "animeAired": row[7],
                "animePremiered": row[8],
                "animeProducers": row[9],
                "animeLicensors": row[10],
                "animeStudios": row[11],
                "animeSource": row[12],
                "animeDuration": row[13],
                "animeRating": row[14],
                "animeRanked": row[15],
                "animePopularity": row[16],
                "animeFavorites": row[17]
            }
            es.index(index=INDEX, body=body, id=i+1)
            print(f"Converting row {i+1} ({row[1]}) to Elastic db")
        print(f"Success convert {csv_files} to Elastic db")
        es.transport.close()

    except Exception as e:
        print("Error while connecting to Elastic", e)
