"""
script to train ccn to detect X's, O's or None
using keras and open-cv
note: already trained a ccn, weights under data/model.h5
(trained on small data set but seemed to work just fine)


"""


import os
import cv2
import numpy as np

from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.callbacks import EarlyStopping
from keras.preprocessing.image import ImageDataGenerator


# Replicate results
np.random.seed(42)

 # directory paths so training set (data)

 # depends on paths in your system
ROOT_DIRECTORY = '...' # root directory path
TRAIN_DIRECTORY = os.path.join(ROOT_DIRECTORY, '..') # path train directory
TEST_DIRECTORY = os.path.join(ROOT_DIRECTORY, '..') # path test directory
input_shape = (32, 32, 1)
batch_size = 32
epochs = 30

# Build and compile model
training_model = Sequential()
training_model.add(Conv2D(64, (3, 3), input_shape=input_shape, padding='same'))
training_model.add(Activation('relu'))
training_model.add(MaxPooling2D(pool_size=(2, 2)))

training_model.add(Conv2D(32, (3, 3), padding='same'))
training_model.add(Activation('relu'))
training_model.add(MaxPooling2D(pool_size=(2, 2)))
training_model.add(Flatten())

training_model.add(Dense(64))
training_model.add(Activation('relu'))
training_model.add(Dropout(0.4))

# training.model.add(Dense(32))
# training.model.add(Activation('relu'))
# training.model.add(Dropout(0.3))

training_model.add(Dense(3, activation='softmax'))
training_model.summary()

training_model.compile(loss='categorical_crossentropy',
                       optimizer='rmsprop',
                       metrics=['accuracy'])


# Load images
def loading_frame(path):
    frame = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # Fit to input size
    frame = cv2.resize(frame, (32, 32))
    frame = np.expand_dims(frame, axis=-1)
    return frame.astype(np.float32)

# encode labels
def labeler(labels):
    mapper = {'blank': 0, 'nough': 1, 'circle': 2}
    encoded = [mapper[label] for label in labels]
    targeto = to_categorical(encoded)
    return targeto

# load data
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


print('Loading data...')
X_set_train, y_set_train = loading_data(TRAIN_DIRECTORY)
X_set_test, y_set_test = loading_data(TEST_DIRECTORY)
print('instances for training ='+ len(X_set_train))
print('instances for evaluation ='+len(X_set_test))


## super small data set to lets create more :)

train_datagenarator = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=90,
    shear_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    rescale=1 / 255,
    validation_split=0.2)

train_set_generator = train_datagenarator.flow(
    X_set_train, y_set_train, batch_size=batch_size, subset='training')

val_set_generator = train_datagenarator.flow(
    X_set_train, y_set_train, batch_size=batch_size, subset='validation')

# Train and evaluate
callafter = [
    EarlyStopping(patience=5, verbose=1, restore_best_weights=True)]

print('Training model...')
# history
hist = training_model.fit_generator(
    train_set_generator,
    steps_per_epoch=128,
    epochs=epochs,
    validation_data=val_set_generator,
    validation_steps=32,
    callbacks=callafter)

print('Evaluating model...')
# Load data
test_datagen = ImageDataGenerator(rescale=1 / 255)
X_set_test, y_set_test = next(test_datagen.flow(X_set_test, y_set_test, batch_size=len(X_set_test)))

loss, accuracy = training_model.evaluate(X_set_test, y_set_test, batch_size=batch_size)
print('Crossentropy loss:'+loss)
print('Accuracy:' + accuracy)

# Save model
# training.model.save('../data/model.h5')
# print('Saved model to disk')
