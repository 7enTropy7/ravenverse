from __future__ import print_function

import pickle as pkl

import numpy as np
import ravop as R
from ravdl.neural_networks import NeuralNetwork
from ravdl.neural_networks.layers import Conv2D, Dense, Dropout, BatchNormalization, Activation, Flatten, MaxPooling2D
from ravdl.neural_networks.loss_functions import CrossEntropy
from ravdl.neural_networks.optimizers import Adam
from sklearn import datasets
from sklearn.model_selection import train_test_split


def to_categorical(x, n_col=None):
    if not n_col:
        n_col = np.amax(x) + 1
    one_hot = np.zeros((x.shape[0], n_col))
    one_hot[np.arange(x.shape[0]), x] = 1
    return one_hot


def get_dataset():
    data = datasets.load_digits()
    X = data.data
    y = data.target

    # Convert to one-hot encoding
    y = to_categorical(y.astype("int"))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    # Reshape X to (n_samples, channels, height, width)
    X_train = X_train.reshape((-1, 1, 8, 8))
    X_test = X_test.reshape((-1, 1, 8, 8))

    return X_train, X_test, y_train, y_test


def create_model(X_test, y_test):
    optimizer = Adam()

    model = NeuralNetwork(optimizer=optimizer,
                          loss=CrossEntropy,
                          validation_data=(X_test, y_test))

    model.add(Conv2D(n_filters=16, filter_shape=(3, 3), stride=1, input_shape=(1, 8, 8), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_shape=(2, 2), stride=2))
    model.add(Dropout(0.25))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(stride=2, padding="same"))
    model.add(Conv2D(n_filters=32, filter_shape=(3, 3), stride=1, padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_shape=(2, 2), stride=2))
    model.add(Dropout(0.25))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.4))
    model.add(BatchNormalization())
    model.add(Dense(10))
    model.add(Activation('softmax'))

    model.summary()
    return model


def train(model, X_train, y_train):
    model.fit(X_train, y_train, n_epochs=1, batch_size=256, save_model=True)
    pkl.dump(model, open("cnn_model.pkl", "wb"))


def compile():
    R.activate()


def execute():
    R.execute()
    R.track_progress()
