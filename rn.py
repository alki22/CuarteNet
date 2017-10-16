from __future__ import absolute_import, print_function, unicode_literals

import numpy as np
import random
import re
import sys
import unicodedata
import keras.backend as K

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM, TimeDistributed
from keras.optimizers import RMSprop

filename = 'CuarteCorpus.txt'
with open(filename, 'r') as file:
	text = unicodedata.normalize('NFC', file.read()).lower()
	text = re.sub('\s+', ' ', text).strip()

print('Corpus length:: %d' % len(text))

# Get every different char in corpus
chars = sorted(set(text))

print('Total chars: %d' % len(chars))

char_index = dict((c, i) for i, c in enumerate(chars))
index_char = dict((i, c) for i, c in enumerate(chars))

K.clear_session()

# Dimensions (Default: 64 and 40)
hidden_layer_size = 64
max_len = 30

# Instantiate the model
model = Sequential()

# Add layers to the model
model.add(LSTM(hidden_layer_size, input_shape=(max_len, len(chars)), return_sequences=True))
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(len(chars), activation='softmax')))


model.compile(loss='categorical_crossentropy', optimizer='adam')
model.summary()

# Cut the text in sequences of max_len chars
sentences = []
next_chars = []

for i in range(0, len(text) - max_len - 1, max_len):
	sentences.append(text[i:i + max_len])
	next_chars.append(text[i + 1 : i + max_len + 1])

print('NB sequences:', len(sentences))

X = np.zeros((len(sentences), max_len, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), max_len, len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
	for t, char in enumerate(sentence):
		X[i, t, char_index[char]] = 1
		y[i, t, char_index[next_chars[i][t]]] = 1

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def print_samples(model, sample_size=700):
    start_index = random.randint(0, len(text) - max_len - 1)

    for diversity in [0.2, 0.3, 0.5, 0.7, 0.8]:
        print()
        print('----- diversity:', diversity)

        sentence = text[start_index: start_index + max_len]
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(sentence)

        # Printing the sample
        for i in range(sample_size):
            x = np.zeros((1, max_len, len(chars)))
            # Build the one-hot encoding for the sentence
            for t, char in enumerate(sentence):
                x[0, t, char_index[char]] = 1.

            preds = model.predict(x, verbose=0)[0][-1]
            next_index = sample(preds, diversity)
            next_char = index_char[next_index]

            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()

last_loss = -1.

for iteration in range(1, 19):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    history = model.fit(X, y,
                        batch_size=128,
                        epochs=40)

    if iteration % 3 == 0:
        print_samples(model)
    if last_loss >= 0 and last_loss - history.history['loss'][0] < 0.001:
        break
    
    last_loss = history.history['loss'][0]