from utils.to_sql import ToSQL

if __name__ == '__main__':
    csv_files = "data/dataset/anime_clean.csv"

    query = """
            create table anime (
                animeIndex int not null auto_increment,
                animeID int,
                animeName varchar(1000),
                animeScore decimal(3, 2),
                animeGenres varchar(255),
                animeSynopsis text,
                animeType varchar(255),
                animeEpisodes int,
                animePremiered varchar(255),
                animeStudios varchar(255),
                animeSource varchar(255),
                animeRating varchar(255),
                animeRanked int,
                animePopularity int,
                animeFavorites int,
                primary key (animeIndex)
            );
            """

    conn = ToSQL()

    conn.from_csv(csv_files=csv_files, db_name='animedb', table_name='anime', query=query)