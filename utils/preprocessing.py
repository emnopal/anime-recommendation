import sys; sys.path.append('..')  # noqa

import pandas as pd
import numpy as np

from scipy.sparse import load_npz
from exceptions.exceptions import FileNotSupported


def readDataset(dataset):
    return pd.read_csv(dataset)


def readnpz(file):
    return load_npz(file)


def readnpy(file):
    return np.load(file)


def readBinary(file):
    if 'npz' in file:
        return readnpz(file)
    elif 'npy' in file:
        return readnpy(file)
    else:
        raise FileNotSupported("file type not supported")
