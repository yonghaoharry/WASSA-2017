import numpy as np
import pandas as pd

from gensim import corpora
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import SnowballStemmer

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM
from sklearn import preprocessing
from sklearn.metrics import (precision_score, recall_score,
                             f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
np.random.seed(0)
from keras.optimizers import RMSprop
from keras import callbacks
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
import os
import math

if __name__ == "__main__":

    #load data
    #train_df = pd.read_csv('data/training/joy-ratings-0to1.train.txt', sep='\t', header=0)
    test_df = pd.read_csv('data/testing/joy-ratings-0to1.test.target.txt', sep='\t', header=0)

    #raw_docs_train = train_df['tweet'].values
    raw_docs_test = test_df['tweet'].values
    
    #sentiment_train = train_df['score'].values
    sentiment_test = test_df['score'].values
    
    #y_train = np.array(sentiment_train)
    y_test = np.array(sentiment_test)

    #text pre-processing
    stop_words = set(stopwords.words('english'))
    stop_words.update(['.', ',', '"', "'", ':', ';', '(', ')', '[', ']', '{', '}'])
    stemmer = SnowballStemmer('english')

    print "pre-processing train docs..."
    #processed_docs_train = []
    #print(raw_docs_train)
    #np.savetxt("traindata.txt",raw_docs_train,fmt="%s")
    #for doc in raw_docs_train:
    #   doc = doc.decode("utf8")
    #   tokens = word_tokenize(doc)
    #   filtered = [word for word in tokens if word not in stop_words]
    #   stemmed = [stemmer.stem(word) for word in filtered]
    #   processed_docs_train.append(stemmed)
   
    print "pre-processing test docs..."
    processed_docs_test = []
    for doc in raw_docs_test:
       doc = doc.decode("utf8")
       tokens = word_tokenize(doc)
       filtered = [word for word in tokens if word not in stop_words]
       stemmed = [stemmer.stem(word) for word in filtered]
       processed_docs_test.append(stemmed)

    #processed_docs_all = np.concatenate((processed_docs_train, processed_docs_test), axis=0)
    processed_docs_all = processed_docs_test

    dictionary = corpora.Dictionary(processed_docs_all)
    dictionary_size = len(dictionary.keys())
    print "dictionary size: ", dictionary_size 
    #dictionary.save('dictionary.dict')
    #corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    #print "converting to token ids..."
    #word_id_train, word_id_len = [], []
    #for doc in processed_docs_train:
    #    word_ids = [dictionary.token2id[word] for word in doc]
    #    word_id_train.append(word_ids)
    #    word_id_len.append(len(word_ids))

    word_id_test, word_id_len = [], []
    for doc in processed_docs_test:
        word_ids = [dictionary.token2id[word] for word in doc]
        word_id_test.append(word_ids)
        word_id_len.append(len(word_ids))
 
    seq_len = np.round((np.mean(word_id_len) + 2*np.std(word_id_len))).astype(int)

    #pad sequences
    #word_id_train = sequence.pad_sequences(np.array(word_id_train), maxlen=seq_len)
    word_id_test = sequence.pad_sequences(np.array(word_id_test), maxlen=seq_len)
   
    
    

    #LSTM
    print "fitting LSTM ..."
    model = Sequential()
    model.add(Embedding(dictionary_size, 256, dropout=0.2))
    model.add(LSTM(256, dropout_W=0.2, dropout_U=0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='rmsprop')
    model.load_weights("logs/joy/checkpoint-08.hdf5")
    print("---------------------------------------")
    print(word_id_test)
    testPredict = model.predict(word_id_test)
    np.savetxt("joy.txt", testPredict, fmt="%1.3f")

    #for file in os.listdir("logs/joy/"):
    #   model.load_weights("logs/joy/"+file)
    #   print("---------------------------------------")
    #   print(file)
    #   testPredict = model.predict(word_id_test)
    #   trainScore = math.sqrt(mean_squared_error(y_test, testPredict))
    #   print('Test Score: %.2f RMSE' % (trainScore))


 
    
