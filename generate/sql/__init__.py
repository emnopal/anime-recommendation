from .to_sql import ToSQL

def run_sql():
    csv_files = "data/dataset/anime_clean.csv"
    query = """
        create table if not exists anime (
            animeIndex int not null auto_increment,
            animeID int,
            animeName text,
            animeScore decimal(3, 2),
            animeGenres text,
            animeSynopsis text,
            animeType text,
            animeEpisodes int,
            animeAired text,
            animePremiered text,
            animeProducers text,
            animeLicensors text,
            animeStudios text,
            animeSource text,
            animeDuration text,
            animeRating text,
            animeRanked int,
            animePopularity int,
            animeFavorites int,
            primary key (animeIndex)
        );
    """
    conn = ToSQL()
    conn.from_csv(csv_files=csv_files, db_name='animedb', table_name='anime', query=query)