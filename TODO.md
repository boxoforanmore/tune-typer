1) Create dataset of music files (30 sec mp3, sampling rate?)
    -Place each item into a corresponding file (reel, jig, hornpipe, etc) for class labels
    -Shoot for 100 training per class

2) Convert mp3s to WAV w/ scipy or librosa

3) Extract features with FFT

4) Build NN with TF or keras

5) Play with hyperparameters

6) Save serialized nn for reclassification of new samples

7) Add script with accuracy predictor for testing on unseen data

8) Add database and retraining mechanism
