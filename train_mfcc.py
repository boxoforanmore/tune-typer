from pathlib import Path
import numpy as numpy
import scipy
import tensorflow as tf
from python_speech_features import mfcc

TT_DIR = 'data/tune_types'

TUNE_TYPES = ['reel', 'jig', 'slipjig', 'polka', 'hornpipe', 'slow air']

def read_ceps(tune_types, base_dir=TT_DIR):
    data = []
    labels = []

    for label, tune_type in enumerate(tune_types):
        tt_dir = Path(base_dir) / tune_type

        for fn in tt_dir.glob('*.ceps.npy'):
            ceps = np.load(fn)
            num_ceps = len(ceps)

            # Average per coefficient over all frames for better generalization
            data.append(np.mean(ceps), axis=0)
            labels.append(label)

    return np.array(data), np.array(y)



