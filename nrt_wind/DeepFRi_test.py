import os
from PIL import Image
import numpy as np
from pathlib import Path
import tensorflow as tf
import keras
from keras.models import Sequential
from tensorflow.keras.utils import Sequence
from tensorflow.keras.layers import Dropout
from keras.layers import Dense
from keras.layers import Dropout, Flatten 
from keras.layers import Dense  #,Softmax
from keras.layers import Conv2D, MaxPooling2D #, concatenate


def cnn_model_fit_60_30(imgPath,f):
    input_shape = (54,162,1)
    def get_model1():
        model = Sequential() 
        model.add(Conv2D(16, kernel_size=(3, 3), activation='relu',padding='same',input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(4, 4)))
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(4, 4)))
      
        model.add(Flatten())
        model.add(Dense(64, activation='relu'))#32
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))
        return model

    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 0.95
    session = tf.compat.v1.Session(config=config)

    keras.backend.clear_session()

    savedModel = imgPath+"fr_1mres_60mdetrend_nfr_1mres_30mdetrend.h5"
    model = get_model1()
    model.load_weights(savedModel)

    class realflankDataGenerator(Sequence):

        def __init__(self, files, batch_size=1, shuffle=False):
            
            self.batch_size = batch_size
            self.files = files
            self.shuffle = shuffle
            self.on_epoch_end()


        def __len__(self):
            
            'Denotes the number of batches per epoch'

            'If the batch size doesnt divide evenly then add 1'
            diff = (len(self.files) / self.batch_size) - np.floor((len(self.files) / self.batch_size))
            if ( diff > 0 ):
                return int(np.floor(len(self.files) / self.batch_size))+1
            else:
                return int(np.floor(len(self.files) / self.batch_size))

            
        def __getitem__(self, index):
            'Generates one sample of data'

            indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

            # get list of files
            files = [self.files[k] for k in indexes]
            
            n = int(len(files))
            X = np.zeros(shape=(n,54,162))
            y = np.empty(n)
            ix= 0
            for file in files:
                fname = file.name
                if fname[0:4]=='wind':
                    y[ix] = 0
                else: 
                    y[ix] = 1
                temporary = np.array(Image.open(file).convert('L'))
                X[ix,:,:] = temporary/np.max(temporary)
                ix+=1

            # Generate data
            
            X = 1-X
            return X, y
        
        
        def on_epoch_end(self):
            
            'Updates indexes after each epoch'
            self.indexes = np.arange(len(self.files))

    real_path = Path(imgPath).joinpath('concat')           
    with open(f, 'w') as file:
        lst = os.listdir(real_path) # your directory path
        print(len(lst))
        for iq in range(len(lst)):
            real = [x for x in real_path.glob('wind'+str(iq)+'_'+'*.jpg')]
            realGen = realflankDataGenerator(real, batch_size=1)
            ynew = model.predict(realGen)
            file.write(real[0].as_posix()+','+str(ynew[0][0])+'\n')
    return
