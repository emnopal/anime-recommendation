import os 

from exceptions.exceptions import DirectoryNotFound
from .to_binary import generate_binary

def check_path(path):
    if not os.path.exists(path):
        raise DirectoryNotFound(f"{path} not found")
    else:
        print(f"Pass! {path}")

def check_files(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{path} not found")
    else:
        print(f"Pass! {path}")

def check_directory():
    check_path("data")
    check_path("data/binary")
    check_path("data/dataset")
    check_path("data/raw")

def check_files_in_directory():
    check_files("data/raw/anime_with_synopsis.csv")
    check_files("data/raw/anime.csv")

def run_binary():
    check_directory()
    check_files_in_directory()
    generate_binary(True)