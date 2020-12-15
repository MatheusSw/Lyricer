from numpy import array
from pickle import dump
import os
import random
import string
import tensorflow as tf
import datetime

data_path = os.path.join(
    os.getcwd(), r"Lyrics\lyrics_filtered_everything.txt")


def clean_data(text):
    # replace '--' with a space ' '
    text = text.replace('--', ' ')
    # split into tokens by white space
    tokens = text.split()
    # remove punctuation from each token
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    # make lower case
    tokens = [word.lower() for word in tokens]
    return tokens


def load_data(file_path, enc='utf-8'):
    f = open(file_path, 'r', encoding=enc)
    text = f.read()
    f.close()
    return text

# Shoutout to machinelearningmastery


def make_training_data(data):
    length = 50 + 1  # Hyper
    sequences = list()
    for i in range(length, len(data)):
        seq = data[i-length:i]
        line = ' '.join(seq)
        sequences.append(line)
    return sequences


def save_file(lines, filename):
    data = '\n'.join(lines)
    file = open(filename, 'w', encoding='utf-8')
    file.write(data)
    file.close()
    return data


def build_model():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Embedding(
        vocab_size, 50, input_length=seq_length))
    model.add(tf.keras.layers.GRU(50, return_sequences=True, dropout=0.35))
    model.add(tf.keras.layers.GRU(100))
    model.add(tf.keras.layers.Dense(100, activation='relu'))
    model.add(tf.keras.layers.Dense(vocab_size, activation='softmax'))
    print(model.summary())
    return model

# generate a sequence from a language model


def generate_seq(model, tokenizer, seq_length, seed_text, n_words):
    result = list()
    in_text = seed_text
    # generate a fixed number of words
    for _ in range(n_words):
        # encode the text as integer
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        # truncate sequences to a fixed length
        encoded = tf.keras.preprocessing.sequence.pad_sequences(
            [encoded], maxlen=seq_length, truncating='pre')
        # predict probabilities for each word
        yhat = model.predict_classes(encoded, verbose=0)
        # map predicted word index to word
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
        # append to input
        in_text += ' ' + out_word
        result.append(out_word)
    return ' '.join(result)

text = clean_data(load_data(data_path))
training = make_training_data(text)

training = save_file(training, r"AI Misc\BROCKHAMPTON_sequences.txt")
training = training.split('\n')

tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(training)  # Feed the texts

# Turn them into sequences of integers
sequences = tokenizer.texts_to_sequences(training)
vocab_size = len(tokenizer.word_index) + 1

##########################################################################
sequences = array(sequences)
X, y = sequences[:, :-1], sequences[:, -1]
y = tf.keras.utils.to_categorical(y, num_classes=vocab_size)
seq_length = X.shape[1]

model = build_model()

checkpoint_file = os.path.join(os.getcwd(), r"AI Misc\Checkpoints")

checkpoint_file = os.path.join(checkpoint_file, "ckpt_{epoch}")

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_file,
    save_weights_only=True)

log_path = os.path.join(os.getcwd(), "AI Misc/Logs/" +
                        datetime.datetime.now().strftime("%d%m%Y-%H%M%S"))

tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=log_path, histogram_freq=1, write_images=True)

dump(tokenizer, open('tokenizer_dump.pkl', 'wb'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])
model.fit(X, y, batch_size=128, epochs=80, callbacks=[
          checkpoint_callback, tensorboard_callback])

#############################################################################
seq_length = len(training[0].split()) - 1

seed_text = training[random.randint(0, len(training))]
seed_text = """
I got cracks in my phone screen
The past fuck with my psyche
Smoke weed and get high, please
Went to school in The Woodlands
And that made niggas wanna fight me
So I don't take threats lightly
Tell them niggas, "Come and find me"
Gotta say it in my eye
"""
print("Initial Text: " + seed_text + "\n=======")

generated = generate_seq(model, tokenizer, seq_length, seed_text, 150)
print("Generated Text: \n" + generated)
