from numpy import mean
from numpy import std
import numpy as np
import os
import cv2
from matplotlib import pyplot as plt
from sklearn.model_selection import KFold
from contextlib import redirect_stdout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.optimizers import SGD

n_folds =5
ROOT_DIRECTORY = '/Users/danieltossaint/Documents/GitHub/Project3-1/data/images' # root directory path
TRAIN_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'train') # path train directory
TEST_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'test') # path test

def loading_frame(path):
    frame = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # Fit to input size
    frame = cv2.resize(frame, (28, 28))
    frame = np.expand_dims(frame, axis=-1)
    return frame.astype(np.float32)

# encode labels
def labeler(labels):
    mapper = {'blank': 0, 'nough': 1, 'circle': 2}
    encoded = [mapper[label] for label in labels]
    targeto = to_categorical(encoded,0)
    return targeto

def loading_data(root_directory, shuffle=True):
    X_SET, y_set = [], []
    for root, dirs, files in os.walk(root_directory):
        for class_directory in dirs:
            image_directory = os.path.join(root_directory, class_directory)
            y_set.extend(np.tile(class_directory, len(os.listdir(image_directory))))
            for frame_FN in os.listdir(image_directory):
                img = loading_frame(os.path.join(image_directory, frame_FN))
                X_SET.append(img)
    y_set = labeler(y_set)
    if shuffle:
        # Combine to maintain order
        data = list(zip(X_SET, y_set))
        np.random.shuffle(data)
        X_SET, y_set = zip(*data)
    return np.asarray(X_SET), np.asarray(y_set)


"""load training and test set and reshape"""

def data_loading():
    (train_x, train_y) = loading_data(TRAIN_DIRECTORY)
    (test_x, test_y) = loading_data(TEST_DIRECTORY)
    train_x = train_x.reshape((train_x.shape[0], 28, 28,1))
    test_x = test_x.reshape((test_x.shape[0], 28, 28,1))
    return train_x, train_y, test_x, test_y

""" scale pixel and convert integers to floats, returns  normilzed images  """
def pixels_scaler(train, test):

    train_normilize = train.astype('float32')
    test_normmilize = test.astype('float32')

    train_normilize = train_normilize / 255.0
    test_normmilize = test_normmilize / 255.0

    return train_normilize, test_normmilize


# define cnn model
def define_model():
	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
	model.add(MaxPooling2D((2, 2)))
	model.add(Flatten())
	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(3, activation='softmax'))
	# compile model
	opt = SGD(learning_rate=0.01, momentum=0.9)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return model


"""Define model"""

def model_builder():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(3, activation='softmax'))
    opt = SGD(learning_rate=0.01, momentum=0.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# evaluate a model using k-fold cross-validation
def evaluate_model(data_x, data_y, n_folds=n_folds):
    scores, histories = list(), list()
    # prepare cross validation
    kfold = KFold(n_folds, shuffle=True, random_state=1)
    # enumerate splits
    for train_ix, test_ix in kfold.split(data_x):
        # define model
        #model = model_builder()
        model = define_model()
        # select rows for train and test
        train_x, train_y, test_x, test_y = data_x[train_ix], data_y[train_ix], data_x[test_ix], data_y[test_ix]
        # fit model
        hist = model.fit(train_x, train_y, epochs=20, batch_size=32, validation_data=(test_x, test_y), verbose=0)
        # evaluate model
        _, acc = model.evaluate(test_x, test_y, verbose=0)
        print('> %.3f' % (acc * 100.0))
        # stores scores
        scores.append(acc)
        histories.append(hist)
    return scores, histories


"""plot diagnostic learning curves, for cross entropy loss and classifaction accuracy """
def diagnostics(histories):
    for i in range(len(histories)):
        plt.subplot(2, 1, 1)
        plt.title('Cross Entropy Loss')
        plt.plot(histories[i].history['loss'], color='blue', label='train')
        print(histories[i].history['loss'])
        plt.plot(histories[i].history['val_loss'], color='orange', label='test')
        plt.subplot(2, 1, 2)
        plt.title('Classification Accuracy')
        plt.plot(histories[i].history['accuracy'], color='blue', label='train')
        plt.plot(histories[i].history['val_accuracy'], color='orange', label='test')
    plt.show()


"""Prints Preformance and creates boxplot"""
def performance(scores):
    print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(scores) * 100, std(scores) * 100, len(scores)))
    plt.boxplot(scores)
    plt.show()

''' evaluates model , loads datatset and evaluates the model '''
def run_test():
    train_x, train_y, test_x, test_y = data_loading()
    train_x, test_x = pixels_scaler(train_x, test_x)
    scores, histories = evaluate_model(train_x, train_y)
    diagnostics(histories)
    performance(scores)
    model = model_builder()
    #model = define_model()
    model.fit(train_x, train_y, epochs=20, batch_size=32, verbose=0)
    model.save('model_daniel_newdata.h5')
    with open('deepermodelsummary.txt', 'w') as f:
      with  redirect_stdout(f):
        model.summary()



run_test()