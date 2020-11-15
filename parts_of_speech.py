# -*- coding: utf-8 -*-
"""parts-of-speech.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1loV3w5snm9S2ybCKF03UaCT0w74uSmn-
"""

from IPython.display import display,HTML
c1,c2,f1,f2,fs1,fs2=\
'#11ff66','#6611ff','Akronim','Smokum',30,20
def dhtml(string,fontcolor=c1,font=f1,fontsize=fs1):
    display(HTML("""<style>
    @import 'https://fonts.googleapis.com/css?family="""\
    +font+"""&effect=3d-float';</style>
    <h1 class='font-effect-3d-float' style='font-family:"""+\
    font+"""; color:"""+fontcolor+"""; font-size:"""+\
    str(fontsize)+"""px;'>%s</h1>"""%string))

dhtml('Code Modules, Setting, & Functions')

import numpy as np,pandas as pd
import pylab as pl,seaborn as sn
import tensorflow_datasets as tfds
from sklearn.feature_extraction.text \
import CountVectorizer
import matplotlib.patheffects as PathEffects
from wordcloud import WordCloud
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers as tkl
from tensorflow.keras import callbacks as tkc

fpath='../input/text-examples-for-processing-classification/'
pl.style.use('seaborn-whitegrid')
fw='weights.best.hdf5'

dhtml('Data Exploration')

data_russian=pd.read_csv(
    fpath+'parts_of_speech_russian.csv')
data_russian.head()

words_russian=np.array(
    [sentence.split() 
     for sentence in data_russian['sentences']])
words_russian=words_russian.reshape(
    words_russian.shape[0]*words_russian.shape[1])
parts_russian=np.array(
    [parts.split() 
     for parts in data_russian['parts_of_speech']])
parts_russian=\
parts_russian.reshape(
    parts_russian.shape[0]*parts_russian.shape[1])
words_russian[:10],parts_russian[:10]

print('Data Statistics. Russian')
print('Number of sentences: {}'\
      .format(len(data_russian['sentences'])))
print('Number of words: {}'\
      .format(len(words_russian)))
print('Parts of speech: \n',
      set(parts_russian))

df_russian=pd.DataFrame(
    {'parts_of_speech':parts_russian,
     'words':words_russian})
pl.figure(figsize=(10,5))
sn.countplot(y="parts_of_speech",data=df_russian,
             facecolor=(0,0,0,0),linewidth=5,
             edgecolor=sn.color_palette("winter"))
pl.title('Russian. Parts of Speech. Distribution',
         fontsize=15);

data_physics=pd.read_csv(
    fpath+'parts_of_speech_physics.csv')
data_physics.head()

words_physics=np.array(
    [sentence.split() 
     for sentence in data_physics['sentences']])
words_physics=words_physics.reshape(
    words_physics.shape[0]*words_physics.shape[1])
parts_physics=np.array(
    [parts.split() 
     for parts in data_physics['parts_of_speech']])
parts_physics=\
parts_physics.reshape(
    parts_physics.shape[0]*parts_physics.shape[1])
words_physics[:10],parts_physics[:10]

print('Data Statistics. Physics')
print('Number of sentences: {}'\
      .format(len(data_physics['sentences'])))
print('Number of words: {}'\
      .format(len(words_physics)))
print('Parts of speech: \n',set(parts_physics))

df_physics=pd.DataFrame(
    {'parts_of_speech':parts_physics,
     'words':words_physics})
pl.figure(figsize=(10,5))
sn.countplot(y="parts_of_speech",data=df_physics,
             facecolor=(0,0,0,0),linewidth=5,
             edgecolor=sn.color_palette("winter"))
pl.title('Physics. Parts of Speech. Distribution',
         fontsize=15);

dhtml("Vocabularies & Sentences' Structure")

def create_lookup_tables(text):
    vocabulary=set(text)
    int_to_vocab=dict(enumerate(vocabulary))
    vocab_to_int=dict((v,k) for k,v \
                      in int_to_vocab.items())
    return vocab_to_int,int_to_vocab
words=np.hstack([words_russian,words_physics])
vocab_to_int,int_to_vocab=\
create_lookup_tables(words)
parts=np.hstack([parts_russian,parts_physics])
part_to_int,int_to_part=\
create_lookup_tables(parts)

int_text_russian=[vocab_to_int[word] for 
                  word in words_russian]
print(int_text_russian[:10])
print(words_russian[:10])
int_parts_russian=[part_to_int[part] 
                   for part in parts_russian]
print(int_parts_russian[:10])
print(parts_russian[:10])

place_in_sentence_russian=\
np.tile(np.array(range(7)),
        len(data_russian['sentences']))
word_lengths_russian=\
np.array([len(i) for i in words_russian])
place_in_sentence_russian.shape

df_russian['word_labels']=int_text_russian
df_russian['part_labels']=int_parts_russian
df_russian['place_in_sentence']=\
place_in_sentence_russian
df_russian['word_lengths']=\
word_lengths_russian
df_russian.head(10)

pl.figure(figsize=(10,6))
sn.countplot(y="parts_of_speech",
             hue='place_in_sentence',
             data=df_russian,palette='winter')
pl.legend(loc=4,title="Places in Sentences")
pl.title('Russian. Distribution by Places in Sentences',
         fontsize=15);

int_text_physics=[vocab_to_int[word] 
                  for word in words_physics]
print(int_text_physics[:10])
print(words_physics[:10])
int_parts_physics=[part_to_int[part] 
                   for part in parts_physics]
print(int_parts_physics[:10])
print(parts_physics[:10])

place_in_sentence_physics=\
np.tile(np.array(range(7)), 
        len(data_physics['sentences']))
word_lengths_physics=\
np.array([len(i) for i in words_physics])
place_in_sentence_physics.shape

df_physics['word_labels']=int_text_physics
df_physics['part_labels']=int_parts_physics
df_physics['place_in_sentence']=\
place_in_sentence_physics
df_physics['word_lengths']=\
word_lengths_physics

pl.figure(figsize=(10,6))
sn.countplot(y="parts_of_speech",
             hue='place_in_sentence',
             data=df_physics,palette='winter')
pl.legend(loc=4,title="Places in Sentences")
pl.title('Physics. Distribution by Places in Sentences',
         fontsize=20);

dhtml('Word Clouds')

wordcloud_russian=WordCloud(
    max_font_size=30,
    background_color='white',
    colormap=pl.cm.winter)\
.generate(' '.join(words_russian))
pe=[PathEffects.withSimplePatchShadow(
    linewidth=4,foreground="gray")]
pl.figure(figsize=(10,11))
pl.imshow(wordcloud_russian,
          interpolation="bilinear")
pl.title("Russian", 
          fontsize=30,fontweight='bold',
          color='#348ABD',path_effects=pe)
pl.axis("off");

wordcloud_physics=WordCloud(
    max_font_size=30,
    background_color='white',
    colormap=pl.cm.winter)\
.generate(' '.join(words_physics))
pe=[PathEffects.withSimplePatchShadow(
    linewidth=4,foreground="gray")]
pl.figure(figsize=(10,11))
pl.imshow(wordcloud_physics,
          interpolation="bilinear")
pl.title("Physics", 
          fontsize=30,fontweight='bold',
          color='#348ABD',path_effects=pe)
pl.axis("off");

#sklearndhtml('Vectorizering')

#sklearn
vectorizer=CountVectorizer(analyzer="word",tokenizer=None, 
                           preprocessor=None,stop_words=None,
                           min_df=0,max_features=1000) 
features=vectorizer.fit_transform([' '.join(words)])
vocabulary=vectorizer.get_feature_names()
word_occurrences=np.sum(features.toarray(),axis=0)
print(features.shape)
print(vocabulary[:100])
print(word_occurrences[:100])

analyzer=vectorizer.build_analyzer()
analyzer(' '.join(words_russian[:7])),\
analyzer(' '.join(words_physics[:7]))

set(df_russian['words'][df_russian['word_lengths']==1])

set(df_physics['words'][df_physics['word_lengths']==1])

#tensorflow
word_set=set(words); n=len(words)
encoder=tfds.features.text.TokenTextEncoder(word_set)
enc_words=[encoder.encode(word)[0] for word in words]
df_russian['enc_words']=enc_words[:len(words_russian)]
df_physics['enc_words']=enc_words[len(words_russian):]
#word_labels=enc_words-1
df_physics.head(10)

dhtml('Binary Classification: Russian vs Physics')

feature_list=['word_labels','part_labels',
              'place_in_sentence','word_lengths']
x=np.vstack([df_russian[feature_list].values,
             df_physics[feature_list].values])
x=x.reshape(x.shape[0]//7,7,4)
x.shape

# labeling texts from two types of studentbooks
# 0 => 'Russian Language', 1 => 'Physics'
zeros=np.zeros((len(words_russian)//7),dtype=int)
ones=np.ones((len(words_physics)//7),dtype=int)
y=np.concatenate((zeros,ones),axis=0)
y.shape

N=y.shape[0]; n=int(.1*N)
shuffle_ids=np.arange(N)
np.random.RandomState(12).shuffle(shuffle_ids)
x=x[shuffle_ids]
y=y[shuffle_ids]
x_test,x_valid,x_train=\
x[:n],x[n:2*n],x[2*n:]
y_test,y_valid,y_train=\
y[:n],y[n:2*n],y[2*n:]

dhtml('NN Models')

def mlp_model():
    model=Sequential()
    model.add(tkl.Dense(1024,activation='relu', 
                        input_shape=(28,)))
    model.add(tkl.Dropout(.1)) 
    model.add(tkl.Dense(64,activation='relu'))
    model.add(tkl.Dropout(.1))
    model.add(tkl.Dense(1,activation='sigmoid'))
    model.compile(optimizer='nadam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model
def cb(fw):
    early_stopping=tkc\
    .EarlyStopping(monitor='val_loss',
                   patience=20,verbose=2)
    checkpointer=tkc\
    .ModelCheckpoint(filepath=fw,verbose=2,
                     save_best_only=True)
    lr_reduction=tkc\
    .ReduceLROnPlateau(monitor='val_loss',verbose=2,
                       patience=5,factor=.75)
    return [checkpointer,early_stopping,lr_reduction]

mlp_model=mlp_model()
history=mlp_model\
.fit(x_train.reshape(-1,28),y_train,
     epochs=100,batch_size=16,verbose=2,
     validation_data=(x_valid.reshape(-1,28),y_valid),
     callbacks=cb(fw))

mlp_model.load_weights(fw)
mlp_model.evaluate(x_test.reshape(-1,28),y_test)

def cnn_model():
    model=Sequential()
    model.add(tkl.Conv1D(32,5,
                         padding='same', 
                         activation='relu',
                         input_shape=(7,4)))
    model.add(tkl.MaxPooling1D(pool_size=2))
    model.add(tkl.Dropout(.25))
    model.add(tkl.Conv1D(96,5,
                         padding='same',
                         activation='relu'))
    model.add(tkl.MaxPooling1D(pool_size=2))
    model.add(tkl.Dropout(.25))
    model.add(tkl.Flatten())  
    model.add(tkl.Dense(1024,activation='relu'))
    model.add(tkl.Dropout(.5))
    model.add(tkl.Dense(1,activation='sigmoid'))
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

cnn_model=cnn_model()
history=cnn_model\
.fit(x_train,y_train,
     epochs=100,batch_size=16,verbose=2,
     validation_data=(x_valid,y_valid),
     callbacks=cb(fw))

cnn_model.load_weights(fw)
cnn_model.evaluate(x_test,y_test)

def rnn_model():
    model=Sequential()
    model.add(tkl.LSTM(28*4,
                       return_sequences=True,
                       input_shape=(7,4)))    
    model.add(tkl.LSTM(28*4,
                       return_sequences=True))
    model.add(tkl.LSTM(28*4))  
    model.add(tkl.Dense(1,activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer='nadam',
                  metrics=['accuracy'])    
    return model

rnn_model=rnn_model()
history=rnn_model\
.fit(x_train,y_train,
     epochs=100,batch_size=16,verbose=2,
     validation_data=(x_valid,y_valid),
     callbacks=cb(fw))

rnn_model.load_weights(fw)
rnn_model.evaluate(x_test,y_test)