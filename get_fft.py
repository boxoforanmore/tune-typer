from pathlib import Path
import numpy as np
import scipy

# Tune type directory
TT_DIR = 'data/tune_types/'


# Creates and saves the Fourier transformed data as a 
# numpy array to for preprocessing
def create_fft(fname):
    # This should eventually be a librosa call, not scipy
    # Returns the sample rate and the data
    sample_rate, X = scipy.io.wavfile.read(fn)

    # First 1000 components for now; will add more based on
    # model efficiency (or should more be processed and less be read in?
    # Maybe do MFC instead?
    fft_features = abs(scipy.fit(X)[:1000])

    # Save serialized fft of wav file for later use w/ .npy filetype and
    # .fft suffix
    np.save(Path(fname).with_suffix('.ffx'), fft_features)


# Generate FFT for each file
for wav_file in Path(TT_DIR).glob('**/*.wav'):
    create_fft(wav_file)
