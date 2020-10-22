import pandas as pd
import numpy as np

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
from datetime import datetime
from os import system

ticker_data = pd.read_csv("../StockData/MSFT.csv")

ticker_array = np.array(ticker_data)

start_time_stamp = datetime.fromisoformat(ticker_array[0][0]).timestamp()*1000
one_week_length = 604800000

two_weeks = start_time_stamp + (one_week_length*1)
three_weeks = start_time_stamp + (one_week_length*2)

learning_data = []
guessing_data = []

temp_two_week = []
temp_one_week = []

two_week_max = 0
one_week_max = 0

print(f'start: {datetime.fromtimestamp(start_time_stamp/1000)}')

x = 0

for point in ticker_array:

    # print(point)

    x+=1
    
    point_timestamp = datetime.fromisoformat(point[0]).timestamp()*1000

    point[0] = point_timestamp

    if point_timestamp < three_weeks:

        if point_timestamp < two_weeks:

            temp_two_week.append(point)

        else:

            temp_one_week.append(point)

    else:
        # system('cls')

        # for x in range(10000):
        #     print(x)
        
        temp_two_week = np.array(temp_two_week)
        temp_one_week = np.array(temp_one_week)


        n = 9600
        n = 4800
        input_matrix = np.zeros((n, 7)) - 1
        input_matrix[:temp_one_week.shape[0],:temp_one_week.shape[1]] = temp_one_week

        n = 4800
        objective_matrix = np.zeros((n, 7)) - 1
        objective_matrix[:temp_one_week.shape[0],:temp_one_week.shape[1]] = temp_one_week

        # print(input_matrix)

        # exit(0)

        learning_data.append(input_matrix)
        guessing_data.append(objective_matrix)

        if len(input_matrix) > two_week_max: two_week_max = len(input_matrix)

        if len(objective_matrix) > one_week_max: one_week_max = len(objective_matrix)

        temp_one_week, temp_two_week = ([],[])
 
        

        start_time_stamp+=one_week_length*3
        two_weeks = start_time_stamp + (one_week_length*2)
        three_weeks = start_time_stamp + (one_week_length*3)
        # break

print(f'end: {datetime.fromtimestamp(start_time_stamp/1000)}')

# print(f'l: {learning_data[0][0]}\n\n')
# print(f'g: {guessing_data[-1][0]}')

# print('two week max: ' + str(two_week_max))
# print('one week max: ' + str(one_week_max))


print(len(guessing_data[0]))

# exit(0)

ticker_model = tf.keras.Sequential([
    layers.Dense(9600),
    layers.Dense(4800, activation='relu'),
    layers.Dense(64),
    layers.Dense(7)
])



ticker_model.compile(loss = tf.losses.MeanAbsoluteError(),
                      optimizer = tf.optimizers.Adam(),
                      metrics=['accuracy'])


for y in range(5):
    for x in range(100):
        print(x)
        print(ticker_model.fit(learning_data[x], guessing_data[x], epochs=5))



# print(ticker_array)


