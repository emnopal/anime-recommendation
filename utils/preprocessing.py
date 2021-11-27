import sys; sys.path.append('..')  # noqa

import pandas as pd
import numpy as np

from scipy.sparse import load_npz
from exceptions.exceptions import (
    ConnectionError,
    FileNotSupported
)


def readDataset(dataset, con=None, index_col=None):#'animeIndex'
    if ".csv" in dataset:
        return pd.read_csv(dataset, index_col=index_col)
    if "select" == dataset[:6]:
        if con is None:
            raise ConnectionError("connection is not defined")
        df = pd.read_sql(dataset, con=con, index_col=index_col)
        df.index = df.index - 1
        return df
    else:
        raise FileNotSupported("file type not supported")


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
