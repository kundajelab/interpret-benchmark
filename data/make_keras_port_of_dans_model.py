#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

#based on Anna's code at
# https://github.com/kundajelab/kerasAC/blob/a0e3414e93a8b234edb9f6ab4a6012bcf8d03060/kerasAC/architectures/basset_architecture_multitask.py#L19

import numpy as np
np.random.seed(1234)
import keras;
from keras.models import Sequential
from keras.layers.core import Dropout, Reshape, Dense, Activation, Flatten
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.optimizers import Adadelta, SGD, RMSprop;
import keras.losses;
from keras.constraints import maxnorm;
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l1, l2    
from keras import backend as K

ntasks=5

data=np.load("encode-roadmap.dnase_tf-chip.batch_256.params.npz");
model=Sequential()
model.add(Conv1D(filters=300,kernel_size=19,input_shape=(1000,4),weights=[data['0.Conv/weights:0'].squeeze(),np.zeros(300,)],padding="same"))
model.add(BatchNormalization(axis=-1,weights=[data['2.BatchNorm/gamma:0'],data['1.BatchNorm/beta:0'],np.zeros(300,),np.zeros(300,)]))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=3))
model.add(Conv1D(filters=200,kernel_size=11,weights=[data['3.Conv_1/weights:0'].squeeze(),np.zeros(200,)],padding="same"))
model.add(BatchNormalization(axis=-1,weights=[data['5.BatchNorm_1/gamma:0'],data['4.BatchNorm_1/beta:0'],np.zeros(200,),np.zeros(200,)]))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=4))
model.add(Conv1D(filters=200,kernel_size=7,weights=[data['6.Conv_2/weights:0'].squeeze(),np.zeros(200,)],padding="same"))
model.add(BatchNormalization(axis=-1,weights=[data['8.BatchNorm_2/gamma:0'].squeeze(),data['7.BatchNorm_2/beta:0'],np.zeros(200,),np.zeros(200,)]))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=4))
model.add(Flatten())
model.add(Dense(1000,weights=[data['9.fc0/fully_connected/weights:0'],np.zeros(1000,)]))
model.add(BatchNormalization(axis=1,weights=[data['11.fc0/BatchNorm/gamma:0'],data['10.fc0/BatchNorm/beta:0'],np.zeros(1000,),np.zeros(1000,)]))
model.add(Activation('relu'))
model.add(Dropout(0.3))

model.add(Dense(1000,weights=[data['12.fc1/fully_connected/weights:0'],np.zeros(1000,)]))
model.add(BatchNormalization(axis=1,weights=[data['14.fc1/BatchNorm/gamma:0'],data['13.fc1/BatchNorm/beta:0'],np.zeros(1000,),np.zeros(1000,)]))
model.add(Activation('relu'))
model.add(Dropout(0.3))

model.add(Dense(ntasks))
model.add(Activation("sigmoid"))

model.save_weights("dan_basset_keras_port.weights.h5")
json_string = model.to_json()
fh = open("dan_basset_keras_port.arch.json",'w')
fh.write(json_string)
fh.close()
