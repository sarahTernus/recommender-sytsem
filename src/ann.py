import tensorflow as tf
from keras import Sequential, layers
from src import createDataframes


def create_model():
    # define the keras model
    model = Sequential()
    model.add(layers.Dense(6, input_dim=2, activation='relu'))
    model.add(layers.Dense(6, activation='relu'))
    model.add(layers.Dense(1))
    model.summary()
    return model


def main():
    df = createDataframes.rating_reduced()
    print(df.to_string())
    x = df.iloc[:, 0:2]
    y = df.iloc[:, 2:3]
    model = create_model()
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x, y, batch_size=32, epochs=12, validation_split=0.2, shuffle=True)

    predictions = model.predict(x)
    rounded = [round(x[0]) for x in predictions]
    print(rounded)


if __name__ == '__main__':
    main()
