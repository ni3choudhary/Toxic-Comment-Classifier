import pickle
import tensorflow as tf
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import numpy as np
from flask import Flask, render_template, request

MAX_FEATURES = 200000  # number of words in the vocab
vectorizer = TextVectorization(max_tokens=MAX_FEATURES,
                               output_sequence_length=1800,
                               output_mode='int')

model = tf.keras.models.load_model('toxic_comments_model.h5')
labels = pickle.load(open('labels.pkl', 'rb'))
# input_str = vectorizer(np.expand_dims('hey, i freaken hate you!',axis=0))

# res = model.predict(input_str)
# print(res)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        comment = request.form['text']
        vectorized_text = vectorizer(np.expand_dims(comment, axis=0))
        result = model.predict(vectorized_text)
        
        res = {}
        for idx, col in enumerate(labels):
            res[col] = result[0][idx] > 0.5

        return render_template('index.html', result = res,labels = labels)


if __name__ == '__main__':
    app.run(debug=True)
