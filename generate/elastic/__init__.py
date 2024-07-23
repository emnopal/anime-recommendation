from .to_elastic import generate_elastic

def run_elastic():
    csv_files = "data/dataset/anime_clean.csv"
    generate_elastic(csv_files=csv_files)
