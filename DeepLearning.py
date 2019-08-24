import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import regularizers

class DeepLearning:
    # ["price", "sqft", "bathrooms", "bedrooms", "type", "region", "address", "city"]
    def __init__(self, dataset):
        self.dataset = dataset

    def process(self):
        # isolate and normalize the quantitative data
        X_quantitative = self.dataset[:, [1, 2, 3]]
        scaler = preprocessing.MinMaxScaler()
        X_quantitative = scaler.fit_transform(X_quantitative)
        print(np.array(X_quantitative).shape)

        # isloate and normalize the categorical data
        X_categorial = self.dataset[:, [4,5,7]]
        onehot = preprocessing.OneHotEncoder()
        X_categorial = onehot.fit_transform(X_categorial).toarray()
        print(np.array(X_categorial).shape)
        
        print(X_categorial[0])
        print(X_quantitative[0])
        # get the X (input) and Y (output) datasets

        X_scaled = np.concatenate((X_categorial, X_quantitative), axis=1)
        Y = self.dataset[:, 0]

        # split the data into training (80%) data, and validation data (20%)
        X_train, X_val, Y_train, Y_val = train_test_split(X_scaled, Y, test_size=0.8)

        model = Sequential([
            Dense(1000, activation='relu', kernel_regularizer=regularizers.l2(0.01), input_shape=(50,)),
            Dropout(0.3),
            Dense(1000, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
            Dropout(0.3),
            Dense(1000, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
            Dropout(0.3),
            Dense(1000, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
            Dropout(0.3),
            Dense(1, kernel_regularizer=regularizers.l2(0.01)),
        ])

        # define the loss function and optimizer
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

        # train the data and save the history
        hist = model.fit(X_train, Y_train,
                        batch_size=32, epochs=500,
                        validation_data=[X_val, Y_val])

        # print("Completed training")
        # output = model.evaluate(X_test, Y_test)[1]
        # print(output)

        plt.figure(1)
        plt.plot(hist.history['acc'])
        plt.plot(hist.history['val_acc'])
        plt.title('Accuracy Progression')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='upper right')
        plt.show()

        plt.figure(2)
        plt.plot(hist.history['loss'])
        plt.plot(hist.history['val_loss'])
        plt.title('Loss Progression')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='upper right')
        plt.show()