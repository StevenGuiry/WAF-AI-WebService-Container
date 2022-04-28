from crypt import methods
from flask import Flask, request, render_template
#from flask_cors import CORS
import numpy as np
import pickle
import logging
import json
import urllib.parse

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
words = ['SLEEP', 'DROP', 'UNION', 'SELECT', 'WAITFOR', 'DELAY', 'ORDER BY', 'GROUP BY', 'DELETE','OR', 'AND', 'WHERE']

model = None

def create_app():
    app = Flask(__name__)
    #CORS(app)

    with open('xgb_model.pkl', 'rb') as f:
        model = pickle.load(f)


    @app.route("/")
    def index():
        return render_template('WAF-AI.html')

    @app.route('/predict', methods=['POST'])
    def get_prediction():
        if request.method == 'POST':
            
            sql_words = 0
            # Parse request 
            data = request.get_json()
            data = json.dumps(data)
            # Decode any URL encoding
            data = urllib.parse.unquote_plus(data)
            # Count the features
            single_q = data.count("'")
            double_q = data.count("\"")
            dash = data.count("-")
            brace = data.count("(") + data.count(")")
            slash = data.count("/")
            dot = data.count(".")
            asterik = data.count("*")
            for word in words:
                sql_words += data.count(word)
            if single_q == 0 & double_q > 2:
                no_quote = 1
            else:
                no_quote = 0

            # Send features to model to get prediction
            data = [single_q, dot, slash, no_quote]
            app.logger.info(str(data))
            data = np.array(data)[np.newaxis, :]
            prediction = model.predict(data)
        if prediction[0] == 0:
            return "Good"
        else:
            return "Bad"
    
    return app

    #     @app.route('/predict', methods=['POST'])
    # def get_prediction():
    #     if request.method == 'POST':
    #         data = request.get_json()
    #         data = np.array(data)[np.newaxis, :]
    #         prediction = model.predict(data)
    #     return str(prediction[0])