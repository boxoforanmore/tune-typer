from pathlib import Path
import librosa
import numpy as np
import scipy

# Tune type directory
TT_DIR = 'data/tune_types/'


# Creates and saves the MFCC coefficient data
# numpy array to for preprocessing
def create_fft(fname):
    # Returns the data and the sample rate
    X, sample_rate = librosa.core.load(fname)

    # MFCC with librosa
    mfcc_features = librosa.feature.mfcc(X)

    # Save serialized cepstrum/MFCC of wav file for later use w/ .npy filetype and
    # .ceps suffix
    np.save(Path(fname).with_suffix('.ceps'), mfcc_features)


# Generate FFT for each file
for wav_file in Path(TT_DIR).glob('**/*.wav'):
    create_fft(wav_file)
