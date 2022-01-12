from keras.models import Sequential
from keras.layers import Dense
from keras.datasets import mnist
from keras.utils.np_utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
import pandas as pd


def confusion_matrix(preds, ans):
    data = {'y_Actual':    ans,
            'y_Predicted': preds}
    df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])
    confusion_matrix = pd.crosstab(df['y_Predicted'], df['y_Actual'], rownames=['Predicted'], colnames=['Actual'])
    sn.heatmap(confusion_matrix, annot=True, cmap='Blues', fmt='g')
    plt.show()


(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_labels = to_categorical(train_labels, 10)
test_labels = to_categorical(test_labels, 10)
train_images = train_images / 255.0
test_images = test_images / 255.0
train_images = train_images.reshape(train_images.shape[0], -1)
test_images = test_images.reshape(test_images.shape[0], -1)

# Network initialisation:
network = Sequential()

# Adding layers and no of neurons inside
network.add(Dense(units=16, input_shape=(784,), activation='sigmoid'))
network.add(Dense(units=16, activation='sigmoid'))
network.add(Dense(units=10, activation='softmax'))

network.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training on batches:
batch_size = 20
epochs = 5
network.fit(train_images, train_labels, batch_size, epochs)

test_loss, test_acc = network.evaluate(test_images, test_labels)
print("Test Loss: ", test_loss , " Test Accuracy: ", test_acc)

predicted_lists = network.predict(test_images)
predicted = np.argmax(predicted_lists, axis=1)

answers = np.argmax(test_labels, axis=1)

confusion_matrix(predicted, answers)
