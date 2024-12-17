import os

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
import keras_tuner as kt
import matplotlib.pyplot as plt

# Set the number of cores you want to use
num_cores = os.cpu_count()  # This will use all available cores
print(f"Number of cores available: {num_cores}")

# Set TensorFlow to use multiple cores
tf.config.threading.set_intra_op_parallelism_threads(num_cores)
tf.config.threading.set_inter_op_parallelism_threads(num_cores)

# Load and preprocess data
dataset = pd.read_csv('data.csv')
features = dataset.columns[1:179].to_list()
target = 'target_next_30_day_price'
time_steps = 60

scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(dataset[features])

# def create_dataset(X, y, time_steps):
#     Xs, ys = [], []
#     for i in range(len(X) - time_steps):
#         v = X[i:(i + time_steps)]
#         Xs.append(v)
#         ys.append(y[i + time_steps])
#     return np.array(Xs), np.array(ys)
#Preparing the dataset for time series prediction
def create_dataset(X, y, time_steps):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

# Create EarlyStopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='mean_absolute_percentage_error',
    mode='min',
    patience=25,
    restore_best_weights=True
)

def build_model(hp):
    input_shape = (time_steps, len(features))
    number_lstm_layers = hp.Int('number_hidden_lstm_layers', min_value=1, max_value=3, step=1)
    number_dense_layers = hp.Int('number_dense_layers', min_value=1, max_value=2, step=1)
    use_dropout = hp.Boolean('use_dropout')
    model = Sequential()

    # Input LSTM layer
    model.add(Input(shape=input_shape))
    # model.add(LSTM(hp.Choice('lstm_units', [16,32,64,128,256,512]),
    #                activation=hp.Choice('activation', ['relu', 'tanh', 'sigmoid']),
    #                return_sequences=True,input_shape=input_shape))
    model.add(LSTM(hp.Choice('lstm_units', [16,32,64,128,256,512]),
                   activation=hp.Choice('activation', ['relu', 'tanh', 'sigmoid']),
                   return_sequences=True))

    if use_dropout:
        model.add(Dropout(hp.Float('dropout_rate_after_input_layer', 0.1, 0.5, step=0.1)))

    # Hidden LSTM layers
    if number_lstm_layers>1:
        for i in range(number_lstm_layers):
            model.add(LSTM(hp.Choice(f'lstm_units_{i}', [16,32,64,128,256,512]),
                           activation=hp.Choice(f'activation_{i}', ['relu', 'tanh', 'sigmoid']),
                           return_sequences=i < number_lstm_layers-1))
            if use_dropout:
                model.add(Dropout(hp.Float(f'dropout_rate_{i}', 0.1, 0.5, step=0.1)))

    # Dense layers
    if number_dense_layers>1:
      for i in range(number_dense_layers):
          model.add(Dense(hp.Choice(f'dense_units_{i}', [16,32,64,128,256,512]),
                          activation=hp.Choice(f'dense_activation_{i}', ['relu', 'tanh', 'sigmoid'])))
          if use_dropout:
              model.add(Dropout(hp.Float(f'dense_dropout_rate_{i}', 0.1, 0.5, step=0.1)))

    # Output layer
    model.add(Dense(1))

    # Compile model
    model.compile(
        optimizer=Adam(hp.Float('learning_rate', 1e-4, 1e-1, sampling='log')),
        loss='mean_squared_error',
        metrics=['mean_absolute_error', 'mean_absolute_percentage_error']
    )

    return model

# Prepare the full dataset
X = data_scaled
y = dataset[target].values

# Create the dataset with the maximum possible sequence length
X, y = create_dataset(pd.DataFrame(data_scaled, columns=features), dataset[target], time_steps)

#Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Define the Keras Tuner search

tuner = kt.BayesianOptimization(
    build_model,
    objective='mean_absolute_percentage_error',
    max_trials=100,
    seed=1,  # Random seed to use
    num_initial_points=30,  # Number of initial points
    overwrite=False,  # If False, will resume from previous trials.
    # directory='/content/',  # Directory to store tuning results
    project_name='lstm_optimization'
)

# Search for the best hyperparameters

tuner.search(
    X_train, y_train,
    epochs=500,
    # batch_size=64,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=1,
)

# Get the best model
best_model = tuner.get_best_models(num_models=1)[0]

# Print the best hyperparameters
best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
print("Best hyperparameters:")
for hp in best_hps.values:
    print(f"{hp}: {best_hps.get(hp)}")

# Evaluate the best model
test_loss, test_mae, test_mape = best_model.evaluate(X_test, y_test)
print(f"Test loss: {test_loss}")
print(f"Test MAE: {test_mae}")
print(f"Test MAPE: {test_mape}")

# Plot the search results
plt.figure(figsize=(12, 8))
plt.plot(tuner.oracle.trials.values())
plt.xlabel('Trial')
plt.ylabel('Val MAPE')
plt.title('Hyperparameter Search Results')
plt.show()