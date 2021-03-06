from pathlib import Path
import numpy as numpy
import scipy
import tensorflow as tf
import tensorflow.keras as keras
from python_speech_features import mfcc

TT_DIR = 'data/tune_types'
TEST_DIR = 'test/tune_types'


TUNE_TYPES = ['reel', 'jig', 'slipjig', 'polka', 'hornpipe', 'slow air']


def load_ceps(tune_types, base_dir=TT_DIR):
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

# Try for 70/30 split of data
X_train, y_train = load_ceps(tune_types=TUNE_TYPES)
X_test, y_test = load_ceps(tune_types=TUNE_TYPES, base_dir=TEST_DIR)

print()
print('X_train => Rows: %d, Columns: %d' % (X_train.shape[0], X_train.shape[1])
print()
print('X_test  => Rows: %d, Columns: %d' % (X_test.shape[0], X_test.shape[1])
print()
print()


'''
# Is standardization necessary here since mfcc was done?
# For standardization
mean_vals = np.mean(X_train, axis=0)
std_val = np.std(X_train)

X_train_centered = (X_train - mean_vals) / std_val
X_test_centered = (X_train - mean_vals) / std_val

del X_train, X_test

'''

# Set random seed
np.random.seed(123)
tf.set_random_seed(123)

# Onehot encode the labels
y_train_onehot = keras.utils.to_categorical(y_train)

print()
print('First 3 labels: ', y_train[:3])
print()
print('First 3 labels (one-hot): \n', y_train_onehot[:3])
print()


# Add a feedforward network
model = keras.models.Sequential()

# Input layer; input dimensions must match number of features in the training set
# Number of output and input units in two consecutive layers must also match

model.add(keras.layers.Dense(units=100, input_dim=X_train.shape[1],
                             kernel_initializer='glorot_uniform',
                             bias_initializer='zeros',
                             activation='tanh'))

model.add(keras.layers.Dense(units=100, input_dim=100,
                             kernel_initializer='glorot_uniform',
                             bias_initializer='zeros',
                             activation='tanh'))

model.add(keras.layers.Dense(units=y_train_onehot.shape[1], input_dim=50, 
                             kernel_initializer='glorot_uniform',
                             bias_initializer='zeros',
                             activation='softmax'))

# Using SGD for more time efficient activation; 
# need to play with decay rate
sgd_optimizer = keras.optimizers.SGD(lr=0.001, decay=1e-7, momentum=.9)

# Crossentropy is the generalization of logistic regression for
# multiclass predictions via softmax
model.compile(optimizer=sgd_optimizer, loss='categorical_crossentropy')


# Train with fit method
history = model.fit(X_train_centered, y_train_onehot,
                    batch_size=64, epochs=50, verbose=1,
                    validation_split=0.1)


# Predict class labels (return class labels as integers)
y_train_pred = model.predict_classes(X_train_centered, verbose=0)
correct_preds = np.sum(y_train == y_train_pred, axis=0)
train_acc = correct_preds / y_train.shape[0]

print()
print('First 3 predictions: ', y_train_pred[:3])
print()
print('Training accuracy: %.2f%%' % (train_acc * 100))
print()

y_test_pred = model.predict_classes(X_test_centered, verbose=0)

correct_preds = np.sum(y_test == y_test_pred, axis=0)
test_acc = correct_preds / y_test.shape[0]

print('Test accuracy: %.2f%%' % (test_acc * 100))
print()
